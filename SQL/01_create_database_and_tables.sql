IF DB_ID('EVAnalyticsDB') IS NULL
BEGIN
    CREATE DATABASE EVAnalyticsDB;
END
GO

USE EVAnalyticsDB;
GO

IF OBJECT_ID('dbo.EV_Stations_Raw', 'U') IS NOT NULL DROP TABLE dbo.EV_Stations_Raw;
GO
CREATE TABLE dbo.EV_Stations_Raw (
    raw_id INT IDENTITY(1,1) PRIMARY KEY,
    station_id NVARCHAR(100) NULL,
    station_name NVARCHAR(255) NULL,
    street_address NVARCHAR(255) NULL,
    city NVARCHAR(120) NULL,
    state NVARCHAR(80) NULL,
    zip NVARCHAR(30) NULL,
    country NVARCHAR(80) NULL,
    latitude VARCHAR(50) NULL,
    longitude VARCHAR(50) NULL,
    ev_network NVARCHAR(160) NULL,
    ev_connector_types NVARCHAR(255) NULL,
    ev_level1_evse_num VARCHAR(20) NULL,
    ev_level2_evse_num VARCHAR(20) NULL,
    ev_dc_fast_num VARCHAR(20) NULL,
    access_code NVARCHAR(80) NULL,
    access_days_time NVARCHAR(255) NULL,
    status_code NVARCHAR(80) NULL,
    open_date VARCHAR(30) NULL,
    date_last_confirmed VARCHAR(30) NULL,
    source_file NVARCHAR(260) NULL,
    loaded_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

CREATE UNIQUE INDEX UX_EV_Stations_Raw_station_id ON dbo.EV_Stations_Raw(station_id) WITH (IGNORE_DUP_KEY = ON);
GO

IF OBJECT_ID('dbo.EV_Stations_Clean', 'U') IS NOT NULL DROP TABLE dbo.EV_Stations_Clean;
GO
CREATE TABLE dbo.EV_Stations_Clean (
    clean_id INT IDENTITY(1,1) PRIMARY KEY,
    station_id NVARCHAR(100) NOT NULL,
    station_name NVARCHAR(255) NULL,
    city NVARCHAR(120) NOT NULL,
    state NVARCHAR(80) NOT NULL,
    country NVARCHAR(80) NOT NULL,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    ev_network NVARCHAR(160) NULL,
    connector_types NVARCHAR(255) NULL,
    level1_count INT NOT NULL DEFAULT 0,
    level2_count INT NOT NULL DEFAULT 0,
    dc_fast_count INT NOT NULL DEFAULT 0,
    total_ports INT NOT NULL DEFAULT 0,
    charger_category NVARCHAR(40) NOT NULL,
    access_type NVARCHAR(80) NULL,
    station_status NVARCHAR(80) NULL,
    open_year INT NULL,
    demand_score FLOAT NULL,
    demand_category NVARCHAR(30) NULL,
    cleaned_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

IF OBJECT_ID('dbo.EV_Demand_Prediction', 'U') IS NOT NULL DROP TABLE dbo.EV_Demand_Prediction;
GO
CREATE TABLE dbo.EV_Demand_Prediction (
    prediction_id INT IDENTITY(1,1) PRIMARY KEY,
    state NVARCHAR(80) NOT NULL,
    city NVARCHAR(120) NOT NULL,
    station_count INT NOT NULL,
    total_ports INT NOT NULL,
    dc_fast_ports INT NOT NULL,
    avg_demand_score FLOAT NOT NULL,
    predicted_demand_category NVARCHAR(30) NOT NULL,
    model_name NVARCHAR(80) NOT NULL,
    prediction_created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

IF OBJECT_ID('dbo.India_EV_Statewise', 'U') IS NOT NULL DROP TABLE dbo.India_EV_Statewise;
GO
CREATE TABLE dbo.India_EV_Statewise (
    record_id INT IDENTITY(1,1) PRIMARY KEY,
    state_ut NVARCHAR(120) NULL,
    public_charging_stations INT NULL,
    source NVARCHAR(120) NULL,
    loaded_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

CREATE OR ALTER VIEW dbo.vw_EV_State_Summary AS
SELECT state, COUNT(*) AS station_count, SUM(total_ports) AS total_ports,
       SUM(dc_fast_count) AS dc_fast_ports, AVG(CAST(demand_score AS FLOAT)) AS avg_demand_score
FROM dbo.EV_Stations_Clean
GROUP BY state;
GO

CREATE OR ALTER VIEW dbo.vw_EV_City_Summary AS
SELECT state, city, COUNT(*) AS station_count, SUM(total_ports) AS total_ports,
       SUM(dc_fast_count) AS dc_fast_ports, AVG(CAST(demand_score AS FLOAT)) AS avg_demand_score
FROM dbo.EV_Stations_Clean
GROUP BY state, city;
GO

CREATE OR ALTER VIEW dbo.vw_EV_Network_Summary AS
SELECT COALESCE(NULLIF(ev_network, ''), 'Unknown') AS ev_network,
       COUNT(*) AS station_count, SUM(total_ports) AS total_ports, SUM(dc_fast_count) AS dc_fast_ports
FROM dbo.EV_Stations_Clean
GROUP BY COALESCE(NULLIF(ev_network, ''), 'Unknown');
GO


