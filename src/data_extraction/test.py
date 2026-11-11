import matplotlib.colors as mpl  # noqa: CPY001
import numpy as np
import polars as pl
from jump_portrait.fetch import get_item_location_metadata, get_jump_image
from matplotlib import pyplot as plt
import tifffile
from src.utils import download_plate_csv, save_site_image

# selected compounds, searched in JCP storage in website
COMPOUNDS = {
    "aspirin": "JCP2022_008461", "ibuprofen": "JCP2022_029646",
    "butylparaben": "JCP2022_073093", "ampicillin": "JCP2022_004119",
    "tobramycin": "JCP2022_059846", "nicotine": "JCP2022_084364",
    "biotin": "JCP2022_107379", "melatonin": "JCP2022_017740",
    "nocodazole": "JCP2022_047835", "colchicine": "JCP2022_033814",
    "7-ethylcamptothecin": "JCP2022_057405", "cycloheximide": "JCP2022_109917",
    "vorinostat": "JCP2022_097466", "cortisol": "JCP2022_042931",
    "curcumin": "JCP2022_093608", "retinoic_acid": "JCP2022_083214",
    "rotenone": "JCP2022_042266", "rapamycin": "JCP2022_018522",
    "resveratrol": "JCP2022_051785", "quercetin": "JCP2022_077797",
}

# get metadata of aspirin, check data
aspirin = get_item_location_metadata("JCP2022_073093", input_column="JCP2022")

print(aspirin.shape)
print(aspirin.head())

r = aspirin.row(0, named=True)
print(r)

# didn't work out, during get_jump_image .parquet file is searched, no .parquet file in open dataset
# img = get_jump_image(
#     source=r['Metadata_Source'],
#     batch=r['Metadata_Batch'],
#     plate=r['Metadata_Plate'],
#     well=r['Metadata_Well'],
#     channel='DNA',
#     site='1'
# )
# print(img.shape)
# print(img.dtype)

# check opened dataset, what's inside, butylparaben example: same path, but not .parquet files, simple .csv
import fsspec
fs = fsspec.filesystem("s3", anon=True)
base = "cellpainting-gallery/cpg0016-jump/source_1/workspace/load_data_csv/Batch6_20221102/" # customly created from metadata
print(fs.ls(base)[:10])                 # which plates exist in this batch
print(fs.ls(base + "UL000583"))       # what's inside needed plate

# use of custom csv-file downloader
# csv_path = download_plate_csv(
#     source=r['Metadata_Source'],
#     batch=r['Metadata_Batch'],
#     plate=r['Metadata_Plate'],
# )
# print(csv_path)

# use of custom image extraction pipeline
p = save_site_image(
    source=r['Metadata_Source'],
    batch=r['Metadata_Batch'],
    plate=r['Metadata_Plate'],
    well=r['Metadata_Well'],
    site='1'
)

img = tifffile.imread(p)   # (5, 1080, 1080)
plt.imshow(img[3])   # 0 = DNA, 1 = ER, 2 = Mito, 3 = AGP, 4 = RNA
plt.show()

# check, whether each of my compounds is available in source 7 -- yes
missing_source_7 = []   # compounds, that are missing in source 7

for name, jcp in COMPOUNDS.items():
    df = get_item_location_metadata(jcp, input_column="JCP2022")
    has_source_7 = (df["Metadata_Source"] == "source_7").any()   # флаг
    if not has_source_7:
        missing_source_7.append(name)

print(missing_source_7)

# check, at which batch possibly all compounds are availabe -- 20210723_Run2 and 20210803_Run5
frames = []
for name, jcp in COMPOUNDS.items():
    df = get_item_location_metadata(jcp, input_column="JCP2022")
    df = df.filter(pl.col("Metadata_Source") == "source_7").with_columns(pl.lit(name).alias("compound"))
    frames.append(df)
wells = pl.concat(frames)

print(
    wells.group_by("Metadata_Batch")
         .agg(pl.col("compound").n_unique().alias("n_compounds"),
              pl.col("Metadata_Plate").n_unique().alias("n_plates"))
         .sort("n_compounds", descending=True)
)