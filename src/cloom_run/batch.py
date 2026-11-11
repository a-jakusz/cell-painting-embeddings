import tempfile
from contextlib import contextmanager
from pathlib import Path

import tifffile

RUN2_DIR = Path("data/images/source_7/20210723_Run2")

# channel order inside our stacked tif (see src.utils.CHANNELS)
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


@contextmanager
def split_channels_tmp(tif_path):
    """Split a (5, H, W) tif into 5 single-channel temporary tif files.

    Yields a list of 5 file paths (str) in the order required by CLOOME
    (Mito, ERSyto, ERSytoBleed, Ph_golgi, Hoechst). The files live in a
    temporary directory that is deleted when the `with` block exits.

        with split_channels_tmp(path) as files:
            emb = encoder.encode_images(files)
    """
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
    """All stacked tif files of source_7 run2 (every compound folder)."""
    return sorted(Path(root).rglob("*.tif"))
