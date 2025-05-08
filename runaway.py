import cloudinary
import cloudinary.uploader
import os
import requests
import time
import random

# ✅ Cloudinary Configuration
cloudinary.config(
    cloud_name="dlyupes6z",      # Replace with your Cloudinary cloud name
    api_key="854827938715293",   # Replace with your Cloudinary API key
    api_secret="6JmlVENJEPAIChU6SNKmF_tQeu8"  # Replace with your Cloudinary API secret
)

# ✅ Video API Config
api_key = "key_8f99687f9fd488fe08af6a9014afde9adc670c4daf865ce569056b4e2c2dfb17d2777cb25866395e24da1eb907ca9b4f1e65c95fc0307611674b71e066c30aa0"
api_version = "2024-09-13"
headers = {
    "Authorization": f"Bearer {api_key}",
    "X-Runway-Version": api_version,
    "Content-Type": "application/json",
}

def upload_to_cloudinary(image_path):
    try:
        upload_result = cloudinary.uploader.upload(image_path, folder="character")
        print(f"☁️ Uploaded: {image_path} -> {upload_result['secure_url']}")
        return upload_result['secure_url']
    except Exception as e:
        print(f"❌ Failed to upload {image_path}: {e}")
        return None

def create_video_task(image_url):
    payload = {
        "promptImage": image_url,
        "seed": random.randint(0, 999999999),
        "model": "gen3a_turbo",
        "promptText": "The bunny is eating a carrot",
        "watermark": False,
        "duration": 5,
        "ratio": "16:9"
    }
    response = requests.post(
        "https://api.dev.runwayml.com/v1/image_to_video",
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        print("❌ Failed to create task:", response.text)
        return None

    task_id = response.json()["id"]
    print("✅ Task ID:", task_id)
    return task_id

def poll_for_completion(task_id):
    while True:
        response = requests.get(
            f"https://api.dev.runwayml.com/v1/tasks/{task_id}",
            headers=headers
        )
        if response.status_code != 200:
            print("❌ Failed to get status:", response.text)
            return None

        result = response.json()
        status = result.get("status")

        print("⏳ Status:", status)

        if status == "SUCCEEDED":
            video_url = result["output"][0]
            print("🎬 Video URL:", video_url)
            return video_url
        elif status == "FAILED":
            print("❌ Video generation failed")
            return None
        else:
            time.sleep(5)

def generate_one_video():
    character_folder = os.path.join(os.path.dirname(__file__), "characters")

    if not os.path.exists(character_folder):
        print("❌ 'characters' folder not found!")
        return

    files = [f for f in os.listdir(character_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

    if not files:
        print("❌ No image files found in the 'characters' folder.")
        return

    # ✅ Just pick the first image
    first_image = files[0]
    image_path = os.path.join(character_folder, first_image)
    image_url = upload_to_cloudinary(image_path)

    if image_url:
        task_id = create_video_task(image_url)
        if task_id:
            poll_for_completion(task_id)

# ✅ Commented out multi-image loop
# def generate_videos_from_folder():
#     character_folder = os.path.join(os.path.dirname(__file__), "characters")
#     if not os.path.exists(character_folder):
#         print("❌ 'characters' folder not found!")
#         return
#     for filename in os.listdir(character_folder):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
#             image_path = os.path.join(character_folder, filename)
#             image_url = upload_to_cloudinary(image_path)
#             if image_url:
#                 task_id = create_video_task(image_url)
#                 if task_id:
#                     poll_for_completion(task_id)

# ✅ Run the single image function
if __name__ == "__main__":
    generate_one_video()
