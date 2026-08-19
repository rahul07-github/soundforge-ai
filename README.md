# 🎵 SoundForge AI

### AI-Powered Text → Song → Video Generation Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![PyTorch](https://img.shields.io/badge/PyTorch-AI%2FML-EE4C2C)
![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

SoundForge AI converts a user's text prompt into lyrics and music, then transforms the generated song into a **cinematic music video** — using a curated image dataset, audio analysis, intelligent image selection, camera motion, transitions, color grading, and video processing.

The goal: go from a creative idea to a complete **song + visual video**, with no manual video editing.

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Project Objective](#-project-objective)
- [Team Responsibilities](#-team-responsibilities)
- [Project Structure](#️-project-structure)
- [How Text Becomes a Video](#-how-text-becomes-a-video)
- [AI / Intelligent Approaches](#-ai--intelligent-approaches)
- [Technology Stack](#️-technology-stack)
- [Hardware Requirements & Constraints](#-hardware-requirements--constraints)
- [Major Problems Faced](#-major-problems-faced)
- [Engineering Approach](#-engineering-approach)
- [Current Development Direction](#-current-development-direction)
- [Future Improvements](#-future-improvements)
- [Running the Project](#️-running-the-project)
- [What I Learned](#-what-i-learned)
- [My Contribution](#-my-contribution)
- [Project Status](#-project-status)
- [Contact](#-contact)

---

## 📌 Project Overview

```text
User Prompt
     │
     ▼
Lyrics Generation → Music/Song Generation → Generated Song
     │
     ▼
Audio Analysis (BPM, Beats, Duration, Energy)
     │
     ▼
Mood Detection → Category Selection → Image Dataset
     │
     ▼
Image Ranking → Image Mixing → Image Scheduling
     │
     ▼
Camera Motion (Zoom In/Out, Pan, Diagonal)
     │
     ▼
Color Grading → Depth/Parallax → Transitions
     │
     ▼
Silent Video Generation → Audio + Video Merge
     │
     ▼
Subtitle/Thumbnail Processing → Final MP4 Video
```

The core idea: synchronize the visual experience with the generated song, instead of producing a random image slideshow.

---

## 🎯 Project Objective

Turn a simple creative prompt into a complete multimedia experience.

**Example:**

```text
Prompt: "A peaceful romantic song about watching the sunset with someone you love."

  → Lyrics → Generated Song → Mood/Category Detection
  → Relevant Images → Audio/Beat Analysis → Image Scheduling
  → Camera Motion + Parallax + Transitions → Final Cinematic Video
```

---

## 👥 Team Responsibilities

### 🎼 Fahim — Lyrics & Music Generation
- Processes the user's creative prompt
- Generates lyrics and music/song audio
- Provides the generated song to the video pipeline

### 🎬 Rahul — Video Processing & Generation *(my role)*
- Audio analysis integration, beat/BPM-based timing
- Image dataset processing, ranking, mixing, scheduling
- Camera motion, cinematic effects, color grading
- Depth/parallax effects, transitions
- Video rendering, FFmpeg integration
- Audio/video sync, subtitle + thumbnail generation
- Pipeline debugging and improvement

**Objective of my module:** make the output feel like a cinematic music video — not a slideshow.

### ⚙️ Backend / Core Team
Connects services and exposes the generation pipeline through the API layer:
`Prompt → Lyrics/Music → Video Generation → Storage → Final Output`

---

## 🏗️ Project Structure

```text
soundforge-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   │
│   │   ├── services/
│   │   │   ├── lyrics/
│   │   │   ├── music/
│   │   │   └── video/
│   │   │       ├── audio_merger.py
│   │   │       ├── audio_trimmer.py
│   │   │       ├── beat_detector.py
│   │   │       ├── category_selector.py
│   │   │       ├── cinematic_effects.py
│   │   │       ├── dataset_loader.py
│   │   │       ├── frame_generator.py
│   │   │       ├── image_mixer.py
│   │   │       ├── image_processor.py
│   │   │       ├── image_ranker.py
│   │   │       ├── image_scheduler.py
│   │   │       ├── mood_detector.py
│   │   │       ├── pipeline.py
│   │   │       ├── prompt_builder.py
│   │   │       ├── scene_loader.py
│   │   │       ├── scene_planner.py
│   │   │       ├── subtitle_burner.py
│   │   │       ├── subtitle_generator.py
│   │   │       ├── thumbnail_generator.py
│   │   │       ├── video_export.py
│   │   │       └── video_generator.py
│   │   │
│   │   └── storage/
│   │       ├── datasets/
│   │       └── generated/
│   │           ├── assets/ ├── covers/ ├── lyrics/ ├── metadata/
│   │           ├── preview/ ├── songs/ ├── subtitles/
│   │           ├── thumbnails/ └── videos/
│   │
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## 🎬 How Text Becomes a Video

**Step 1 — User Prompt:** `"Create a peaceful song about mountains and sunset."`

**Step 2 — Lyrics and Music:** Prompt → Lyrics → Generated Song

**Step 3 — Audio Analysis:**
```text
Song Duration: 20 seconds
BPM: 156.61
Detected Beats: 0.17, 0.55, 0.94, 1.32, 1.70, 2.10 ...
```

**Step 4 — Mood and Category Selection:**
```text
Mood: nature
Categories: nature, forest, mountains, sunset
```

**Step 5 — Image Selection:** current prototype uses a manually collected, organized image dataset, ranked with quality metrics + CLIP-based semantic similarity.

```text
datasets/Images/
├── nature/ ├── forest/ ├── mountains/ ├── sunset/
├── romantic/ ├── sad/ └── lofi/
```

**Step 6 — Scene Scheduling:** each selected image gets scene metadata:
```python
{
    "image_path": "...",
    "motion": "zoom_in",
    "transition": "crossfade",
    "energy": "medium",
    "zoom": 1.08,
    "brightness": 1.02,
    "contrast": 1.05
}
```

**Step 7 — Cinematic Processing:** resizing/cropping, camera motion, color grading, transitions, depth/parallax.

**Step 8 — Video and Audio Merge:** `Processed Visual Scenes + Generated Song → Final MP4`

---

## 🧠 AI / Intelligent Approaches

| Technique | Purpose |
|---|---|
| Audio Intelligence | BPM detection, beat detection, audio/scene timing |
| Semantic Image Matching | CLIP-based ranking — how well an image matches the prompt/context |
| Depth Estimation | Spatial movement and parallax effects (in progress) |
| Rule-Based Visual Scheduling | Decides image order, motion, transitions, energy pacing |
| Classical Computer Vision (OpenCV) | Reading, resizing, cropping, sharpness/brightness/contrast analysis |

SoundForge AI combines AI models, classical CV, audio analysis, and rule-based scheduling — rather than relying on a single model.

---

## 🛠️ Technology Stack

| Area | Technologies |
|---|---|
| Language | Python 3.11 |
| Backend | FastAPI, Uvicorn |
| Audio | Librosa, Pydub, FFmpeg |
| Computer Vision | OpenCV, NumPy, Pillow |
| AI / ML | PyTorch, TorchVision, timm, OpenCLIP |
| Video | FFmpeg, MoviePy, OpenCV |
| Development | VS Code, Git, GitHub, Python Virtual Environment |

---

## 💻 Hardware Requirements & Constraints

Development and testing were done on consumer-grade hardware, which directly shaped some engineering decisions:

- **GPU:** RTX 2050, 4GB VRAM
- **Free storage:** ~8GB during development

**Impact:** heavier compute stages (advanced depth models, larger batch rendering) had to be scoped down or deferred rather than run at full quality. This is a known, intentional trade-off — not an oversight — and is documented here so the design choices below make sense in context.

---

## 🚧 Major Problems Faced

**1. Beat Detection** — audio decoding was unreliable at first (`PySoundFile failed`, `NoBackendError()`). Fixed by ensuring MP3 files were correctly decoded before beat analysis.

**2. FFmpeg Integration** — used for trimming, conversion, merging, encoding, export. Incorrect paths/codecs/formats caused pipeline failures; required careful path and codec handling.

**3. Image Processing** — dataset images vary in aspect ratio, resolution, orientation, and color. Needed portrait/landscape handling, resizing, cropping, and consistent formatting.

**4. Metadata Mismatch** — pipeline stages depend on shared metadata (`motion`, `transition`, `zoom`, `brightness`, `contrast`, `duration`, `start_time`, `end_time`). Missing fields could break later stages, so safer access patterns were introduced:
```python
item.get("contrast", 1.05)
```

**5. Making Static Images Feel Like Video** — basic image + audio looked like a slideshow. Extended pipeline: `Static Image → Camera Motion → Color Grading → Transitions → Depth Estimation → Parallax → Audio Sync`

**6. Image Repetition** — pure random selection repeated visuals too often. The image mixer/scheduler was redesigned to reduce repetition and add variety.

---

## 💡 Engineering Approach

Instead of one large end-to-end model, SoundForge AI uses a **modular pipeline**:

```text
Audio Analysis → Visual Understanding → Image Selection
→ Scene Planning → Image Processing → Motion → Depth → Video Rendering
```

This makes each component easier to debug, test, improve, replace, and scale independently.

---

## 📈 Current Development Direction

**✅ Implemented:** audio analysis, beat detection, mood-based categories, curated datasets, image ranking (incl. CLIP-based), image mixing, scene scheduling, camera motion, color grading, transitions, audio/video merging, subtitle processing, thumbnail generation.

**🔄 Ongoing:** better depth estimation, more realistic parallax, better beat-synced transitions, improved scene planning and semantic selection, more natural camera movement, better visual continuity.

---

## 🔮 Future Improvements

- AI-generated image sequences / AI image-to-video generation
- Better depth-aware camera movement
- Character/object consistency across scenes
- Scene-to-scene semantic continuity
- Automatic shot planning
- Advanced audio-visual synchronization
- GPU-optimized inference / cloud-based inference for larger models
- Higher-quality video generation

---

## ▶️ Running the Project

```powershell
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the environment
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the FastAPI application
python -m uvicorn backend.app.main:app --reload
```

API documentation is available through the FastAPI Swagger UI once running.

**Recommended minimum hardware:** NVIDIA GPU with 4GB+ VRAM (project developed and tested on RTX 2050 4GB); CPU-only mode works but is significantly slower for depth/parallax stages.

---

## 📚 What I Learned

Working on the video-generation component gave me hands-on experience with Python backend development, FastAPI, audio processing, beat detection, computer vision, CLIP-based semantic matching, AI model integration, depth estimation, video processing, FFmpeg, API integration, pipeline architecture, debugging, and Git/GitHub collaboration.

The biggest lesson: building an AI media-generation system isn't just about the model. Final quality depends heavily on **data preparation, timing, preprocessing, model selection, post-processing, and integration across components.**

---

## 👨‍💻 My Contribution

**Rahul — Video Processing & AI Video Pipeline**

I converted the generated song into a visual video experience by connecting it with a manually curated image dataset through this pipeline:

```text
Generated Song → Audio Analysis → Beat/BPM Detection → Mood/Category Info
→ Image Dataset → Image Ranking → Image Mixing → Scene Scheduling
→ Camera Motion → Color Grading → Depth/Parallax → Transitions
→ Video Rendering → Audio Merge → Final Video
```

Focus: make the output dynamic and cinematic, not a simple sequence of static images.

---

## 📌 Project Status

**Status: Active Development**

Working end-to-end prototype for converting generated songs and curated visual assets into videos. Actively improving: realistic motion, depth, parallax, scene continuity, beat synchronization, semantic image selection, and overall cinematic quality — within the current hardware constraints noted above.

---

## 📞 Contact

**Rahul** — Data Engineer | ML Engineer
GitHub: [rahul07-github](https://github.com/rahul07-github)

For questions, collaboration, or discussion about this project, feel free to reach out through GitHub.

---

### Repository Description
> SoundForge AI is a modular text-to-song-to-video generation platform that combines lyrics/music generation, audio analysis, semantic image selection, cinematic motion, depth/parallax effects, and automated video rendering.

### Recommended Repository Topics
```text
python artificial-intelligence machine-learning computer-vision
audio-processing video-generation fastapi pytorch opencv ffmpeg
clip deep-learning generative-ai music-generation ai-video
```
