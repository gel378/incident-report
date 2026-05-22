import re
import pandas as pd
from datetime import datetime
from database import get_tracking_map, get_ci_type_map

DIVISIONS = [
    "Denver", "Haggen", "Intermountain", "Jewel-Osco", "MidAtlantic",
    "NorCal", "Portland", "Seattle", "Shaws", "SoCal", "Southern",
    "Southwest", "United"
]

CI_LIST = [
    "Online Shopping Fulfillment (OSFL)",
    "VPOS - Virtual Point of Sale System (OSVP)",
    "PPD - Personal Picking Device",
    "Lexmark MS610de",
    "Zebra GK420T",
    "Online Shopping Payment Dashboard and Refunds (OSDB)",
    "Descartes Route Planner (OSRP)",
    "Online Shopping Micro Services (OSMS)",
    "eCom Picking Mgmt. System (OSPK)",
    "eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)",
    "Online Shopping Payment Gateway (OSPG)",
    "eCom Online Shopping Last Mile (OSLM)",
    "Online Shopping Demand Planning (OSDP)",
    "Omni Channel Snap & EBT Payments (OCSE)",
    "Online Shopping Store Locator (OSSL)",
    "Online Shopping Made To Order (OSMO)",
    "eCom Customer Order - Control Tower (OSCT)",
]

TYPES = ["SYSTEM", "OPS", "PE"]

DIVISION_KEYWORDS = {
    "Denver":        ["denver"],
    "Haggen":        ["haggen"],
    "Intermountain": ["intermountain", "intermtn"],
    "Jewel-Osco":    ["jewel", "jewel-osco", "jewel osco"],
    "MidAtlantic":   ["midatlantic", "mid-atlantic", "mid atlantic"],
    "NorCal":        ["norcal", "nor cal", "northern cal"],
    "Portland":      ["portland"],
    "Seattle":       ["seattle"],
    "Shaws":         ["shaws", "shaw's"],
    "SoCal":         ["socal", "so cal", "southern cal"],
    "Southern":      ["southern"],
    "Southwest":     ["southwest", "south west"],
    "United":        ["united"],
}


def detect_division(site_zone: str) -> str:
    lower = site_zone.lower()
    for division, keywords in DIVISION_KEYWORDS.items():
        if any(k in lower for k in keywords):
            return division
    return ""


def detect_tracking_from_resolution(resolution: str, tracking_map: dict) -> str:
    if not resolution:
        return ""

    text = resolution.strip()
    first_line = text.split("\n")[0].strip()
    code_pat = re.compile("[A-Z]{2,6}[0-9]{3,6}")

    if code_pat.fullmatch(first_line):
        return first_line

    for code in tracking_map:
        if code.upper() in text.upper():
            return code

    match = code_pat.search(text)
    if match:
        return match.group(0)

    return ""


def build_inc(df: pd.DataFrame) -> pd.DataFrame:
    tracking_map = get_tracking_map()

    inc = pd.DataFrame()
    inc["Configuration Item"] = df.get("Configuration Item", pd.Series(dtype=str)).fillna("")
    inc["Caller"]             = df.get("Caller", pd.Series(dtype=str)).fillna("")
    inc["Resolution notes"]   = df.get("Resolution notes", pd.Series(dtype=str)).fillna("")
    inc["Site Zone"]          = df.get("Site Zone", pd.Series(dtype=str)).fillna("")

    inc["Tracking"] = inc["Resolution notes"].apply(
        lambda r: detect_tracking_from_resolution(r, tracking_map)
    )
    inc["Division"] = inc["Site Zone"].apply(detect_division)

    def resolve_type(row):
        # Derive type solely from tracking code — most accurate
        if row["Tracking"] and row["Tracking"] in tracking_map:
            return tracking_map[row["Tracking"]]["type"]
        # Fallback: scan tracking map by CI to find any matching type
        ci = row["Configuration Item"]
        for code, info in tracking_map.items():
            if info["ci"] == ci:
                return info["type"]
        return "OPS"

    inc["Type"] = inc.apply(resolve_type, axis=1)

    inc["Priority"]          = df.get("Priority", pd.Series(dtype=str)).fillna("")
    inc["Number"]            = df.get("Number", pd.Series(dtype=str)).fillna("")
    inc["Short description"] = df.get("Short description", pd.Series(dtype=str)).fillna("")
    inc["Description"]       = df.get("Description", pd.Series(dtype=str)).fillna("")
    inc["Knowledge Article"] = df.get("Knowledge Article", pd.Series(dtype=str)).fillna("")
    inc["State"]             = df.get("State", pd.Series(dtype=str)).fillna("")
    inc["Assigned to"]       = df.get("Assigned to", pd.Series(dtype=str)).fillna("")

    date_col = df.get("Created", df.get("Opened", pd.Series(dtype=str))).fillna("")
    inc["Date Opened"] = date_col.apply(
        lambda v: v.strftime("%Y-%m-%d") if hasattr(v, "strftime") else str(v) if v else ""
    )
    inc["Opened"] = df.get("Opened", df.get("Created", pd.Series(dtype=str))).fillna("").apply(
        lambda v: v.strftime("%Y-%m-%d") if hasattr(v, "strftime") else str(v) if v else ""
    )

    inc["Assignment group"] = df.get("Assignment group", pd.Series(dtype=str)).fillna("")
    inc["Work Notes"]       = df.get("Work notes", df.get("Work Notes", pd.Series(dtype=str))).fillna("")
    inc["Parent Incident"]  = df.get("Parent Incident", pd.Series(dtype=str)).fillna("")
    inc["Problem"]          = df.get("Problem", pd.Series(dtype=str)).fillna("")

    cols = [
        "Type", "Priority", "Number", "Short description", "Configuration Item",
        "Description", "Knowledge Article", "State", "Caller", "Assigned to",
        "Date Opened", "Opened", "Assignment group", "Work Notes", "Site Zone",
        "Parent Incident", "Tracking", "Division", "Problem", "Resolution notes"
    ]
    return inc[cols]


def build_category_counts(inc: pd.DataFrame) -> pd.DataFrame:
    tracking_map = get_tracking_map()
    codes = inc[inc["Tracking"] != ""]["Tracking"].unique()
    rows = []
    for code in sorted(codes):
        subset = inc[inc["Tracking"] == code]
        label = tracking_map.get(code, {}).get("category") or subset["Short description"].iloc[0]
        row = {"Code": code, "Category": label}
        for div in DIVISIONS:
            row[div] = int((subset["Division"] == div).sum())
        row["Total"] = sum(row[d] for d in DIVISIONS)
        rows.append(row)
    df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["Code", "Category"] + DIVISIONS + ["Total"])
    return df.sort_values("Total", ascending=False).reset_index(drop=True)


def build_category_callers(inc: pd.DataFrame) -> pd.DataFrame:
    tracking_map = get_tracking_map()
    ops = inc[inc["Type"] == "OPS"].copy()
    codes = ops[ops["Tracking"] != ""]["Tracking"].unique()
    rows = []
    for code in sorted(codes):
        subset = ops[ops["Tracking"] == code]
        label = tracking_map.get(code, {}).get("category") or subset["Short description"].iloc[0]
        row = {"Code": code, "Category": label}
        total = 0
        for div in DIVISIONS:
            callers = subset[subset["Division"] == div]["Caller"].tolist()
            row[div] = "\n".join(callers) if callers else "0"
            total += len(callers)
        row["Total"] = total
        rows.append(row)
    df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["Code", "Category"] + DIVISIONS + ["Total"])
    return df.sort_values("Total", ascending=False).reset_index(drop=True)


def build_summary(inc: pd.DataFrame, date_from: str, date_to: str) -> dict:
    def normalize_date(d):
        if not d:
            return ""
        d = str(d).strip().split(" ")[0].split("T")[0]
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
            try:
                return datetime.strptime(d, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return d

    inc = inc.copy()
    inc["_date_norm"] = inc["Date Opened"].apply(normalize_date)

    try:
        d_from = datetime.strptime(date_from, "%Y-%m-%d").strftime("%Y-%m-%d")
        d_to   = datetime.strptime(date_to,   "%Y-%m-%d").strftime("%Y-%m-%d")
    except Exception:
        d_from, d_to = date_from, date_to

    # All dates in range that have at least one incident
    in_range = inc[(inc["_date_norm"] >= d_from) & (inc["_date_norm"] <= d_to)]
    all_dates = sorted(in_range["_date_norm"].unique())

    # Per-day breakdown
    daily = []
    for day in all_dates:
        day_inc = inc[inc["_date_norm"] == day]
        rows = []
        for ci in CI_LIST:
            row = {"Configuration Item": ci}
            for t in TYPES:
                row[t] = int(((day_inc["Type"] == t) & (day_inc["Configuration Item"] == ci)).sum())
            rows.append(row)
        daily.append({"date": day, "data": rows})

    # Totals across full range
    totals = []
    for ci in CI_LIST:
        row = {"Configuration Item": ci}
        for t in TYPES:
            row[t] = int(((in_range["Type"] == t) & (in_range["Configuration Item"] == ci)).sum())
        row["Total"] = sum(row[t] for t in TYPES)
        totals.append(row)

    return {"date_from": d_from, "date_to": d_to, "daily": daily, "totals": totals}


def process_csv(df: pd.DataFrame, date_from: str, date_to: str) -> dict:
    inc         = build_inc(df)
    cat_counts  = build_category_counts(inc)
    cat_callers = build_category_callers(inc)
    acupick     = cat_counts[cat_counts["Total"] > 0].reset_index(drop=True)
    summary     = build_summary(inc, date_from, date_to)
    return {
        "inc":        inc,
        "categories": cat_counts,
        "acupick":    acupick,
        "ops_issues": cat_callers,
        "summary":    summary,
    }