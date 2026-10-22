import matplotlib.colors as mpl  # noqa: CPY001
import numpy as np
from jump_portrait.fetch import get_item_location_metadata, get_jump_image
from matplotlib import pyplot as plt

aspirin = get_item_location_metadata("JCP2022_008461", input_column="JCP2022")

print(aspirin.shape)
print(aspirin.head())

r = aspirin.row(0, named=True)
print(r)

import fsspec
fs = fsspec.filesystem("s3", anon=True)
base = "cellpainting-gallery/cpg0016-jump/source_7/workspace/load_data_csv/20210719_Run1/"
print(fs.ls(base)[:10])                 # какие плашки есть в партии
print(fs.ls(base + "CP1-SC1-04"))       # что лежит в нужной плашке

img = get_jump_image(
    source=r['Metadata_Source'],
    batch=r['Metadata_Batch'],
    plate=r['Metadata_Plate'],
    well=r['Metadata_Well'],
    channel='DNA',
    site='1'
)
print(img.shape)
print(img.dtype)