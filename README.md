# Smart EV Charging Infrastructure Analytics and Demand Forecasting System

End-to-end mini project using Python API extraction, SQL Server, SSIS, Python analytics, and Power BI.

## Local setup

- Project folder: `D:\ANCHAL\MINI Project SEM 2\EV_Charging_Analytics_Project`
- SQL Server instance: `.\SQLEXPRESS`
- Database: `EVAnalyticsDB`
- API: NLR Alternative Fuel Stations API (formerly NREL developer API) filtered to `fuel_type=ELEC`

## Execution order

1. Create database and tables:

```powershell
sqlcmd -S .\SQLEXPRESS -E -i "D:\ANCHAL\MINI Project SEM 2\EV_Charging_Analytics_Project\sql\01_create_database_and_tables.sql"
```

2. Install Python requirements if needed:

```powershell
pip install -r "D:\ANCHAL\MINI Project SEM 2\EV_Charging_Analytics_Project\requirements.txt"
```

3. Copy `config\config.example.json` to `config\config.json` and add your NREL API key. `DEMO_KEY` works for testing.

4. Download API data:

```powershell
python "D:\ANCHAL\MINI Project SEM 2\EV_Charging_Analytics_Project\python\01_extract_ev_api.py"
```

5. Load `data\raw\ev_stations_raw.csv` into `dbo.EV_Stations_Raw` using SSIS. Follow `ssis\SSIS_Setup_Guide.md`.

6. Run cleaning and prediction:

```powershell
python "D:\ANCHAL\MINI Project SEM 2\EV_Charging_Analytics_Project\python\02_clean_transform_load.py"
python "D:\ANCHAL\MINI Project SEM 2\EV_Charging_Analytics_Project\python\03_demand_prediction.py"
```

7. Build the Power BI dashboard with `powerbi\PowerBI_Dashboard_Build_Guide.md` and save it as `powerbi\EV_Charging_Dashboard.pbix`.

## Note on `.pbix` and `.dtsx`

A real `.pbix` must be saved by Power BI Desktop, and a production `.dtsx` package should be created/generated in Visual Studio SSDT. This project includes the database, Python, SSIS Biml, DAX, theme, and exact build steps. Power BI Desktop/SSDT were not found on PATH, so I created the ready-to-build assets rather than a fake binary file.
