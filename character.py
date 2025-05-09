import random
import torch
from diffusers import StableDiffusionPipeline

# Set device based on availability
device = "mps" if torch.backends.mps.is_available() else "cpu"

# Load the pipeline
pipe = StableDiffusionPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V6.0_B1_noVAE",
    torch_dtype=torch.float16 if device != "cpu" else torch.float32
).to(device)

# Base prompt for a consistent character (Character 1)
base_prompt_1 = (
    "A full-upper body photo of a man sitting, "
    "highly detailed face, realistic skin texture, 4K, indoors, cinematic lighting, "
    "with dark hair, blue eyes, and a beard"
)

# Base prompt for a second character (Character 2)
base_prompt_2 = (
    "A full-upper body photo of a woman sitting, "
    "highly detailed face, realistic skin texture, 4K, indoors, cinematic lighting, "
    "with long blonde hair, green eyes, and wearing makeup"
)

# Function to generate variations for a given character
def generate_variations(character_prompt, character_number):
    for i in range(5):  # Generate 5 variations for each character
        # Use a fixed seed for consistency across generations for each character
        seed = 123456 + i  # Adjust seed slightly for each variation
        generator = torch.manual_seed(seed)

        # List of possible variations for expressions, lighting, etc.
        variations = [
            "smiling",
            "serious expression",
            "wearing glasses",
            "in casual clothing",
            "under soft lighting"
        ]
        
        # Add variation to the base prompt
        variation_prompt = character_prompt + ", " + variations[i]
        
        # Generate the image
        image = pipe(variation_prompt, generator=generator).images[0]
        image.save(f"generated_character_{character_number}_variation_{i}.png")
        print(f"Character {character_number} - Variation {i+1} generated with seed {seed}")

# Generate variations for both characters
generate_variations(base_prompt_1, 1)  # Character 1
generate_variations(base_prompt_2, 2)  # Character 2
