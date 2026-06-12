import pandas as pd
import pyodbc
from pathlib import Path
from common import load_config, odbc_connection_string

RAW_QUERY = """
SELECT station_id, station_name, city, state, country, latitude, longitude, ev_network,
       ev_connector_types, ev_level1_evse_num, ev_level2_evse_num, ev_dc_fast_num,
       access_code, status_code, open_date
FROM dbo.EV_Stations_Raw
WHERE station_id IS NOT NULL;
"""

def clean_dataframe(df):
    df = df.copy()
    text_cols = ["station_name", "city", "state", "country", "ev_network", "ev_connector_types", "access_code", "status_code"]
    for col in text_cols:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()
    for col in ["ev_level1_evse_num", "ev_level2_evse_num", "ev_dc_fast_num"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df["total_ports"] = df["ev_level1_evse_num"] + df["ev_level2_evse_num"] + df["ev_dc_fast_num"]
    df["charger_category"] = "Level 2 / Standard"
    df.loc[df["ev_dc_fast_num"] > 0, "charger_category"] = "DC Fast Available"
    df.loc[(df["ev_dc_fast_num"] == 0) & (df["ev_level2_evse_num"] == 0), "charger_category"] = "Basic / Unknown"
    df["open_year"] = pd.to_datetime(df["open_date"], errors="coerce").dt.year
    city_count = df.groupby(["state", "city"])["station_id"].transform("count")
    df["demand_score"] = df["total_ports"].clip(upper=20) * 3 + df["ev_dc_fast_num"].clip(upper=10) * 5 + city_count.clip(upper=50) * 1.5
    df["demand_category"] = pd.cut(df["demand_score"], bins=[-1, 20, 60, 9999], labels=["Low", "Medium", "High"]).astype(str)
    return pd.DataFrame({
        "station_id": df["station_id"].astype(str), "station_name": df["station_name"], "city": df["city"], "state": df["state"], "country": df["country"],
        "latitude": pd.to_numeric(df["latitude"], errors="coerce"), "longitude": pd.to_numeric(df["longitude"], errors="coerce"),
        "ev_network": df["ev_network"], "connector_types": df["ev_connector_types"],
        "level1_count": df["ev_level1_evse_num"], "level2_count": df["ev_level2_evse_num"], "dc_fast_count": df["ev_dc_fast_num"],
        "total_ports": df["total_ports"], "charger_category": df["charger_category"], "access_type": df["access_code"], "station_status": df["status_code"],
        "open_year": df["open_year"], "demand_score": df["demand_score"], "demand_category": df["demand_category"]
    }).drop_duplicates(subset=["station_id"])

def main():
    config = load_config()
    conn = pyodbc.connect(odbc_connection_string(config))
    raw = pd.read_sql(RAW_QUERY, conn)
    clean = clean_dataframe(raw)
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE dbo.EV_Stations_Clean;")
    insert_sql = """INSERT INTO dbo.EV_Stations_Clean
    (station_id, station_name, city, state, country, latitude, longitude, ev_network, connector_types, level1_count, level2_count, dc_fast_count, total_ports, charger_category, access_type, station_status, open_year, demand_score, demand_category)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.fast_executemany = True
    rows = [tuple(None if pd.isna(x) else x for x in row) for row in clean.itertuples(index=False, name=None)]
    cursor.executemany(insert_sql, rows)
    conn.commit()
    out_path = Path(r"D:\ANCHAL\MINI Project SEM 2\EV_Charging_Analytics_Project\data\processed\ev_stations_clean.csv")
    clean.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Loaded {len(clean):,} clean rows into dbo.EV_Stations_Clean")

if __name__ == "__main__":
    main()
