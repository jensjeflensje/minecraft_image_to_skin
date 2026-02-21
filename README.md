# Minecraft Image to Skin

A web application that converts photos of people into Minecraft character skins using AI.

Upload a photo and the app will analyze it, extract physical characteristics, and generate a Minecraft skin that you can preview in 3D and download.

## How it works

1. **Upload** a photo of yourself (drag-and-drop, file picker, or paste)
2. **OpenAI Vision** analyzes the image and describes physical characteristics (hair, skin tone, clothing, etc.)
3. A **fine-tuned Stable Diffusion XL** model generates a Minecraft skin texture from that description
4. The skin is post-processed (scaled to 64x32, transparency restored) and presented as a **3D preview**
5. **Download** the skin as a PNG and use it in Minecraft

## Tech stack

- **Frontend** — Vue 3, TypeScript, Vite, Pinia, skin3d (3D preview)
- **Backend** — Django 5, Django REST Framework, Django-Q2 (async task queue)
- **AI/ML** — Hugging Face Diffusers (SDXL), PyTorch, OpenAI API
- **Infrastructure** — Docker Compose, Nginx, PostgreSQL, Redis, MinIO / S3

## Getting started

Copy the example environment file and fill in the required values:

```bash
cp .env.example .env
```

Start all services with Docker Compose:

```bash
docker compose up
```

The frontend will be available at `http://localhost:8080` (through the Nginx reverse proxy).

## Credits

The AI skin generation model is based on [minecraft-skin-generator](https://github.com/Monadical-SAS/minecraft_skin_generator) by [Monadical](https://github.com/Monadical-SAS). Their fine-tuned Stable Diffusion XL model (`monadical-labs/minecraft-skin-generator-sdxl`) powers the skin generation pipeline.
