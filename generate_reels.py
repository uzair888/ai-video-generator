import cloudinary
import cloudinary.uploader
import os
import requests
import time
import random
from gtts import gTTS
from moviepy.config import change_settings
from moviepy.editor import (
    VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip,
    concatenate_videoclips
)
from moviepy.audio.fx.all import audio_loop
from moviepy.audio.AudioClip import CompositeAudioClip

# ✅ Cloudinary Config
cloudinary.config(
    cloud_name="dlyupes6z",
    api_key="854827938715293",
    api_secret="6JmlVENJEPAIChU6SNKmF_tQeu8"
)

# ✅ Runway API Config
api_key = "key_8f99687f9fd488fe08af6a9014afde9adc670c4daf865ce569056b4e2c2dfb17d2777cb25866395e24da1eb907ca9b4f1e65c95fc0307611674b71e066c30aa0"
api_version = "2024-09-13"
headers = {
    "Authorization": f"Bearer {api_key}",
    "X-Runway-Version": api_version,
    "Content-Type": "application/json",
}

# ✅ ImageMagick path
change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

# ✅ Paths
base_dir = os.path.dirname(__file__)
characters_folder = os.path.join(base_dir, "variations")
captions_folder = os.path.join(base_dir, "data", "caption.txt")
prompts_file = os.path.join(base_dir, "data", "video_prompt.txt")
music_folder = os.path.join(base_dir, "music")
sample_video_folder = os.path.join(base_dir, "sample_videos")
videos_folder = os.path.join(base_dir, "output_videos")
font_path = "D:/Projects/ai-video-generator-backend/app/fonts/Roboto-Bold.ttf"
os.makedirs(videos_folder, exist_ok=True)

def get_random_or_single_file(file_list):
    return file_list[0] if len(file_list) == 1 else random.choice(file_list)

def read_lines(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def upload_to_cloudinary(image_path):
    try:
        upload_result = cloudinary.uploader.upload(image_path, folder="character")
        print(f"☁️ Uploaded: {image_path} -> {upload_result['secure_url']}")
        return upload_result['secure_url']
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

def create_video_task(image_url, prompt):
    payload = {
        "promptImage": image_url,
        "seed": random.randint(0, 999999999),
        "model": "gen3a_turbo",
        "promptText": prompt,
        "watermark": False,
        "duration": 5,
        "ratio": "9:16"
    }
    response = requests.post(
        "https://api.dev.runwayml.com/v1/image_to_video",
        json=payload,
        headers=headers
    )
    if response.status_code != 200:
        print("❌ Task creation failed:", response.text)
        return None
    return response.json()["id"]

def poll_for_completion(task_id):
    while True:
        response = requests.get(
            f"https://api.dev.runwayml.com/v1/tasks/{task_id}",
            headers=headers
        )
        if response.status_code != 200:
            print("❌ Polling failed:", response.text)
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
        time.sleep(5)

def download_video(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("📥 Downloaded video to", filename)
        return filename
    else:
        print("❌ Failed to download video:", response.status_code)
        return None

def create_combined_video(raw_video_path, caption_text, music_file, sample_video_folder, index):
    tts_path = f"tts_{index}.mp3"
    tts = gTTS(caption_text)
    tts.save(tts_path)

    ai_clip = VideoFileClip(raw_video_path)

    caption = TextClip(
        caption_text,
        fontsize=40,
        color='white',
        font=font_path,
        method='caption',
        size=(ai_clip.w * 0.8, None),
        align='center'
    ).set_duration(ai_clip.duration).set_position('center')

    captioned_ai_clip = CompositeVideoClip([ai_clip, caption])

    sample_files = [
        os.path.join(sample_video_folder, f)
        for f in os.listdir(sample_video_folder)
        if f.lower().endswith(('.mp4', '.mov'))
    ]
    if not sample_files:
        print("❌ No sample video found.")
        return

    sample_clip = VideoFileClip(get_random_or_single_file(sample_files)).resize(ai_clip.size)

    # ✅ Reverse order: AI video first, sample video after
    final_clip = concatenate_videoclips([captioned_ai_clip, sample_clip])

    bg_music = AudioFileClip(music_file)
    bg_music = audio_loop(bg_music, duration=final_clip.duration).volumex(0.2)

    tts_audio = AudioFileClip(tts_path).set_start(0)  # starts with AI clip

    final_audio = CompositeAudioClip([bg_music, tts_audio])
    final_clip = final_clip.set_audio(final_audio)

    output_path = os.path.join(videos_folder, f"final_video_{index+1}.mp4")
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"✅ Saved final video: {output_path}")

    # Cleanup
    ai_clip.close()
    sample_clip.close()
    final_clip.close()
    bg_music.close()
    tts_audio.close()
    os.remove(tts_path)

def main():
    image_files = [
        f for f in os.listdir(characters_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
    ]
    if not image_files:
        print("❌ No images found.")
        return

    music_files = [
        os.path.join(music_folder, f)
        for f in os.listdir(music_folder)
        if f.lower().endswith(('.mp3', '.wav'))
    ]
    if not music_files:
        print("❌ No music files found.")
        return

    captions = read_lines(captions_folder)
    prompts = read_lines(prompts_file)

    for idx, image_name in enumerate(image_files):
        print(f"\n--- Processing {image_name} ---")
        image_path = os.path.join(characters_folder, image_name)
        image_url = upload_to_cloudinary(image_path)
        if not image_url:
            continue

        caption = captions[idx] if idx < len(captions) else "Default caption"
        prompt = prompts[idx] if idx < len(prompts) else "Default prompt"
        music_file = get_random_or_single_file(music_files)

        task_id = create_video_task(image_url, prompt)
        if not task_id:
            continue

        video_url = poll_for_completion(task_id)
        if not video_url:
            continue

        temp_videos_folder = os.path.join(base_dir, "temp_videos")
        os.makedirs(temp_videos_folder, exist_ok=True)
        raw_video_path = os.path.join(temp_videos_folder, f"video_{idx+1}.mp4")

        if download_video(video_url, raw_video_path):
            create_combined_video(raw_video_path, caption, music_file, sample_video_folder, idx)

if __name__ == "__main__":
    main()
