import pandas as pd
import pyodbc
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from common import load_config, odbc_connection_string

QUERY = """
SELECT state, city, COUNT(*) AS station_count, SUM(total_ports) AS total_ports,
       SUM(dc_fast_count) AS dc_fast_ports, AVG(CAST(demand_score AS FLOAT)) AS avg_demand_score
FROM dbo.EV_Stations_Clean
GROUP BY state, city;
"""

def label_clusters(df, labels):
    tmp = df.copy(); tmp["cluster"] = labels
    order = tmp.groupby("cluster")["avg_demand_score"].mean().sort_values().index.tolist()
    if len(order) < 3:
        return ["Medium" for _ in labels]
    mapping = {order[0]: "Low", order[1]: "Medium", order[2]: "High"}
    return [mapping[x] for x in labels]

def main():
    config = load_config()
    conn = pyodbc.connect(odbc_connection_string(config))
    df = pd.read_sql(QUERY, conn)
    if df.empty:
        raise SystemExit("No clean data found. Run SSIS raw load and 02_clean_transform_load.py first.")
    feature_cols = ["station_count", "total_ports", "dc_fast_ports", "avg_demand_score"]
    if len(df) >= 3:
        labels = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(StandardScaler().fit_transform(df[feature_cols].fillna(0)))
        df["predicted_demand_category"] = label_clusters(df, labels)
        model_name = "KMeans city demand clustering"
    else:
        df["predicted_demand_category"] = pd.cut(df["avg_demand_score"], [-1,20,60,9999], labels=["Low","Medium","High"]).astype(str)
        model_name = "Rule-based fallback"
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE dbo.EV_Demand_Prediction;")
    cursor.fast_executemany = True
    rows = [(r.state, r.city, int(r.station_count), int(r.total_ports or 0), int(r.dc_fast_ports or 0), float(r.avg_demand_score or 0), r.predicted_demand_category, model_name) for r in df.itertuples(index=False)]
    cursor.executemany("""INSERT INTO dbo.EV_Demand_Prediction
        (state, city, station_count, total_ports, dc_fast_ports, avg_demand_score, predicted_demand_category, model_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", rows)
    conn.commit()
    out_path = Path(r"D:\ANCHAL\MINI Project SEM 2\EV_Charging_Analytics_Project\data\processed\ev_demand_prediction.csv")
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Loaded {len(df):,} prediction rows into dbo.EV_Demand_Prediction")

if __name__ == "__main__":
    main()
