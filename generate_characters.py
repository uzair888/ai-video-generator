import os
import torch
from diffusers import StableDiffusionPipeline

# Set device
device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"

# Load the model
pipe = StableDiffusionPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V6.0_B1_noVAE",
    torch_dtype=torch.float16 if device != "cpu" else torch.float32
).to(device)

# Read prompts from file
with open("character-prompts.txt", "r") as f:
    prompts = [line.strip() for line in f if line.strip()]

# Output directory
os.makedirs("characters", exist_ok=True)

# Generate one base character per prompt
for idx, prompt in enumerate(prompts):
    seed = 1000 + idx  # consistent seed for each character
    generator = torch.manual_seed(seed)

    image = pipe(prompt, generator=generator).images[0]
    filename = f"characters/character_{idx}_seed_{seed}.png"
    image.save(filename)
    print(f"✅ Character {idx} saved as {filename} with seed {seed}")
