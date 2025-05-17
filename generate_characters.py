import os
import torch
import random
import logging
from faker import Faker
from diffusers import StableDiffusionPipeline

def main():
    # ─── Setup Logging ─────────────────────────────────────────────────────────
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )
    log = logging.getLogger(__name__)

    # ─── Initialize Name Generator ────────────────────────────────────────────
    fake = Faker()

    # ─── Select Device ──────────────────────────────────────────────────────────
    device = "mps" if torch.backends.mps.is_available() \
             else "cuda" if torch.cuda.is_available() \
             else "cpu"
    log.info(f"Using device: {device}")

    # ─── Load the Model ─────────────────────────────────────────────────────────
    log.info("Loading StableDiffusionPipeline...")
    pipe = StableDiffusionPipeline.from_pretrained(
        "SG161222/Realistic_Vision_V6.0_B1_noVAE",
        safety_checker=None,
        torch_dtype=torch.float16 if device != "cpu" else torch.float32
    ).to(device)
    log.info("Model loaded successfully.")

    # ─── Read Configuration ────────────────────────────────────────────────────
    config_path = "data/config.txt"
    log.info(f"Reading config from '{config_path}'...")
    num_characters = None
    with open(config_path, "r") as f:
        for line in f:
            if line.strip().startswith("num_characters="):
                num_characters = int(line.strip().split("=")[1])
                break
    if num_characters is None:
        log.error("⚠️ 'num_characters' not found in config.txt")
        raise ValueError("'num_characters' not found in config.txt")
    log.info(f"Will generate {num_characters} characters.")

    # ─── Read Prompt ────────────────────────────────────────────────────────────
    prompts_path = "data/base_prompts.txt"
    log.info(f"Reading prompt from '{prompts_path}'...")
    with open(prompts_path, "r") as f:
        prompt = next((line.strip() for line in f if line.strip()), None)
    if not prompt:
        log.error("⚠️ No prompt found in base_prompts.txt")
        raise ValueError("No prompt found in base_prompts.txt")
    log.info(f"Base prompt: {prompt!r}")

    # ─── Prepare Output Directory ───────────────────────────────────────────────
    out_dir = "characters"
    os.makedirs(out_dir, exist_ok=True)
    log.info(f"Output directory is '{out_dir}/'")

    # ─── Generate Characters ────────────────────────────────────────────────────
    used_seeds = set()
    for idx in range(num_characters):
        # Unique seed
        while True:
            seed = random.randint(0, 999_999)
            if seed not in used_seeds:
                used_seeds.add(seed)
                break

        # Random name
        name = fake.first_name()
        safe_name = name.replace(" ", "_")

        # Personalized prompt
        personalized_prompt = f"{name}, {prompt}"
        log.info(f"[{idx+1}/{num_characters}] Generating '{name}' (seed={seed})")
        log.info(f"Prompt: {personalized_prompt!r}")

        # Generate & save
        torch.manual_seed(seed)
        generator = torch.Generator(device=device).manual_seed(seed)
        image = pipe(personalized_prompt, generator=generator).images[0]
        filename = f"{out_dir}/{safe_name}_seed{seed}.png"
        image.save(filename)
        log.info(f"✅ Saved '{filename}'")

    log.info("All characters generated successfully.")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Log the full exception traceback
        logging.getLogger(__name__).exception("❌ Unexpected error")
    finally:
        # Pause so you can read the logs before the window closes
        input("Press Enter to exit...")
