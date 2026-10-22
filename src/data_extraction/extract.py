import matplotlib.colors as mpl  # noqa: CPY001
import numpy as np
from jump_portrait.fetch import get_item_location_metadata, get_jump_image
from matplotlib import pyplot as plt

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

