USE EVAnalyticsDB;
GO
SELECT COUNT(*) AS raw_rows FROM dbo.EV_Stations_Raw;
SELECT COUNT(*) AS clean_rows FROM dbo.EV_Stations_Clean;
SELECT COUNT(*) AS prediction_rows FROM dbo.EV_Demand_Prediction;
SELECT TOP 10 * FROM dbo.vw_EV_State_Summary ORDER BY station_count DESC;
SELECT TOP 10 * FROM dbo.vw_EV_City_Summary ORDER BY avg_demand_score DESC;
SELECT TOP 10 * FROM dbo.EV_Demand_Prediction ORDER BY avg_demand_score DESC;
