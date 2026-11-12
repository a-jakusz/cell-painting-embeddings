import tempfile
from contextlib import contextmanager
from pathlib import Path

import tifffile

RUN2_DIR = Path("data/images/source_7/20210723_Run2")

STACK_CHANNELS = ["DNA", "ER", "Mito", "AGP", "RNA"]

# CLOOME expects exactly this order: Mito, ERSyto, ERSytoBleed, Ph_golgi, Hoechst
# mapping CLOOME channel name -> channel name in our stack
CLOOME_TO_STACK = {
    "Mito": "Mito",
    "ERSyto": "ER",
    "ERSytoBleed": "RNA",
    "Ph_golgi": "AGP",
    "Hoechst": "DNA",
}


# Split a (5, H, W) tif into 5 single-channel temporary tif files.
#   for tif in iter_run2_tifs():
#       with split_channels_tmp(tif) as files:
#           emb = encoder.encode_images(files)
@contextmanager
def split_channels_tmp(tif_path):
    stack = tifffile.imread(tif_path)
    if stack.ndim != 3 or stack.shape[0] != len(STACK_CHANNELS):
        raise ValueError(f"{tif_path}: expected shape (5, H, W), got {stack.shape}")

    with tempfile.TemporaryDirectory(prefix="cloome_") as tmp:
        paths = []
        for cloome_name, stack_name in CLOOME_TO_STACK.items():
            p = Path(tmp) / f"{cloome_name}.tif"
            tifffile.imwrite(p, stack[STACK_CHANNELS.index(stack_name)])
            paths.append(str(p))
        yield paths


def iter_run2_tifs(root=RUN2_DIR):
    return sorted(Path(root).rglob("*.tif"))
