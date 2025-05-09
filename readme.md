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

- 🧠 update /data/base_prompts.txt to update the prompt for character generation, make sure that this prompt stays same during variation generation aswell. The script will generate number of characters using that prompt.
- 🎭 update /data/config.txt with as many characters you want to generate.
- run python generate_characters.py to generate characters, the output will be saved iin characters folder.
```bash
python generate_characters.py
```
