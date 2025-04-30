import typer
from pyfiglet import Figlet
import os
import glob
from download import *
from bronze import *
from silver import *
from run_pipeline import *

app = typer.Typer()

# Load .env just in case defaults are needed
#load_dotenv()



def main():
    """
    CI/CD Data Pipeline CLI Entry Point
    """ 

    # Banner
    fig = Figlet(font='slant')
    typer.secho(fig.renderText("CI/CD CLI"), fg=typer.colors.CYAN) 

    # STEP 1 ### ENTER Prompt for URL and Key
    url = typer.prompt("🌐 Enter your CDSAPI URL")
    key = typer.prompt("🔑 Enter your CDSAPI Key", hide_input=True)

    ### 
    # Validate
    if not url or not key:
        typer.secho("❌ CDSAPI credentials missing!", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) 
    
    typer.secho(f"\n✅ Using CDSAPI URL: {url}", fg=typer.colors.GREEN)
    typer.secho(f"✅ Using CDSAPI KEY: {'*' * len(key)}", fg=typer.colors.GREEN)
 
    
    ## STEP 2 Prompt for shapefile folder
    shapefile_folder = typer.prompt("📁 Enter your shapefile folder path")

    shapefile_list = glob.glob(os.path.join(shapefile_folder, "*.shp"))

    if not shapefile_list:
        typer.secho(f"❌ No shapefiles found in folder: {shapefile_folder}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    shapefile = shapefile_list[0]
    typer.secho(f"📄 Found shapefile: {shapefile}", fg=typer.colors.BLUE) 

    ## STEP 3 Prompt to enter [declare rest of the parameters]
    ## dataset name
    ## product type
    ## variable
    ## year
    ## month 
    ## data_format
    ## download_folder
    ## bronze_output_folder
    ## silver_output_folder 

    # 🌍 Dataset selection
    dataset = typer.prompt("🌍 Enter the [bold]CDS dataset name[/bold] (e.g., reanalysis-era5-single-levels-monthly-means)") 

    # 📦 Product type
    product_type_str = typer.prompt("📦 Enter the [bold]product type(s)[/bold], comma-separated (e.g., monthly_averaged_reanalysis)")
    product_type = [p.strip() for p in product_type_str.split(",")]
    
    # 🌡️ Variables
    variable_str = typer.prompt("🌡️ Enter the [bold]climate variable(s)[/bold], comma-separated (e.g., 2m_temperature, total_precipitation)")
    variable = [v.strip() for v in variable_str.split(",")] 

    # 📅 Years
    year_str = typer.prompt("📅 Enter the [bold]year(s)[/bold], comma-separated (e.g., 2023, 2024)")
    year = [y.strip() for y in year_str.split(",")] 

    # 🗓️ Months
    month_str = typer.prompt("🗓️ Enter the [bold]month(s)[/bold], comma-separated (e.g., 01, 02)")
    month = [m.strip() for m in month_str.split(",")] 

    # 📄 File format (usually fixed)
    data_format = "netcdf"
    typer.secho("📄 Data format set to [bold]netcdf[/bold] by default.", fg=typer.colors.CYAN)

    # 📂 Folder structure
    download_folder = typer.prompt("📥 Enter the [bold]download folder name[/bold] (e.g., vermont_monthly)")
    bronze_output_folder = typer.prompt("🥉 Enter the [bold]bronze output folder name[/bold] (e.g., vermont_monthly_bronze)")
    silver_output_folder = typer.prompt("🥈 Enter the [bold]silver output folder name[/bold] (e.g., vermont_monthly_silver)") 

    ### # 👇 Call the pipeline
    run_pipeline(
    shapefile=shapefile,
    url=url,
    key=key,
    dataset=dataset,
    product_type=product_type,
    variable=variable,
    year=year,
    month=month,
    data_format=data_format,
    download_folder=download_folder,
    bronze_output_folder=bronze_output_folder,
    silver_output_folder=silver_output_folder)

    



# 🔚 CLI Entry Point
if __name__ == "__main__":
    typer.run(main)








