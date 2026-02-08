import os
import subprocess
import sys
from huggingface_hub import snapshot_download

def download_model(model_name):
    """
    Check if the model is present in the HF_HOME cache and download if necessary.
    Uses hf_transfer for high-speed downloads if enabled in Docker.
    """
    print(f"--- Starting model check/download for: {model_name} ---")
    try:
        # snapshot_download respects the HF_HOME env var set in Dockerfile
        snapshot_download(
            repo_id=model_name,
            allow_patterns=["*.json", "*.safetensors", "*.model", "*.txt"],
            ignore_patterns=["*.bin", "*.pth"]
        )
        print("--- Model is ready! ---")
    except Exception as e:
        print(f"Error downloading model: {e}")
        sys.exit(1)

def start_vllm_server(model_name):
    """
    Launch the vLLM OpenAI-compatible API server.
    Explicitly uses the official Mistral-Nemo tokenizer to ensure correct Russian output.
    """
    print(f"--- Launching vLLM OpenAI Server: {model_name} ---")
    
    # We use the official tokenizer to fix the 'rasterization' and language glitches
    command = [
        "python3", "-m", "vllm.entrypoints.openai.api_server",
        "--model", model_name,
        "--tokenizer", "mistralai/Mistral-Nemo-Instruct-2407",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--max-model-len", "32768",
        "--gpu-memory-utilization", "0.90",
        "--disable-log-requests"
        # --enforce-eager is removed for better performance (CUDA Graphs enabled)
    ]
    
    try:
        # Use subprocess.run to keep the process alive as the main entrypoint
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"vLLM server exited with error: {e}")
    except KeyboardInterrupt:
        print("Shutting down server...")

if __name__ == "__main__":
    # Get model name from ENV or use the default Heretic model
    model = os.getenv("MODEL_NAME", "DavidAU/Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus")
    
    # Ensure model weights are available in the persistent volume
    download_model(model)
    
    # Start the engine
    start_vllm_server(model)
