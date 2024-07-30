from openllms.core import install_ollama_model

models = [
    "qwen2:0.5b",
    "deepseek-coder:1.3b-base-q4_0",
    "phi3",
    "llama3.1",
]
print(f"Installing {models}...")
print()

for model in models:
    print(f"Installing {model}...")
    install_ollama_model(model)

print("All models installed succesfully!")