import os
import re
import torch
from diffusers import StableDiffusionPipeline

# Set device
device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"

# Load model
pipe = StableDiffusionPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V6.0_B1_noVAE",
    safety_checker=None,
    torch_dtype=torch.float16 if device != "cpu" else torch.float32
).to(device)

# Load base prompt
with open("data/base_prompts.txt", "r") as f:
    base_prompt = next((line.strip() for line in f if line.strip()), None)

if not base_prompt:
    raise ValueError("⚠️ No base prompt found in base_prompts.txt")

# Load variation modifiers
with open("data/variations.txt", "r") as f:
    variations = [line.strip() for line in f if line.strip()]

# Output folder
os.makedirs("variations", exist_ok=True)

# Generate variations
for filename in os.listdir("characters"):
    match = re.match(r"character_(\d+)_seed_(\d+)\.png", filename)
    if not match:
        continue

    char_id = int(match.group(1))
    base_seed = int(match.group(2))

    print(f"🎨 Generating variations for Character {char_id} (base seed {base_seed})")

    for i, modifier in enumerate(variations):
        identity_tag = "zk-person"
        anchored_prompt = base_prompt.replace("woman", f"woman named {identity_tag}")
        full_prompt = f"{anchored_prompt}, {modifier}"

        # Use the same base seed for all variations
        generator = torch.manual_seed(base_seed)

        image = pipe(full_prompt, generator=generator).images[0]
        out_path = f"variations/character_{char_id}_variation_{i+1}_seed_{base_seed}.png"
        image.save(out_path)
        print(f"✅ Saved: {out_path}")
