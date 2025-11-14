## Server vLLM model
- connect to remote runpod machine
- run `pip install vllm`
- run below command
```terminaloutput
vllm serve "Qwen/Qwen3-VL-8B-Instruct" \
    --tensor-parallel-size 4 \
    --host 0.0.0.0 \
    --port 8000 \
    --max-model-len 16384 \
    --gpu-memory-utilization 0.95 \
    --trust-remote-code
```