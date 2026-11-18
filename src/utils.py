import io
from pathlib import Path

import fsspec
import numpy as np
import polars as pl
import tifffile

ROOT = "cellpainting-gallery/cpg0016-jump"
DATA_DIR = Path(__file__).resolve().parents[1] / "data"  # cell-painting-embeddings/data

# channel order
CHANNELS = ["DNA", "ER", "Mito", "AGP", "RNA"]

# downloads csv of a plate, returns local path
def download_plate_csv(source, batch, plate, name="load_data_with_illum.csv"):
    fs = fsspec.filesystem("s3", anon=True)
    remote = f"{ROOT}/{source}/workspace/load_data_csv/{batch}/{plate}/{name}"
    local = DATA_DIR / "csv" / source / batch / plate / name
    local.parent.mkdir(parents=True, exist_ok=True)
    fs.get(remote, str(local))
    return local

# saves site into data/images/<source>/<batch>/<group>/<plate>_<well>_s<site>.tif
def save_site_image(source, batch, plate, well, site, group="misc",
                    name="load_data_with_illum.csv"):
    out = (DATA_DIR / "images" / source / batch / group
           / f"{plate}_{well}_s{site}.tif")
    if out.exists():
        return out

    csv_path = DATA_DIR / "csv" / source / batch / plate / name
    if not csv_path.exists():
        download_plate_csv(source, batch, plate, name)
    df = pl.read_csv(csv_path, infer_schema_length=0)
    row = df.filter(
        (pl.col("Metadata_Well") == well) & (pl.col("Metadata_Site") == str(site))
    )
    if row.height != 1:
        raise LookupError(f"{plate} {well}, сайт {site}: найдено строк {row.height}")
    row = row.row(0, named=True)

    fs = fsspec.filesystem("s3", anon=True)
    channels = []
    for ch in CHANNELS:
        url = row[f"URL_Orig{ch}"].removeprefix("s3://")
        with fs.open(url, "rb") as f:
            channels.append(tifffile.imread(io.BytesIO(f.read())))
    stack = np.stack(channels)  # (5, H, W)

    out.parent.mkdir(parents=True, exist_ok=True)
    tifffile.imwrite(out, stack, compression="zlib")
    return out