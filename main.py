import os
from moviepy.config import change_settings
from moviepy.editor import (
    VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips,
    AudioFileClip
)
from moviepy.video.fx.all import resize, crop
from moviepy.audio.fx.all import audio_loop
from moviepy.audio.AudioClip import CompositeAudioClip  # ✅ Corrected import
from gtts import gTTS

# === ImageMagick path for Windows ===
change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

# === Paths ===
video1_path = "videos/video-1.mp4"
video2_path = "videos/video-2.mp4"
caption_path = "caption.txt"
tts_audio_path = "tts.mp3"
music_path = "music/background.mp3"
output_path = "videos/combined_video.mp4"

# === Read caption text ===
with open(caption_path, 'r', encoding='utf-8') as f:
    caption_text = f.read().strip()

# === Generate TTS audio ===
tts = gTTS(caption_text)
tts.save(tts_audio_path)

# === Load video clips ===
video2 = VideoFileClip(video2_path)
video1 = VideoFileClip(video1_path).subclip(0, 4)

# Match dimensions and fps
# video1 = video1.resize(video2.size).set_fps(video2.fps)
video1 = video1.resize(height=video2.h)

# Crop or pad width to match video2 width
if video1.w > video2.w:
    # Crop horizontally (centered)
    extra_width = (video1.w - video2.w) // 2
    video1 = crop(video1, x1=extra_width, x2=video1.w - extra_width)
elif video1.w < video2.w:
    # Add black bars (padding) left and right
    from moviepy.video.fx.all import margin
    pad = (video2.w - video1.w) // 2
    video1 = margin(video1, left=pad, right=pad, color=(0, 0, 0))

# Match fps
video1 = video1.set_fps(video2.fps)

font_path = "D:/Projects/ai-video-generator-backend/app/OvercameDemoBold.ttf"
# "D:/Projects/ai-video-generator-backend/app/Roboto-Bold.ttf"
# === Add caption over first video ===
caption_clip = TextClip(caption_text,
                        fontsize=40,
                        color='white',
                        font=font_path,
                        method='caption',
                        size=(video1.w * 0.8, None),
                        align='center'
                    ).set_duration(video1.duration).set_position('center')

# === Add TTS audio to first video ===
tts_audio = AudioFileClip(tts_audio_path)
video1 = video1.set_audio(tts_audio)

# === Overlay caption on top of the first video ===
video1_with_caption = CompositeVideoClip([video1, caption_clip])

# === Combine both video parts ===
combined_video = concatenate_videoclips([video1_with_caption, video2])

# === Load and loop background music to match video duration ===
background_music = AudioFileClip(music_path)
background_music = audio_loop(background_music, duration=combined_video.duration).volumex(0.2)

# === Combine all audio: video narration + background music ===
final_audio = CompositeAudioClip([
    combined_video.audio,      # TTS and original audio
    background_music           # Background music
])

# === Attach final audio to video ===
final_video = combined_video.set_audio(final_audio)

# === Write the final output ===
final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# === Cleanup ===
tts_audio.close()
os.remove(tts_audio_path)
