# Use a base image with guaranteed support for RunPod drivers
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

# Install basic system dependencies
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Fix for "Error 803: system has unsupported display driver"
# This links the container to the host's CUDA compatibility libraries
RUN ldconfig /usr/local/cuda-12.4/compat/

# Upgrade pip and install vLLM (v0.6.3 is stable for CUDA 12.4)
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir vllm==0.6.3.post1 huggingface_hub

# Set the environment variable for model caching
# This ensures models are saved to the persistent volume if it's mounted
ENV HF_HOME="/runpod-volume/huggingface-cache/hub"

WORKDIR /app

# Copy the service code into the container
COPY services/main.py /app/main.py

# Launch the service
ENTRYPOINT ["python3", "/app/main.py"]
