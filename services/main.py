import subprocess
import time
import sys
import os

def start_vllm():
    print("--- [HUB] Starting vLLM Server ---")
    
    # Параметры берем из переменных окружения или ставим дефолт
    model_name = os.getenv("MODEL_NAME", "mistralai/Mistral-Nemo-Base-2407")
    
    command = [
        "python3", "-m", "vllm.entrypoints.openai.api_server",
        "--model", model_name,
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    
    # Запускаем vLLM. stdout=None позволит логам лететь прямо в консоль RunPod
    return subprocess.Popen(command)

def main():
    print("--- [HUB] Personal AI Hub Wrapper Started ---")
    vllm_process = start_vllm()
    
    try:
        while True:
            # Проверяем жива ли нейронка
            status = vllm_process.poll()
            if status is not None:
                print(f"--- [HUB] vLLM process died with status {status}. Exiting... ---")
                sys.exit(status)
            
            # Место для будущего Watchdog
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("--- [HUB] Shutting down gracefully... ---")
        vllm_process.terminate()
        vllm_process.wait()

if __name__ == "__main__":
    main()
