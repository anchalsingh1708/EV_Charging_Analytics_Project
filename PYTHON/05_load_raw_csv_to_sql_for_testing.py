import pandas as pd
import pyodbc
from pathlib import Path
from common import load_config, odbc_connection_string

COLUMNS = [
    "station_id", "station_name", "street_address", "city", "state", "zip", "country",
    "latitude", "longitude", "ev_network", "ev_connector_types", "ev_level1_evse_num",
    "ev_level2_evse_num", "ev_dc_fast_num", "access_code", "access_days_time",
    "status_code", "open_date", "date_last_confirmed", "source_file"
]

def none_if_nan(value):
    return None if pd.isna(value) else value

def main():
    config = load_config()
    csv_path = Path(config["raw_csv_path"])
    df = pd.read_csv(csv_path)
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None
    for col in ["ev_level1_evse_num", "ev_level2_evse_num", "ev_dc_fast_num"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["open_date", "date_last_confirmed"]:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
    conn = pyodbc.connect(odbc_connection_string(config))
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE dbo.EV_Stations_Raw;")
    cursor.fast_executemany = True
    sql = """INSERT INTO dbo.EV_Stations_Raw
    (station_id, station_name, street_address, city, state, zip, country, latitude, longitude, ev_network,
     ev_connector_types, ev_level1_evse_num, ev_level2_evse_num, ev_dc_fast_num, access_code, access_days_time,
     status_code, open_date, date_last_confirmed, source_file)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    rows = [tuple(none_if_nan(x) for x in row) for row in df[COLUMNS].itertuples(index=False, name=None)]
    cursor.executemany(sql, rows)
    conn.commit()
    print(f"Loaded {len(rows):,} rows into dbo.EV_Stations_Raw")

if __name__ == "__main__":
    main()
