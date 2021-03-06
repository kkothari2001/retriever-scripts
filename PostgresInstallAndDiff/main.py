import retriever as rt
import os
import shutil as sh
from difflib import HtmlDiff
import json
from datetime import datetime, timezone
from json.decoder import JSONDecodeError

IGNORE_LIST = ['alberta-detailed-soil-survey', 'amniote-life-hist', 'antarctic-breed-bird', 'aquatic-animal-excretion', 'arsenic-contamination-bangladesh', 'baltimore-restaurants', 'bioclim', 'biodiversity-response', 'biomass-allometry-db', 'biotime', 'biotimesql', 'bird-migration-data', 'bird-size', 'boston-buildbps', 'boston-buildbpss', 'breast-cancer-wi', 'breed-bird-survey', 'breed-bird-survey-50stop', 'breed-bird-survey-nlcd', 'british-columbia-detailed-soil-survey', 'bupa-liver-disorders', 'butterfly-population-network', 'canada-soil-survery', 'canada-soil-survey', 'catalogos-dados-brasil', 'chytr-disease-distr', 'community-abundance-misc', 'coronavirus-belgium', 'coronavirus-italy', 'coronavirus-south-korea', 'county-emergency-management-offices', 'credit-card-fraud', 'croche-vegetation-data', 'dicerandra-frutescens', 'ecoregions-us', 'fao-global-capture-product', 'felix-riese-hyperspectral-soilmoisture', 'fernow-air-temperature', 'fernow-biomass', 'fernow-forest-streamflow', 'fernow-nadp-rain-chemistry', 'fernow-precipitation', 'fernow-precipitation-chemistry', 'fernow-soil-productivity', 'fernow-stream-chemistry', 'fernow-watershed-acidification', 'fia-alabama', 'fia-alaska', 'fia-american-samoa', 'fia-arizona', 'fia-arkansas', 'fia-california', 'fia-colorado', 'fia-connecticut', 'fia-delaware', 'fia-federated-states-micrones', 'fia-florida', 'fia-georgia', 'fia-guam', 'fia-hawaii', 'fia-idaho', 'fia-illinois', 'fia-indiana', 'fia-iowa', 'fia-kansas', 'fia-kentucky', 'fia-louisiana', 'fia-maine', 'fia-maryland', 'fia-massachusetts', 'fia-michigan', 'fia-minnesota', 'fia-mississippi', 'fia-missouri', 'fia-montana', 'fia-nebraska', 'fia-nevada', 'fia-new-hampshire', 'fia-new-jersey', 'fia-new-mexico', 'fia-new-york', 'fia-north-carolina', 'fia-north-dakota', 'fia-northern-mariana-islands', 'fia-ohio', 'fia-oklahoma', 'fia-oregon', 'fia-palau', 'fia-pennsylvania', 'fia-puerto-rico', 'fia-rhode-island', 'fia-south-carolina', 'fia-south-dakota', 'fia-tennessee', 'fia-texas', 'fia-us-virgin-islands', 'fia-utah', 'fia-vermont', 'fia-virginia', 'fia-washington', 'fia-west-virginia', 'fia-wisconsin', 'fia-wyoming', 'fish-parasite-hosts', 'flensburg-food-web', 'foreign-exchange-rates-2000-2019', 'forest-biomass-china', 'forest-fires-portugal', 'forest-inventory-analysis', 'forest-plots-michigan', 'forest-plots-wghats', 'foster-ltreb', 'fray-jorge-ecology', 'gdp', 'gentry-forest-transects', 'global-population-dynamics', 'globi-interaction', 'great-basin-mammal-abundance', 'home-ranges', 'intertidal-abund-me', 'jornada-lter-rodent', 'la-selva-trees', 'lake-county-illinois-cancer-rates', 'lakecats-final-tables', 'leaf-herbivory', 'macroalgal-communities', 'macrocystis-variation', 'mammal-community-db', 'mammal-diet', 'mammal-life-hist', 'mammal-masses', 'mammal-metabolic-rate', 'mammal-super-tree', 'mapped-plant-quads-co',
               'mapped-plant-quads-id', 'mapped-plant-quads-ks', 'mapped-plant-quads-mt', 'marine-recruitment-data', 'mediter-basin-plant-traits', 'mt-st-helens-veg', 'nadp-precipitation-chemistry', 'national-pedon-database-summary-layer', 'nematode-traits', 'new-york-city-airbnb-open-data', 'ngreatplains-flowering-dates', 'nla', 'noaa-fisheries-trade', 'north-carolina-piedmont-mapped-foreset', 'north-carolina-piedmont-permanent-plots', 'north-carolina-piedmont-seedlng-sampling', 'north-carolina-piedmont_seedlng_sampling', 'nova-scotia-detailed-soil-survey', 'npn', 'nyc-tree-count', 'ontario-detailed-soil-survey', 'pantheria', 'partners-in-flight', 'phytoplankton-size', 'plant-comp-ok', 'plant-life-hist-eu', 'plant-occur-oosting', 'plant-taxonomy-us', 'portal-project-teaching', 'prairie-forest', 'predator-prey-body-ratio', 'predator-prey-size-marine', 'prince-edward-island-detailed-soil-survey', 'prism-climate', 'predicts', 'rainfall-in-india', 'sample-hdf', 'saskatchewan-detailed-soil-survey', 'shortgrass-steppe-lter', 'socean-diet-data', 'soil-db', 'soil-landscapes-of-canada', 'sonoran-desert', 'species-exctinction-rates', 'streamflow-conditions', 'sycamore-creek-macroinvertebrate', 'titanic', 'transparencia-dados-abertos-brasil', 'tree-canopy-geometries', 'tree-demog-wghats', 'turtle-offspring-nesting', 'usda-agriculture-plants-database', 'usda-dietary-supplement-ingredient-data', 'usda-mafcl-fooddatacenteral-alldatatypes', 'usda-mafcl-fooddatacenteral-brandedfoods', 'usda-mafcl-fooddatacenteral-fndds', 'usda-mafcl-fooddatacenteral-foundationfoods', 'usda-mafcl-fooddatacenteral-srlegacy', 'usda-mafcl-fooddatacenteral-supportingdata', 'usda-mafcl-standard-reference', 'usgs-elevation', 'ushio-maizuru-fish-community', 'veg-plots-sdl', 'vertnet', 'vertnet-amphibians', 'vertnet-birds', 'vertnet-fishes', 'vertnet-mammals', 'vertnet-reptiles', 'virgin-islands-coral-decadal-scale', 'virgin-islands-coral-diadema-antillarum', 'virgin-islands-coral-geography', 'virgin-islands-coral-juvenile', 'virgin-islands-coral-landscape-scale', 'virgin-islands-coral-octocorals-count', 'virgin-islands-coral-physical-measurements', 'virgin-islands-coral-population-projections', 'virgin-islands-coral-recruitment-tiles', 'virgin-islands-coral-scleractinian-corals', 'virgin-islands-coral-taxonomy', 'virgin-islands-coral-yawzi-transects', 'white-clay-creek-avondale-soil', 'white-clay-creek-boulton-chemistry', 'white-clay-creek-chlorophyll', 'white-clay-creek-christina-chemistry', 'white-clay-creek-christina-sediment', 'white-clay-creek-christina-temperatures', 'white-clay-creek-streamflow', 'white-clay-creek-swrc-meteorology', 'white-clay-creek-waterlevels', 'white-clay-dissolved-carbon', 'white-clay-dissolved-carbon ', 'wine-composition', 'wine-quality', 'wood-density', 'worldclim-five', 'worldclim-ten', 'worldclim-thirty', 'worldclim-twofive', 'yukon-detailed-soil-survey', 'zipcodes', 'abalone-age', 'nd-gain', 'elton-traits', 'poker-hands', 'nuclear-power-plants', 'airports', 'car-eval', 'portal', 'portal-dev', 'airport-codes', 'forest-health-monitoring-wyoming', 'forest-health-monitoring-newhampshire', 'forest-health-monitoring-newjersey', 'mtbs-burn-area-boundary', 'forest-health-monitoring-tennessee', 'forest-health-monitoring-michigan', 'national-usfs-finalfire-perimeter', 'usa-activity-silvreforestation', 'forest-health-monitoring-missouri', 'forest-health-monitoring-utah', 'forest-health-monitoring-colorado', 'forest-health-monitoring-vermont', 'forest-health-monitoring-northcarolina', 'forest-health-monitoring-southcarolina', 'forest-health-monitoring-alabama', 'forest-health-monitoring-maine', 'iris', 'forest-health-monitoring-california', 'nytimes-us-covid', 'activity-range-vegetation-improvement', 'forest-health-monitoring-pennsylvania', 'forest-health-monitoring-virginia', 'forest-health-monitoring-florida', 'acton-lake', 'forest-health-monitoring-minnesota', 'forest-health-monitoring-oregon', 'forest-health-monitoring-connecticut', 'mtbs-fire-occurrence', 'forest-health-monitoring-delaware', 'forest-health-monitoring-georgia', 'forest-health-monitoring-westvirginia', 'forest-health-monitoring-newyork', 'forest-health-monitoring-illinois', 'forest-health-monitoring-massachusetts', 'forest-health-monitoring-indiana', 'forest-health-monitoring-rhodeisland', 'forest-health-monitoring-wisconsin', 'activity-timberharvest', 'forest-health-monitoring-maryland', 'fire-occurrence-firestat-yearly', 'forest-health-monitoring-idaho', 'activity-silviculture-timber-stand-improvement', 'forest-health-monitoring-nevada']


# Takes all the scripts that are not in the ignore list and creates a list
scripts = [script for script in rt.reload_scripts()
           if script.name not in IGNORE_LIST]

# Prints them (just for debugging reference)
print([script.name for script in scripts])


# Defining all the paths that will be useful in the future.
# This section will be useful to make the paths OS-independent
file_location = os.path.normpath(os.path.dirname(os.path.realpath(__file__)))
new_store_path = os.path.normpath(os.path.join(file_location, 'new'))
old_store_path = os.path.normpath(os.path.join(file_location, 'old'))
diff_store_path = os.path.normpath(os.path.join(file_location, 'diffs'))


def install_postgres(dataset):
    # Function to install the dataset in postgres form into the database.
    # Uses the retriever postgres engine.
    '''
     required_opts = [
        ("user", "Enter your PostgreSQL username", "postgres"),
        ("password", "Enter your password", ""),
        ("host", "Enter your PostgreSQL host", "localhost"),
        ("port", "Enter your PostgreSQL port", 5432),
        I'm hoping the above 3 will automatically get installed by
        ("database", "Enter your PostgreSQL database name", "postgres"),
        ("database_name", "Format of schema name", "{db}"),
        ("table_name", "Format of table name", "{db}.{table}"),
    ]
    '''
    # database_name = "{}".format(dataset.name)
    args = {
        "command": 'install',
        "dataset": dataset,
        "database_name": dataset.name
    }
    test_engine = rt.engines.postgres.engine()
    test_engine.opts = args
    dataset.download(engine=test_engine, debug=True)

    folder_save_location = os.path.normpath(
        os.path.join(new_store_path, dataset.name))
    if not os.path.exists(folder_save_location):
        os.makedirs(folder_save_location)
    test_engine.to_csv(path=folder_save_location)
    test_engine.final_cleanup()


def create_diff(dataset_name, file_name):
    # Creates the diff for a single file, and stores in the appropriate location
    # Used inside check_diffs
    html_diff = HtmlDiff()
    html_filename = file_name[:-4] + ".html"

    diff_file_path = os.path.normpath(os.path.join(
        diff_store_path, dataset_name, html_filename))

    old_file_path = os.path.normpath(os.path.join(
        old_store_path, dataset_name, file_name))

    new_file_path = os.path.normpath(os.path.join(
        new_store_path, dataset_name, file_name))

    with open(new_file_path, "r") as new_file,\
            open(old_file_path, "r") as old_file,\
            open(diff_file_path, "w") as html_file:
        diff_lines = html_diff.make_file(old_file, new_file, context=True)
        html_file.writelines(diff_lines)


def check_diffs(dataset):
    # Creates all the diffs for a particular dataset
    diff_loc = os.path.normpath(os.path.join(diff_store_path, dataset.name))
    old_loc = os.path.normpath(os.path.join(old_store_path, dataset.name))
    new_loc = os.path.normpath(os.path.join(new_store_path, dataset.name))

    # Error checking to make sure all required directories exist.
    if not os.path.exists(new_loc):
        install_postgres(dataset)
    if not os.path.exists(old_loc):
        sh.copytree(new_loc, old_loc)
    if not os.path.exists(diff_loc):
        os.makedirs(diff_loc)

    # Cycle through all files in the dataset and
    # find the diff of each file using the helper function create_diff
    for csv in os.listdir(old_loc):
        try:
            create_diff(dataset.name, csv)
        except e:
            print(e)


def get_md5(dataset):
    # Function to get md5 hash of a particular file
    # Uses retriever functionality.
    md5 = rt.lib.engine_tools.getmd5(
        os.path.join(new_store_path, dataset.name),
        data_type='dir', encoding=dataset.encoding)
    return md5


def save_md5(dataset):
    # Parent driver function for the md5 functionality.
    # Also handles the json functionality to store the hashes.
    md5 = get_md5(dataset)
    print(md5)

    dataset_details = 0
    try:
        with open(os.path.join(file_location, "dataset_details.json"), "r") as json_file:
            dataset_details = json.load(json_file)
    except (OSError, JSONDecodeError):
        dataset_details = dict()
        dataset_details['hashes'] = {}

    dataset_details["hashes"][str(dataset.name)] = md5
    dataset_details["LastChecked"] = datetime.now(
        timezone.utc).strftime("%d %b %Y")

    with open(os.path.join(file_location, "dataset_details.json"), "w+") as json_file:
        json.dump(dataset_details, json_file, indent=4)


# ================================================ Main Script starts
for script in scripts:
    install_postgres(script)
    save_md5(script)

if not os.path.exists(old_store_path):
    print("No old data to compare to, creating it based on the new data downloaded")
    sh.copytree(new_store_path, old_store_path)

for script in scripts:
    check_diffs(script)
