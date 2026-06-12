from pathlib import Path
import json

PROJECT_ROOT = Path(r"D:\ANCHAL\MINI Project SEM 2\EV_Charging_Analytics_Project")
CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "config.example.json"

def load_config():
    path = CONFIG_PATH if CONFIG_PATH.exists() else DEFAULT_CONFIG_PATH
    return json.loads(path.read_text(encoding="utf-8-sig"))

def odbc_connection_string(config):
    server = config.get("sql_server", r".\SQLEXPRESS")
    database = config.get("sql_database", "EVAnalyticsDB")
    if config.get("trusted_connection", True):
        return "DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + server + ";DATABASE=" + database + ";Trusted_Connection=yes;TrustServerCertificate=yes;"
    return "DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + server + ";DATABASE=" + database + ";UID=" + config["sql_user"] + ";PWD=" + config["sql_password"] + ";TrustServerCertificate=yes;"
