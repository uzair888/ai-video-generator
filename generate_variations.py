import os
import re
import torch
from diffusers import StableDiffusionPipeline

# Set device
device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"

# Load model
pipe = StableDiffusionPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V6.0_B1_noVAE",
    torch_dtype=torch.float16 if device != "cpu" else torch.float32
).to(device)

# Load variation modifiers from file
with open("variations.txt", "r") as f:
    variations = [line.strip() for line in f if line.strip()]

# Map character IDs to prompts
prompt_map = {
    0: "A full-upper body photo of a man with dark hair, beard, and blue eyes, cinematic lighting",
    1: "A full-upper body photo of a woman with blonde hair and green eyes, 4K lighting indoors"
    # Extend as needed
}

# Output folder
os.makedirs("variations", exist_ok=True)

# Generate variations for characters in the "characters/" folder
for filename in os.listdir("characters"):
    match = re.match(r"character_(\d+)_seed_(\d+)\.png", filename)
    if not match:
        continue

    char_id = int(match.group(1))
    base_seed = int(match.group(2))
    base_prompt = prompt_map.get(char_id)

    if not base_prompt:
        print(f"❌ No prompt found for character {char_id}. Skipping.")
        continue

    print(f"🎨 Generating variations for Character {char_id}...")

    for i, modifier in enumerate(variations):
        full_prompt = f"{base_prompt}, {modifier}"
        seed = base_seed + i + 1  # variation seed based on base + offset
        generator = torch.manual_seed(seed)

        image = pipe(full_prompt, generator=generator).images[0]
        out_path = f"variations/character_{char_id}_variation_{i+1}_seed_{seed}.png"
        image.save(out_path)
        print(f"✅ Saved: {out_path}")
