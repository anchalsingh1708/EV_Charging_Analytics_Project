# EV Charging Analytics Dashboard

An end-to-end EV charging analytics project built using Python, SQL Server, SSIS, and Power BI. It extracts charging station data from an API, processes it, predicts city-level demand, and displays the results through an interactive dashboard.

## Features

- EV charging station API extraction
- CSV-to-SQL Server loading using SSIS
- Data cleaning and transformation using Python
- City-level demand prediction
- Interactive Power BI dashboard
- Automated pipeline using a batch file
- Scheduled execution using Windows Task Scheduler
- Email notification after every successful step

## Technology Stack

- Python
- Pandas
- Requests
- SQL Server
- SSIS
- Power BI
- Windows Task Scheduler
- Gmail SMTP

## Workflow

```text
EV Charging API
        |
        v
Python API Extraction
        |
        v
Raw CSV Dataset
        |
        v
SSIS ETL Package
        |
        v
SQL Server Database
        |
        v
Python Cleaning and Prediction
        |
        v
Power BI Dashboard
