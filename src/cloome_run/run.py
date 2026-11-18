import os
import polars as pl
from third_party.cloome.src.cloome.model import CLOOME
from huggingface_hub import hf_hub_download
from src.cloome_run.split import split_channels_tmp, iter_run2_tifs

# get checkpoint from Hugging Face
FILENAME = "cloome-bioactivity.pt"
REPO_ID = "anasanchezf/cloome"
ckpt = hf_hub_download(REPO_ID, FILENAME)

CLOOME_DIR = os.path.join("third_party", "cloome")
config = os.path.join(CLOOME_DIR, "src", "training", "model_configs", "RN50.json")

OUT = os.path.join("data", "embeddings", "embs.parquet")

encoder = CLOOME(ckpt, config)

rows = []
for tif in iter_run2_tifs("data/images/source_7"):
    with split_channels_tmp(tif) as images:
        emb = encoder.encode_images(images)[0].cpu().tolist()
    # path: data/images/<source>/<batch>/<compound>/<plate>_<well>_s<site>.tif
    source, batch, compound = tif.parts[-4], tif.parts[-3], tif.parts[-2]
    plate, well, site = tif.stem.split("_")
    rows.append({
        "source": source, "batch": batch, "compound": compound,
        "plate": plate, "well": well, "site": int(site.removeprefix("s")),
        "file": tif.name, "embedding": emb,
    })
    print(len(rows), tif)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
pl.DataFrame(rows).write_parquet(OUT)
print(f"saved {len(rows)} embeddings to {OUT}")
