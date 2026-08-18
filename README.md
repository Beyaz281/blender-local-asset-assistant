# 🐳 Dockerized RAG & LLM Based Blender AI Layout Assistant (v7.0)

<img width="1920" height="1080" alt="2026-07-27-17-16-25-pjj7dyzg_kVjORyEQ" src="https://github.com/user-attachments/assets/3c96d76e-09e5-4ab4-b21f-c13904ea01b6" />

### 🎥 Project Demo
https://youtu.be/7lmovybQdng

# AI-Powered 3D Production Pipeline: Dockerized RAG & LLM Asset Placement Agent (v7.0)

An advanced, microservice-driven production pipeline agent that bridges modern software engineering with 3D animation workflows. The system leverages Natural Language Processing (NLP), Retrieval-Augmented Generation (RAG), and Blender's Python API (`bpy`) to seamlessly parse complex artist queries and generate collision-free, production-ready 3D layouts.


## 📌 What's New in v7.0
The static coordinate bottlenecks have been completely eliminated. The architecture has been upgraded to a fully asynchronous, non-blocking, and collision-free pipeline framework designed for modern studio environments.

---

## 🏗️ System & Microservices Architecture

The system is decoupled into a loose, high-performance client-server infrastructure:

### 1. Backend Services (Containerized Infrastructure)
Runs isolated inside **Docker** containers to guarantee cross-platform scalability and zero deployment friction:
*   **FastAPI:** Acts as the high-throughput gateway layer, handling low-latency HTTP/JSON payloads transmitted from the Blender client.
*   **ChromaDB:** A dedicated vector database managing high-speed semantic asset search and metadata querying for local pipeline asset libraries.
*   **70B LLM Layer (Llama-3.3-70B-Versatile via Groq):** Orchestrates intent classification and linguistic dependencies. Instead of arbitrary coordinate guessing, it outputs validation-ready, deterministic JSON configurations that adhere strictly to pipeline rules.

### 2. Frontend / Client (Blender Native Integration)
Executes directly within the artist's digital content creation (DCC) environment:
*   **Asynchronous HTTP Client:** Dispatches payloads without halting artist workflows.
*   **Non-Blocking Scene Graph Execution:** Leverages `bpy.app.timers` to parse incoming JSON payloads concurrently in the background, updating the 3D viewport in real time without causing UI freezes or thread locks.

---

## 🔥 Key Technical Capabilities & Algorithms

*   **Universal Geometry Engine (Dynamic Bounding Boxes):** Zero dependency on hardcoded asset naming or pre-calculated static values. The pipeline programmatically measures the precise bounding box of imported geometry on-the-fly. This allows for complex stacking towers and horizontal alignment with dynamic row offsets and absolute zero mesh clipping.
*   **Universal Rotation Calibration Matrix:** Resolves inconsistent native asset orientations across internal source axes. Alignment is dynamically locked via a global calibration multiplier, ensuring characters, furniture, or props face the uniform cinematic direction automatically.
*   **Few-Shot Prompt Engineering:** Features fine-tuned operational prompts allowing the LLM to successfully break down complex, multi-object arrangements and nested dependencies into sequential transformation matrices.

---

## 🛠️ Tech Stack & Dependencies

*   **3D Core & Pipeline Client:** Python, Blender Python API (`bpy`), `bpy.app.timers`, Python Requests
*   **API & Backend Layer:** FastAPI, Uvicorn, Pydantic (v2)
*   **AI & Vector Middleware:** Groq SDK, ChromaDB
*   **DevOps & Infrastructure:** Docker, Docker Compose

---

## 📅 Roadmap & Project Milestones

*   [x] Containerize server components via Docker & Docker Compose
*   [x] Establish robust JSON communication interfaces between Blender and FastAPI
*   [x] Implement thread-safe, non-blocking scene injection using `bpy.app.timers`
*   [x] Deploy dynamic bounding box collision detection and orientation matrices
*   [x] **[In Progress]** Advanced RAG synchronization for continuous, deep scanning of local multi-format asset libraries

---

## 💻 Quick Start & Deployment Guide

### 1. Initialize the Backend Services
Ensure Docker and Docker Compose are installed on your workstation. Open a terminal in the root directory and spin up the microservices:

```bash
docker-compose up --build
```
The high-performance API gateway will initialize locally at `http://localhost:8000`.

### 2. Connect the Blender Add-on
1. Open your Blender workspace.
2. Navigate to the **Scripting** tab, open the client-side `v7.1` script engine, and click **Run Script**.
3. In the 3D Viewport, press `N` to toggle the side panel.
4. Locate the **AI Safe Measurement** suite to trigger, prompt, and test the real-time AI layout generation natively.

---
**Developer Links:** [LinkedIn](https://www.linkedin.com/in/beyza-özdemir-7aa303231) | **Email:** byz1707@gmail.com
