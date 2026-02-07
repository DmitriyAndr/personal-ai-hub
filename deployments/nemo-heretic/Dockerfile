# Stable release with CUDA 13.0 support
FROM vllm/vllm-openai:v0.15.1-cu130

# Set working directory inside the container
WORKDIR /app

# Reset the entrypoint of the base vLLM image to allow custom commands
ENTRYPOINT []

# Copy the service wrapper from the project root
# Note: This requires setting the build context to the root directory
COPY services/main.py /app/main.py

# Set the environment variable for the specific model
ENV MODEL_NAME="DavidAU/Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus"

# Launch the service using the wrapper
CMD ["python3", "/app/main.py"]
