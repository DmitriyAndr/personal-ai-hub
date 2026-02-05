import subprocess
import time
import sys
import os

def start_vllm():
    # Use environment variable or fallback to the Heretic model we chose
    model_name = os.getenv("MODEL_NAME", "DavidAU/Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus")
    
    print(f"--- [HUB] Starting vLLM Server with model: {model_name} ---")
    
    # Launch vLLM as an OpenAI-compatible API server
    command = [
        "python3", "-m", "vllm.entrypoints.openai.api_server",
        "--model", model_name,
        "--host", "0.0.0.0",
        "--port", "8000",
        "--max-model-len", "32768" # Set reasonable context window to save VRAM
    ]
    
    # Let logs stream directly to the RunPod console
    return subprocess.Popen(command)

def main():
    print("--- [HUB] Personal AI Hub Wrapper Started ---")
    vllm_process = start_vllm()
    
    try:
        while True:
            # Check if the vLLM process is still running
            status = vllm_process.poll()
            if status is not None:
                print(f"--- [HUB] vLLM process died with status {status}. Exiting... ---")
                sys.exit(status)
            
            # Placeholder for future watchdog/telemetry logic
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("--- [HUB] Shutting down gracefully... ---")
        vllm_process.terminate()
        vllm_process.wait()

if __name__ == "__main__":
    main()
