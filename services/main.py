import os
import subprocess
import sys
from huggingface_hub import snapshot_download

def download_model(model_name):
    """
    Check if the model is present and download it if necessary.
    This prevents vLLM from failing during initial loading.
    """
    print(f"--- Starting model check/download for: {model_name} ---")
    try:
        # Download only necessary files. 
        # snapshot_download automatically checks the cache first.
        snapshot_download(
            repo_id=model_name,
            allow_patterns=["*.json", "*.safetensors", "*.model", "*.txt"],
            ignore_patterns=["*.bin", "*.pth"] # Prefer safetensors
        )
        print("--- Model is ready! ---")
    except Exception as e:
        print(f"Error downloading model: {e}")
        sys.exit(1)

def start_vllm_server(model_name):
    """
    Launch the vLLM OpenAI-compatible API server as a subprocess.
    """
    print(f"--- Launching vLLM OpenAI Server: {model_name} ---")
    
    command = [
        "python3", "-m", "vllm.entrypoints.openai.api_server",
        "--model", model_name,
        "--host", "0.0.0.0",
        "--port", "8000",
        "--max-model-len", "32768", # Adjust based on your GPU VRAM
        "--disable-log-requests"
    ]
    
    # Run the server and stream logs to the console
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"vLLM server exited with error: {e}")
    except KeyboardInterrupt:
        print("Shutting down server...")

if __name__ == "__main__":
    # Get the model name from environment variables
    model = os.getenv("MODEL_NAME", "DavidAU/Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus")
    
    # Step 1: Ensure model is available
    download_model(model)
    
    # Step 2: Start the server
    start_vllm_server(model)
