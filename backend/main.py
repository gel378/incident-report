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

BASE_DIR     = Path(__file__).parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(title="Incident Report Generator")
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ── Helpers ───────────────────────────────────────────────────────────────────

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
    return json.loads(frame.to_json(orient="records", date_format="iso", default_handler=str))


# ── Static / root ─────────────────────────────────────────────────────────────

@app.get("/api/debug/tracking/{code}")
async def debug_tracking(code: str):
    from database import get_conn
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM tracking_ref WHERE tracking_code=?", (code,)
        ).fetchone()
    return dict(row) if row else {"error": "not found"}

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


# ── Tracking reference CRUD ───────────────────────────────────────────────────

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


# ── Incident processing ───────────────────────────────────────────────────────

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

    return JSONResponse({
        "stats": {
            "total":  len(processed["inc"]),
            "system": int((processed["inc"]["Type"] == "SYSTEM").sum()),
            "ops":    int((processed["inc"]["Type"] == "OPS").sum()),
            "pe":     int((processed["inc"]["Type"] == "PE").sum()),
        },
        "inc":        df_to_json(processed["inc"]),
        "categories": df_to_json(processed["categories"]),
        "acupick":    df_to_json(processed["acupick"]),
        "ops_issues": df_to_json(processed["ops_issues"]),
        "summary": {
            "date_from": processed["summary"]["date_from"],
            "date_to":   processed["summary"]["date_to"],
            "daily":     processed["summary"]["daily"],
            "totals":    processed["summary"]["totals"],
        },
        "tracking_map": get_tracking_map(),
    })


@app.post("/api/export")
async def export(
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

    processed  = process_csv(df, date_from, date_to)
    xlsx_bytes = build_workbook(processed)

    filename = f"incident_report_{date_from}_to_{date_to}.xlsx"
    return StreamingResponse(
        io.BytesIO(xlsx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )