# Personal AI Hub

A private ecosystem designed to manage and orchestrate custom ML models on remote GPU resources.

## Project Goal
To provide a unified interface for triggering and interacting with private AI models while minimizing cloud costs through dynamic instance management.

## Key Principles
- **Provider Agnostic**: Abstract interfaces for switching between cloud providers (RunPod, Modal, etc.).
- **On-Demand Execution**: Resources are active only during active sessions.
- **Client Agnostic**: Interaction via standard OpenAI-compatible API, accessible from any device.

## Technology Stack
- **Backend**: Python (FastAPI / vLLM).
- **Architecture**: Provider-Consumer pattern with automated lifecycle management.
