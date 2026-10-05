# AI Garden Buddy

AI Garden Buddy is a local-first gardening assistant built for the Hacktoberfest 2026 Open-Source AI Challenge: Week 1 — Touch Grass.

## What it does

- Creates a personalized beginner-friendly garden plan.
- Suggests plants based on region, season, space and sunlight.
- Generates practical outdoor tasks for the week.
- Creates short outdoor missions so the user spends less time on the screen.
- Uses an open-weight AI model locally through Ollama.
- Includes a fallback plan when the local model is unavailable.

## Open-source AI

The default model is **Qwen2.5 1.5B Instruct** running locally through **Ollama**. You can swap the model by setting `OLLAMA_MODEL` without changing the application code.

Because inference can run on the user's machine, garden details do not have to be sent to a closed hosted AI API.

## Run locally

### 1. Install Ollama

Install Ollama from https://ollama.com/ and start it.

### 2. Download the model

```bash
ollama pull qwen2.5:1.5b
```

You can use another compatible model later:

```bash
set OLLAMA_MODEL=your-model-name
```

On Linux/macOS:

```bash
export OLLAMA_MODEL=your-model-name
```

### 3. Create a Python environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the app

```bash
python app.py
```

Open:

http://localhost:5000

## Project structure

```text
ai-garden-buddy/
├── index.html
├── app.py
├── requirements.txt
└── README.md
```

## Challenge story

The idea is simple: AI should not become another reason to stare at a screen. Garden Buddy uses AI for the short planning step, then sends the user outside to plant, observe, water and grow.

## Safety note

Garden advice depends on local weather, soil, plant varieties and growing conditions. The app is an educational helper, not a substitute for local horticultural guidance. Always check local frost/heat conditions and the instructions for the plants you grow.
