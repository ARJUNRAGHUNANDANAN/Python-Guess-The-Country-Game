import os
import re
import json
import geopandas as gpd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import requests
from zipfile import ZipFile

class CountryShapeExtractor:
    def __init__(self, shapefile, output_folder):
        self.shapefile = shapefile
        self.output_folder = output_folder
        self.processed_countries = set()
        self.country_json_path = os.path.join(self.output_folder, 'country.json')
        self.initialize_country_json()

    def initialize_folders(self):
        os.makedirs(self.output_folder, exist_ok=True)

    def initialize_country_json(self):
        # Ensure the country.json file is empty at the start of each execution
        with open(self.country_json_path, 'w') as json_file:
            json.dump([], json_file)

    def fetch_and_extract_zip(self, url, extract_to):
        # Ensure the directory exists
        os.makedirs(extract_to, exist_ok=True)

        zip_path = os.path.join(extract_to, 'wb_countries_admin0_10m.zip')
        print(f"Downloading zip file from {url}...")
        response = requests.get(url, stream=True)
        with open(zip_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print("Download complete. Extracting...")

        with ZipFile(zip_path, 'r') as zip_ref:
            # Extract all members
            for member in zip_ref.namelist():
                # Construct the target path
                member_path = os.path.join(extract_to, member)
                # Check if member is a directory
                if member.endswith('/'):
                    os.makedirs(member_path, exist_ok=True)
                else:
                    # Extract file
                    zip_ref.extract(member, extract_to)
                    # Move the file if it is inside an unintended subdirectory
                    if os.path.dirname(member_path) != extract_to:
                        final_path = os.path.join(extract_to, os.path.basename(member))
                        os.rename(member_path, final_path)

        print("Extraction complete.")
        os.remove(zip_path)

    def sanitize_filename(self, name):
        return re.sub(r'[^a-zA-Z0-9_-]', '', name)

    def process_country(self, row):
        country_name = row['NAME_EN'].replace(" ", "")
        iso_code = row['ISO_A2']

        if iso_code == '-99':
            iso_code = 'NONE'

        if country_name in self.processed_countries:
            return None

        self.processed_countries.add(country_name)
        geom = row['geometry']
        sanitized_country_name = self.sanitize_filename(country_name)
        filename = f"{iso_code}-{sanitized_country_name}.jpg"
        filepath = os.path.join(self.output_folder, filename)

        return filepath, geom, {
            'name': country_name,
            'iso_code': iso_code,
            'filename': filename
        }

    def plot_geometry(self, geom, filepath):
        fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
        fig.patch.set_facecolor('blue')
        ax.set_facecolor('blue')

        minx, miny, maxx, maxy = geom.bounds
        geom_width = maxx - minx
        geom_height = maxy - miny
        geom_aspect = geom_width / geom_height

        if geom_aspect > 1:
            ax.set_xlim(minx, maxx)
            ax.set_ylim(miny - (geom_width - geom_height) / 2, maxy + (geom_width - geom_height) / 2)
        else:
            ax.set_xlim(minx - (geom_height - geom_width) / 2, maxx + (geom_height - geom_width) / 2)
            ax.set_ylim(miny, maxy)

        if geom.geom_type == 'Polygon':
            ax.fill(*geom.exterior.xy, color='green')
        elif geom.geom_type == 'MultiPolygon':
            for polygon in geom.geoms:
                ax.fill(*polygon.exterior.xy, color='green')
        else:
            print(f"Unsupported geometry type: {geom.geom_type}")
            return False

        ax.set_aspect('equal')
        ax.set_axis_off()

        plt.savefig(filepath, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close(fig)
        print(f"Exported image to {filepath}")
        return True

    def extract_shapes(self):
        world = gpd.read_file(self.shapefile)
        for index, row in world.iterrows():
            result = self.process_country(row)
            if result:
                filepath, geom, country_details = result
                if self.plot_geometry(geom, filepath):
                    self.append_country_details(country_details)

    def append_country_details(self, country_details):
        with open(self.country_json_path, 'r+') as json_file:
            data = json.load(json_file)
            data.append(country_details)
            json_file.seek(0)  # Move to the beginning of the file
            json.dump(data, json_file, indent=4)

    def cleanup(self):
        confirm = input(f"Do you want to delete the '{self.output_folder}' directory? (yes/no, default: no): ").strip().lower()
        if confirm == '' or confirm == 'no':
            print(f"Preserved '{self.output_folder}' directory.")
        elif confirm == 'yes':
            os.system(f'rm -rf {self.output_folder}')
            print(f"Deleted '{self.output_folder}' directory.")
        else:
            print("Invalid input. Preserving directory by default.")

def main():
    base_directory = os.getcwd()
    default_shapefile_dir = os.path.join(base_directory, 'WB_countries_Admin0_10m')
    default_shapefile = os.path.join(default_shapefile_dir, 'WB_countries_Admin0_10m.shp')
    output_folder = os.path.join(base_directory, 'exported_data')

    use_default = input(f"Do you want to use the default shapefile location ({default_shapefile})? (yes/no): ").strip().lower()
    if use_default == 'yes':
        if not os.path.exists(default_shapefile):
            print(f"Shapefile not found at the default location: {default_shapefile}")
            print("Fetching the latest version...")
            url = "https://datacatalogfiles.worldbank.org/ddh-published/0038272/DR0046659/wb_countries_admin0_10m.zip?versionId=2024-05-14T14:58:01.5696428Z"
            extractor = CountryShapeExtractor(default_shapefile, output_folder)
            extractor.initialize_folders()
            extractor.fetch_and_extract_zip(url, default_shapefile_dir)
        else:
            print(f"Shapefile found at the default location: {default_shapefile}")
    else:
        while True:
            shapefile = input("Please provide the full path to the 'WB_countries_Admin0_10m.shp' file: ").strip()
            if shapefile:
                if not os.path.exists(shapefile):
                    print(f"Shapefile not found at the provided location: {shapefile}")
                else:
                    default_shapefile = shapefile
                    break
            else:
                print("No path provided. Exiting.")
                return

    extractor = CountryShapeExtractor(default_shapefile, output_folder)
    extractor.initialize_folders()
    if not os.path.exists(default_shapefile):
        print(f"Shapefile not found at the specified location: {default_shapefile}")
        return
    extractor.extract_shapes()
    extractor.cleanup()

if __name__ == "__main__":
    main()
