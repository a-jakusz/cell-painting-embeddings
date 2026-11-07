import matplotlib.colors as mpl  # noqa: CPY001
import numpy as np
from jump_portrait.fetch import get_item_location_metadata, get_jump_image
from matplotlib import pyplot as plt
from src.utils import download_plate_csv, save_site_image

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

SOURCE, BATCH = "source_7", "20210723_Run2" # obtained experimentally
N_WELLS, SITES, N_DMSO = 3, [1, 2, 3], 40

def pick(df):
    df = df.filter((df["Metadata_Source"] == SOURCE) & (df["Metadata_Batch"] == BATCH))
    return df.select("Metadata_Plate", "Metadata_Well").unique().sort("Metadata_Plate", "Metadata_Well")

# extract compounds
plates = set()
for name, jcp in COMPOUNDS.items():
    wells = pick(get_item_location_metadata(jcp, input_column="JCP2022")).head(N_WELLS)
    for plate, well in wells.rows():
        plates.add(plate)
        for site in SITES:
            save_site_image(SOURCE, BATCH, plate, well, site, group=name)
    print('completed:', name)

# extract DMSO (negative probe) from same plates
dmso = pick(get_item_location_metadata("IAZDPXIOMUYVGZ-UHFFFAOYSA-N")) # InChiKey DMSO
dmso = dmso.filter(dmso["Metadata_Plate"].is_in(list(plates))).sample(N_DMSO, seed=0)
for plate, well in dmso.rows():
    for site in SITES:
        save_site_image(SOURCE, BATCH, plate, well, site, group="dmso")
print('dmso completed')