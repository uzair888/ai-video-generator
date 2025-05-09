import os
import torch
import random
from diffusers import StableDiffusionPipeline

# Set device
device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"

# Load the model
pipe = StableDiffusionPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V6.0_B1_noVAE",
    safety_checker=None,  # Optional
    torch_dtype=torch.float16 if device != "cpu" else torch.float32
).to(device)

# Read config
config_path = "data/config.txt"
num_characters = None

with open(config_path, "r") as f:
    for line in f:
        if line.strip().startswith("num_characters="):
            num_characters = int(line.strip().split("=")[1])
            break

if num_characters is None:
    raise ValueError("⚠️ 'num_characters' not found in config.txt")

# Read single prompt from file
with open("./data/base_prompts.txt", "r") as f:
    prompt = next((line.strip() for line in f if line.strip()), None)

if not prompt:
    raise ValueError("⚠️ No prompt found in base_prompts.txt")

# Output directory
os.makedirs("characters", exist_ok=True)

# Generate characters using same prompt but random seeds
used_seeds = set()

for idx in range(num_characters):
    # Ensure unique seed
    while True:
        seed = random.randint(0, 999999)
        if seed not in used_seeds:
            used_seeds.add(seed)
            break

    generator = torch.manual_seed(seed)
    image = pipe(prompt, generator=generator).images[0]
    filename = f"characters/character_{idx}_seed_{seed}.png"
    image.save(filename)
    print(f"✅ Character {idx} saved as {filename} with seed {seed}")
