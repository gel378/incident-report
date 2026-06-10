import io
import json
from pathlib import Path
from datetime import date, datetime
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd

from database import (
    init_db, get_all_tracking, upsert_tracking,
    delete_tracking, get_tracking_map
)
from processor import process_csv
from exporter import build_workbook

app = FastAPI(title="Incident Report Generator", root_path="/IRT")
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR     = Path(__file__).parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


def parse_upload(filename: str, contents: bytes) -> pd.DataFrame:
    name = filename.lower()
    try:
        if name.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
        else:
            raise HTTPException(400, "Only .csv, .xlsx, or .xls files are accepted.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Could not parse file: {e}")
    df.columns = df.columns.str.strip()
    return df


def df_to_json(frame: pd.DataFrame) -> list:
    if frame is None or len(frame) == 0:
        return []
    return json.loads(frame.to_json(orient="records", date_format="iso", default_handler=str))


def json_serial(obj):
    if isinstance(obj, (datetime, date, pd.Timestamp)):
        return obj.strftime("%Y-%m-%d %H:%M:%S") if hasattr(obj, "hour") else str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        path = FRONTEND_DIR / "index.html"
        print(f"[DEBUG] Looking for index.html at: {path}")
        print(f"[DEBUG] File exists: {path.exists()}")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        import traceback
        traceback.print_exc()
        return HTMLResponse(f"<pre>Error: {e}</pre>", status_code=500)


# ── Tracking CRUD ─────────────────────────────────────────────────────────────

class TrackingEntry(BaseModel):
    id:            int | None = None
    type:          str
    ci:            str
    tracking_code: str
    category:      str


@app.get("/api/tracking")
async def api_get_tracking():
    return get_all_tracking()


@app.post("/api/tracking")
async def api_upsert_tracking(entry: TrackingEntry):
    try:
        row = upsert_tracking(entry.id, entry.type, entry.ci, entry.tracking_code, entry.category)
        return row
    except Exception as e:
        raise HTTPException(400, str(e))


@app.delete("/api/tracking/{id}")
async def api_delete_tracking(id: int):
    delete_tracking(id)
    return {"deleted": id}


# ── Preview ───────────────────────────────────────────────────────────────────

@app.post("/api/preview")
async def preview(
    file: UploadFile = File(...),
    date_from: str = Form(default=str(date.today())),
    date_to:   str = Form(default=str(date.today())),
):
    contents = await file.read()
    try:
        df = parse_upload(file.filename, contents)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Could not read file: {e}")

    try:
        processed = process_csv(df, date_from, date_to)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Processing error: {e}")

    def serialize_categories(cats: dict) -> dict:
        return {t: df_to_json(df) for t, df in cats.items()}

    return JSONResponse({
        "stats": {
            "total":  len(processed["inc"]),
            "system": int((processed["inc"]["Type"] == "SYSTEM").sum()),
            "ops":    int((processed["inc"]["Type"] == "OPS").sum()),
            "pe":     int((processed["inc"]["Type"] == "PE").sum()),
        },
        "inc":                 df_to_json(processed["inc"]),
        "acupick_inc":         df_to_json(processed["acupick_inc"]),
        "vpos_inc":            df_to_json(processed["vpos_inc"]),
        "acupick_categories":  serialize_categories(processed["acupick_categories"]),
        "acupick_ops":         df_to_json(processed["acupick_ops"]),
        "vpos_categories":     serialize_categories(processed["vpos_categories"]),
        "vpos_ops":            df_to_json(processed["vpos_ops"]),
        "summary": {
            "date_from": processed["summary"]["date_from"],
            "date_to":   processed["summary"]["date_to"],
            "daily":     processed["summary"]["daily"],
            "totals":    processed["summary"]["totals"],
        },
        "tracking_map": get_tracking_map(),
    })


# ── Export ────────────────────────────────────────────────────────────────────

@app.post("/api/export-edited")
async def export_edited(
    payload: dict,
):
    try:
        report_type = payload.get("report_type", "acupick")
        date_from   = payload.get("date_from", str(date.today()))
        date_to     = payload.get("date_to",   str(date.today()))
        inc_data    = payload.get("inc", [])

        # Rebuild inc DataFrame from edited frontend data
        inc = pd.DataFrame(inc_data)
        if inc.empty:
            raise HTTPException(400, "No INC data provided")

        from processor import (
            build_category_counts, build_category_callers,
            build_summary, VPOS_CI
        )

        vpos_inc    = inc[inc["Configuration Item"] == VPOS_CI].reset_index(drop=True)
        acupick_inc = inc[inc["Configuration Item"] != VPOS_CI].reset_index(drop=True)

        processed = {
            "inc":                 inc,
            "acupick_inc":         acupick_inc,
            "vpos_inc":            vpos_inc,
            "acupick_categories":  build_category_counts(acupick_inc),
            "acupick_ops":         build_category_callers(acupick_inc),
            "vpos_categories":     build_category_counts(vpos_inc),
            "vpos_ops":            build_category_callers(vpos_inc),
            "summary":             build_summary(inc, date_from, date_to),
        }

        xlsx_bytes = build_workbook(processed, report_type)
        filename   = f"{report_type}_incident_report_{date_from}_to_{date_to}.xlsx"
        return StreamingResponse(
            io.BytesIO(xlsx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Export error: {e}")
async def export(
    file: UploadFile = File(...),
    date_from:   str = Form(default=str(date.today())),
    date_to:     str = Form(default=str(date.today())),
    report_type: str = Form(default="acupick"),
):
    contents = await file.read()
    try:
        df = parse_upload(file.filename, contents)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Could not read file: {e}")

    try:
        processed = process_csv(df, date_from, date_to)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Processing error: {e}")

    try:
        print(f"[DEBUG] processed keys: {list(processed.keys())}")
        print(f"[DEBUG] report_type: {report_type}")
        import traceback
        xlsx_bytes = build_workbook(processed, report_type)
    except KeyError as e:
        traceback.print_exc()
        raise HTTPException(500, f"Export error - missing key: {e}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, f"Export error: {e}")

    filename = f"{report_type}_incident_report_{date_from}_to_{date_to}.xlsx"
    return StreamingResponse(
        io.BytesIO(xlsx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )