import os
from third_party.cloome.src.cloome.model import CLOOME
from huggingface_hub import hf_hub_download

# get checkpoint from Hugging Face
FILENAME = "cloome-bioactivity.pt"
REPO_ID = "anasanchezf/cloome"
ckpt = hf_hub_download(REPO_ID, FILENAME)

CLOOME_DIR = os.path.join("third_party", "cloome")
config = os.path.join(CLOOME_DIR, "src", "training", "model_configs", "RN50.json")
images = [os.path.join(CLOOME_DIR, "example", "images", f"{channel}.tif") for channel in ["Mito", "ERSyto", "ERSytoBleed", "Ph_golgi", "Hoechst"]]


encoder = CLOOME(ckpt, config)
img_embeddings = encoder.encode_images(images)
print(img_embeddings)