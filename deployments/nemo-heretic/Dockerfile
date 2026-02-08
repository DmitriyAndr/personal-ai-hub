# Use the proven RunPod base image with PyTorch and CUDA 12.4
FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

# Set the working directory to the standard RunPod workspace
WORKDIR /workspace

# Install specific vLLM version and helper libraries
# hf_transfer: drastically speeds up model downloads
# requests: needed for API health checks
RUN pip install --no-cache-dir \
    vllm==0.15.1 \
    hf_transfer \
    requests \
    huggingface_hub

# --- Environment Variables ---

# Enable high-speed model downloads using hf_transfer
ENV HF_HUB_ENABLE_HF_TRANSFER=1

# Ensure Python logs (print statements) are sent directly to the console in real-time
ENV PYTHONUNBUFFERED=1

# Point HuggingFace cache to the persistent network volume
# This prevents re-downloading the 25GB+ model every time the pod starts
ENV HF_HOME="/workspace/huggingface-cache/hub"

# Copy the management script from your local project structure
# Ensure your local path 'services/main.py' matches your build context
COPY services/main.py /workspace/main.py

# Launch the Python manager as the entry point
ENTRYPOINT ["python3", "main.py"]
