CREATE OR ALTER VIEW dbo.vw_PBI_Stations_Clean AS
SELECT CONCAT(state,'|',city) AS city_key, COALESCE(NULLIF(ev_network,''),'Unknown') AS network_key, *
FROM dbo.EV_Stations_Clean;
GO
CREATE OR ALTER VIEW dbo.vw_PBI_Demand_Prediction AS
SELECT CONCAT(state,'|',city) AS city_key, *
FROM dbo.EV_Demand_Prediction;
GO
CREATE OR ALTER VIEW dbo.vw_PBI_Dim_City AS
SELECT DISTINCT CONCAT(state,'|',city) AS city_key, state, city FROM dbo.EV_Stations_Clean
UNION
SELECT DISTINCT CONCAT(state,'|',city) AS city_key, state, city FROM dbo.EV_Demand_Prediction;
GO
CREATE OR ALTER VIEW dbo.vw_PBI_Dim_State AS
SELECT DISTINCT state FROM dbo.EV_Stations_Clean
UNION
SELECT DISTINCT state FROM dbo.EV_Demand_Prediction;
GO
CREATE OR ALTER VIEW dbo.vw_PBI_Dim_Network AS
SELECT DISTINCT COALESCE(NULLIF(ev_network,''),'Unknown') AS network_key FROM dbo.EV_Stations_Clean;
GO
