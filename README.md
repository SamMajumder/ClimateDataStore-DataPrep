# 🌦️ ClimateDataStore-DataPrep

A modular and interactive command-line pipeline for downloading, processing, and indexing ERA5 monthly-averaged climate data from the Copernicus Climate Data Store (CDS) using a user-provided shapefile.

---

## 📁 Repository Structure

```
ClimateDataStore-DataPrep/
├── basecode/                    # Core data processing functions (download, bronze, silver stages)
├── era5-monthly-averages/      # Main CLI interface and pipeline entrypoint
├── .gitignore
├── .actrc
└── README.md                    # You're here!
```

---

## 🚀 What This Project Does

This project provides a full ETL workflow for ERA5 monthly-averaged reanalysis data:

- ✅ Download climate data using a shapefile-defined region
- ✅ Organize data into CI/CD-style `bronze` and `silver` folders
- ✅ Apply H3 spatial indexing
- ✅ Use an interactive CLI to avoid hardcoding parameters

The CLI guides the user through each step with secure prompts and emoji-enhanced messages.

---

## 🧭 How to Use

### 1. 📦 Install Dependencies

First, create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

### 2. 🔑 Get Your CDS API Key

1. Register at [cds.climate.copernicus.eu/register](https://cds.climate.copernicus.eu/register)
2. Visit [cds.climate.copernicus.eu/api-how-to](https://cds.climate.copernicus.eu/api-how-to)
3. Copy your credentials:

```
CDSAPI URL: https://cds.climate.copernicus.eu/api/v2
CDSAPI KEY: abc12345-xxxx-yyyy-zzzz-yyyyyyyyyyyy
```

These will be entered securely when prompted by the CLI.

### 3. 📁 Prepare a Shapefile Folder

You must have a valid shapefile (including `.shp`, `.shx`, `.dbf`, and optionally `.prj`) placed in a folder like `vermont/`.

---

## ▶️ Running the CLI

Navigate into the CLI folder:

```bash
cd era5-monthly-averages
```

Run the pipeline:

```bash
python cli.py
```

The CLI will guide you through:

- Entering your CDS API credentials
- Specifying your shapefile folder
- Selecting dataset, variables, time range
- Defining output folders

---

## 📂 Output Structure

```
your-working-directory/
├── download_folder/           # NetCDF files + inventory_table.parquet
├── bronze_output_folder/      # Flattened netCDF bronze table
└── silver_output_folder/      # H3-tessellated silver table
```

---

## ✅ Example CLI Prompt Inputs

| Prompt                  | Example                                   |
|-------------------------|-------------------------------------------|
| CDSAPI URL              | `https://cds.climate.copernicus.eu/api/v2` |
| CDSAPI Key              | `abc12345-xxxx-yyyy-zzzz-yyyyyyyyyyyy`    |
| Shapefile folder        | `vermont`                                  |
| Dataset                 | `reanalysis-era5-single-levels-monthly-means` |
| Product type(s)         | `monthly_averaged_reanalysis`              |
| Variable(s)             | `2m_temperature, total_precipitation`      |
| Year(s)                 | `2023, 2024`                                |
| Month(s)                | `01, 02`                                    |
| Download folder         | `vermont_monthly`                          |
| Bronze output folder    | `vermont_monthly_bronze`                   |
| Silver output folder    | `vermont_monthly_silver`                   |

---

## 📦 `requirements.txt`

```
typer[all]
pyfiglet
pandas
pyarrow
xarray
netCDF4
numpy==1.26
geopandas
rasterio
shapely
h3
cdsapi
```

> ✅ `pyarrow` is required for saving `.parquet` files  
> ✅ `typer[all]` includes rich CLI formatting  
> ⚠️ `numpy==1.26` is pinned for compatibility

---

## 💡 Future Enhancements

- [ ] Add subcommands (`show-inventory`, `clear-cache`)
- [ ] Add support for `.env` fallback (optional)
- [ ] Dockerize pipeline
- [ ] Integrate with GitHub Actions

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---
