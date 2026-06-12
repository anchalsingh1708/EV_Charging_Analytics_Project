from pathlib import Path
import pandas as pd
import requests
from common import load_config

NREL_URL = "https://developer.nlr.gov/api/alt-fuel-stations/v1.json"
DATA_GOV_URL = "https://api.data.gov.in/resource/203a82ce-9b00-4e3a-b18d-daf85e16684f"
NREL_COLUMNS = ["id", "station_name", "street_address", "city", "state", "zip", "country", "latitude", "longitude", "ev_network", "ev_connector_types", "ev_level1_evse_num", "ev_level2_evse_num", "ev_dc_fast_num", "access_code", "access_days_time", "status_code", "open_date", "date_last_confirmed"]

def extract_nrel(config):
    params = {"api_key": config.get("nrel_api_key", "DEMO_KEY"), "fuel_type": "ELEC", "country": config.get("nrel_country", "US"), "limit": int(config.get("nrel_limit", 2000)), "format": "JSON"}
    response = requests.get(NREL_URL, params=params, timeout=60)
    response.raise_for_status()
    df = pd.DataFrame(response.json().get("fuel_stations", []))
    for col in NREL_COLUMNS:
        if col not in df.columns:
            df[col] = None
    df = df[NREL_COLUMNS].rename(columns={"id": "station_id"})
    for col in ["latitude", "longitude", "ev_level1_evse_num", "ev_level2_evse_num", "ev_dc_fast_num"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def extract_india_supporting_dataset(config):
    params = {"api-key": "579b464db66ec23bdd00000149117228807449b882e96a", "format": "json", "limit": 1000}
    try:
        response = requests.get(DATA_GOV_URL, params=params, timeout=60)
        response.raise_for_status()
        df = pd.DataFrame(response.json().get("records", []))
        if not df.empty:
            df.to_csv(config["india_csv_path"], index=False, encoding="utf-8")
        return df
    except Exception as exc:
        print(f"India supporting dataset skipped: {exc}")
        return pd.DataFrame()

def main():
    config = load_config()
    raw_path = Path(config["raw_csv_path"])
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    df = extract_nrel(config)
    df["source_file"] = raw_path.name
    df.to_csv(raw_path, index=False, encoding="utf-8")
    print(f"Saved {len(df):,} NREL EV station rows to {raw_path}")
    india_df = extract_india_supporting_dataset(config)
    if not india_df.empty:
        print(f"Saved {len(india_df):,} India support rows to {config['india_csv_path']}")

if __name__ == "__main__":
    main()
