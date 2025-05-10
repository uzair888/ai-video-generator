# 🔧 Custom Avatar Reel Generator

Generate personalized AI-driven avatar reels with facial animation, voiceovers, and background customization. Perfect for marketing, storytelling, and social media automation.

---

## 📍 Features

- 🎭 Full-body AI avatars with customizable appearance (face, outfit, pose)
- 🧠 AI voiceover generation with emotion control
- 🎬 Script-to-video pipeline
- 🌄 Background generation using prompt-based control
- 🕹️ Pose control with AnimateDiff or similar
- 📦 Bulk generation support for scalable content creation

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/uzair888/ai-video-generator.git
cd ai-video-generator
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### Usage

### Character generation

- 🧠 update /data/base_prompts.txt to update the prompt for character generation, make sure that this prompt stays same during variation generation aswell. The script will generate number of characters using that prompt.
- 🎭 update /data/config.txt with as many characters you want to generate.
- run python generate_characters.py to generate characters, the output will be saved in characters folder.

```bash
python generate_characters.py
```

### Variations generation

- 🌄 update /data/variations.txt to update the prompt for character generation, follow same structure.
- it will generate variations in variation folder.

```bash
python generate_variations.py
```

## generated AI reel

## 🔧 Custom Avatar Reel Generator

Generate personalized AI-driven avatar reels with facial animation, voiceovers, and background customization. Perfect for marketing, storytelling, and social media automation.

📍 Features

🌝 Full-body AI avatars with customizable appearance (face, outfit, pose)

🧠 AI voiceover generation with emotion control

🎬 Script-to-video pipeline

🌄 Background generation using prompt-based control

🔹 Pose control with AnimateDiff or similar

📦 Bulk generation support for scalable content creation

🚀 Getting Started

## 1. 📥 Clone the Repository

git clone https://github.com/uzair888/ai-video-generator.git
cd ai-video-generator

## 2. 🧪 Setup Virtual Environment

`python -m venv venv`
source venv/Scripts/activate # On Windows: venv\Scripts\activate

## 3. 📦 Install Dependencies

`pip install -r requirements.txt`

🔄 Usage

🌈 Character Generation

🧠 Update /data/base_prompts.txt to define the prompt for base character generation. This prompt should remain consistent during variation generation.

📄 Update /data/config.txt to define how many characters you want to generate.

▶️ Run the character generation script:

`python generate_characters.py`

📂 Output will be saved in the characters folder.

🎭 Variations Generation

🌄 Update /data/variations.txt with variation prompts following the defined format.

▶️ Run the variation script:

`python generate_variations.py`

📂 Output will be saved in the variations folder.

🎥 Reel Generation (generate_reel.py)

This script automates the full pipeline of generating an AI avatar video reel:

`python generate_reel.py`

It performs the following steps:

☁️ Uploads character image to Cloudinary

🖼️ Generates an AI video using RunwayML's image_to_video API with a corresponding prompt from data/video_prompt.txt

🔁 Polls RunwayML for video generation completion

📥 Downloads the generated video

🔊 Generates voiceover for the caption (from data/caption.txt) using Google TTS

📝 Adds caption overlay on top of the AI-generated video

🎞️ Selects a random sample video from /sample_videos to append after the AI video

🎶 Adds background music (randomly selected from /music) and mixes it with TTS

💾 Exports the final video to /output_videos

🔑 Configuration Notes

🔤 Fonts are loaded from /app/fonts/Roboto-Bold.ttf

⚙️ The script uses ImageMagick, make sure the binary path is correctly set

🔐 Cloudinary and RunwayML credentials are embedded in the script — replace with your own keys

📂 Folder Structure

.
├── app/
│ └── fonts/ # Custom font(s) used in videos
├── characters/ # Generated base characters
├── variations/ # Generated character variations
├── music/ # Background music tracks
├── sample_videos/ # Sample videos to be appended after AI content
├── output_videos/ # Final video output files
├── temp_videos/ # Temporary video downloads from Runway
├── data/
│ ├── caption.txt # Captions for each video
│ ├── config.txt # Character generation settings
│ ├── base_prompts.txt # Prompts for initial character generation
│ ├── variations.txt # Prompts for character variations
│ └── video_prompt.txt # Prompts to guide AI video generation

⚡ Example Workflow

👤 Generate character images with generate_characters.py

🌀 Generate multiple variation images using generate_variations.py

🎬 Create videos by combining AI clips, voiceover, captions, music, and sample clips using generate_reel.py

📄 Notes

⚠️ Ensure ImageMagick is installed and its path is correctly set in generate_reel.py

🔑 Make sure your RunwayML API key and Cloudinary credentials are properly configured

🖋️ Font used for captioning must exist on your system or be provided in fonts/

🚪 License

MIT License. Feel free to fork, modify, and use commercially.
