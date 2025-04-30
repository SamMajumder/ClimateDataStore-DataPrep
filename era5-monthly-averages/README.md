# 📦 ERA5 Monthly Averages CI/CD CLI

A friendly command-line tool to download, process, and index ERA5 climate data using a local shapefile and save the results in a CI/CD-ready structure with bronze and silver tables.

---

## 🚀 Features

- 📥 Downloads ERA5 monthly-averaged climate data from the Copernicus Climate Data Store (CDS)
- 🗂️ Organizes data into Bronze and Silver folders (including H3 tessellation)
- 📁 Accepts user-provided shapefiles
- 🧾 Fully interactive CLI with prompts and guidance
- ❌ No `.env` fallback — credentials must be entered securely at runtime

---

## 🔧 Installation

Create and activate a new environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

### 🛠️ `requirements.txt`

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

> ⚠️ The version of `numpy` is pinned to `1.26` for compatibility with geospatial and scientific libraries.
>  
> ✅ `pyarrow` is required for saving Parquet files.  
> ✅ `typer[all]` includes `rich`, which enables styled CLI prompts.

---

## 🔑 Getting Your CDS API Key

To download ERA5 data, you need a free account with the **Copernicus Climate Data Store (CDS)**.

1. 📄 Register at [cds.climate.copernicus.eu/register](https://cds.climate.copernicus.eu/register)
2. 🔑 After logging in, go to your [API page](https://cds.climate.copernicus.eu/api-how-to)
3. You'll see your `CDSAPI_URL` and `CDSAPI_KEY`. Example:

```text
https://cds.climate.copernicus.eu/api/v2
abc12345-xxxx-xxxx-xxxx-yyyyyyyyyyyy
```

> You’ll be prompted to enter these securely when running the CLI — **no need to store them in a file**.

---

## 📁 Required: Local Shapefile

This CLI **requires a valid shapefile** to define the area of interest for downloading data. You must provide the **path to a folder** that contains:

- `.shp`
- `.shx`
- `.dbf`
- (optionally) `.prj` and `.cpg`

**Example folder structure**:
```
vermont/
├── boundaries.shp
├── boundaries.shx
├── boundaries.dbf
└── boundaries.prj
```

---

## 🛠️ How to Use

Once everything is ready, run the CLI:

```bash
python cli.py
```

You’ll be interactively prompted to enter:

- CDS API URL and Key
- Shapefile folder path
- Dataset name (e.g. `reanalysis-era5-single-levels-monthly-means`)
- Product type(s) (e.g. `monthly_averaged_reanalysis`)
- Climate variable(s) (e.g. `2m_temperature, total_precipitation`)
- Year(s) (e.g. `2023, 2024`)
- Month(s) (e.g. `01, 02`)
- Folder names for download, bronze, and silver stages

---

## 📂 Output Structure

```
your-working-directory/
├── download_folder/           # NetCDF files + inventory_table.parquet
├── bronze_output_folder/      # Flattened netCDF bronze table
└── silver_output_folder/      # H3-tessellated silver table
```

---

## ✅ Example Prompt Answers

| Prompt                             | Example Input                             |
|------------------------------------|-------------------------------------------|
| CDSAPI URL                         | `https://cds.climate.copernicus.eu/api/v2` |
| CDSAPI Key                         | `abc12345-xxxx-yyyy-zzzz-yyyyyyyyyyyy`    |
| Shapefile folder                   | `vermont`                                  |
| Dataset                            | `reanalysis-era5-single-levels-monthly-means` |
| Product type(s)                    | `monthly_averaged_reanalysis`              |
| Variable(s)                        | `2m_temperature, total_precipitation`      |
| Year(s)                            | `2023, 2024`                                |
| Month(s)                           | `01, 02`                                    |
| Download folder                    | `vermont_monthly`                          |
| Bronze folder                      | `vermont_monthly_bronze`                   |
| Silver folder                      | `vermont_monthly_silver`                   |

---

## 💡 Future Ideas

- [ ] Add support for `.env` fallback (optional)
- [ ] Add subcommands like `show-inventory`, `clear-cache`
- [ ] Integrate Yaspin or Rich for loading feedback
- [ ] Dockerize for consistent deployments

---

## 📬 Questions or Contributions?

Feel free to open an issue or pull request if you'd like to suggest an improvement or need help getting started.

---
