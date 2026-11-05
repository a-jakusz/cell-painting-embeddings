"""JUMP (cpg0016): скачать CSV плашки и собрать из него изображение сайта."""

import io
from pathlib import Path

import fsspec
import numpy as np
import polars as pl
import tifffile

ROOT = "cellpainting-gallery/cpg0016-jump"
DATA_DIR = Path(__file__).resolve().parents[1] / "data"  # cell-painting-embeddings/data

# порядок каналов в сохранённом файле (ось 0)
CHANNELS = ["DNA", "ER", "Mito", "AGP", "RNA"]


def download_plate_csv(source, batch, plate, name="load_data_with_illum.csv"):
    """Шаг 1. Скачивает CSV плашки в data/csv/... и возвращает локальный путь."""
    fs = fsspec.filesystem("s3", anon=True)
    remote = f"{ROOT}/{source}/workspace/load_data_csv/{batch}/{plate}/{name}"
    local = DATA_DIR / "csv" / source / batch / plate / name
    local.parent.mkdir(parents=True, exist_ok=True)
    fs.get(remote, str(local))
    return local


def save_site_image(source, batch, plate, well, site, name="load_data_with_illum.csv"):
    """Шаг 2. Находит в CSV плашки строку (well, site), качает 5 каналов (Orig),
    склеивает в массив (5, H, W) и сохраняет в data/images/<source>/<plate>/<well>_s<site>.tif.
    Если CSV плашки ещё не скачан, скачивает его.
    """
    csv_path = DATA_DIR / "csv" / source / batch / plate / name
    if not csv_path.exists():
        download_plate_csv(source, batch, plate, name)
    df = pl.read_csv(csv_path, infer_schema_length=0)  # всё как строки
    row = df.filter(
        (pl.col("Metadata_Well") == well) & (pl.col("Metadata_Site") == str(site))
    )
    if row.height != 1:
        raise LookupError(f"{well}, сайт {site}: найдено строк {row.height}")
    row = row.row(0, named=True)

    out = DATA_DIR / "images" / row["Metadata_Source"] / row["Metadata_Plate"] / f"{well}_s{site}.tif"
    if out.exists():
        return out

    fs = fsspec.filesystem("s3", anon=True)
    channels = []
    for ch in CHANNELS:
        url = row[f"URL_Orig{ch}"].removeprefix("s3://")
        with fs.open(url, "rb") as f:
            channels.append(tifffile.imread(io.BytesIO(f.read())))
    stack = np.stack(channels)  # (5, H, W), uint16

    out.parent.mkdir(parents=True, exist_ok=True)
    tifffile.imwrite(out, stack, compression="zlib")
    return out


# import matplotlib.colors as mpl  # noqa: CPY001
# import numpy as np
# from jump_portrait.fetch import get_item_location_metadata, get_jump_image
# from matplotlib import pyplot as plt

# def display_site(
#     source: str,
#     batch: str,
#     plate: str,
#     well: str,
#     site: int,
#     label: str,
#     int_percentile: float,
# ) -> None:
#     """Plot all channels from one image.

#     Parameters
#     ----------
#     source : String
#         Source ID for image of interest.
#     batch : String
#         Batch ID for image of interest.
#     plate : String
#         Plate ID for image of interest.
#     well : String
#         Well ID for image of interest.
#     site : String
#         Site ID for image of interest.
#     label : String
#         Label to display in lower left corner.
#     int_percentile: float
#         Rescale the image from 0 - this percentile of intensity values.

#     """
#     n_rows = 2
#     n_cols = 3

#     # Make images
#     axes = plt.subplots(n_rows, n_cols, figsize=(2.6 * n_cols, 2.6 * n_rows))[1]
#     axes = axes.ravel()

#     channel_rgb = {
#         "AGP": "#FF7F00",  # Orange
#         "DNA": "#0000FF",  # Blue
#         "ER": "#00FF00",  # Green
#         "Mito": "#FF0000",  # Red
#         "RNA": "#FFFF00",  # Yellow
#     }

#     for ax, (channel, rgb) in zip(axes, channel_rgb.items()):
#         cmap = mpl.LinearSegmentedColormap.from_list(channel, ("#000", rgb))

#         img = get_jump_image(source, batch, plate, well, channel, site)

#         ax.imshow(img, vmin=0, vmax=np.percentile(img, int_percentile), cmap=cmap)
#         ax.axis("off")

#         # Add channel name label in the top left corner
#         ax.text(
#             0.05,
#             0.95,
#             channel,
#             horizontalalignment="left",
#             verticalalignment="top",
#             fontsize=18,
#             color="black",
#             bbox=dict(
#                 facecolor="white", alpha=0.8, edgecolor="none", boxstyle="round,pad=0.3"
#             ),
#             transform=ax.transAxes,
#         )

#     # put label in last subplot
#     ax = axes[-1]
#     ax.text(
#         0.5,
#         0.5,
#         label,
#         horizontalalignment="center",
#         verticalalignment="center",
#         fontsize=20,
#         color="black",
#         transform=ax.transAxes,
#     )
#     ax.axis("off")

#     # show plot
#     plt.tight_layout()