import matplotlib.colors as mpl  # noqa: CPY001
import numpy as np
from jump_portrait.fetch import get_item_location_metadata, get_jump_image
from matplotlib import pyplot as plt
import tifffile
from src.utils import download_plate_csv, save_site_image


aspirin = get_item_location_metadata("JCP2022_073093", input_column="JCP2022")

print(aspirin.shape)
print(aspirin.head())

r = aspirin.row(0, named=True)
print(r)

# import fsspec
# fs = fsspec.filesystem("s3", anon=True)
# base = "cellpainting-gallery/cpg0016-jump/source_1/workspace/load_data_csv/Batch6_20221102/"
# print(fs.ls(base)[:10])                 # какие плашки есть в партии
# print(fs.ls(base + "UL000583"))       # что лежит в нужной плашке

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

# csv_path = download_plate_csv(
#     source=r['Metadata_Source'],
#     batch=r['Metadata_Batch'],
#     plate=r['Metadata_Plate'],
# )
# print(csv_path)

p = save_site_image(
    source=r['Metadata_Source'],
    batch=r['Metadata_Batch'],
    plate=r['Metadata_Plate'],
    well=r['Metadata_Well'],
    site='1'
)

img = tifffile.imread(p)   # (5, 1080, 1080)

plt.imshow(img[4], cmap="gray")   # 0 = DNA, 1 = ER, 2 = Mito, 3 = AGP, 4 = RNA
plt.show()