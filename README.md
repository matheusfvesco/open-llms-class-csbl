
<div align=center>
  <img src="assets/logo.jpeg" width=200 >
</div>

# Leveraging Open LLMs Locally class 2024

Companion code for the Open LLMs class

It includes:
1. Instructions on how to get an ollama instance up and running
2. Code for a basic chatbot demo with history, and agentic capabilities

## Syllabus

1. Setting up a basic ollama instance for local inference
1.1 Setting up both ollama and open-webui (quick start)
1.2 Open-webui demonstration and basic settings
1.3 Ollama API and OpenAI compatibility
2. Demonstration
2.1 Demonstration of code completion model
2.2 Demonstration of Continue.dev
2.3 Demonstration of function calling

## Ollama/OpenWebUi Setup

1. Setup Docker and docker compose on your system
2. Clone open-webui repository locally

```bash
git clone https://github.com/open-webui/open-webui.git && cd open-webui
```

3. Run the docker compose

3.1. Making Ollama API visible (RECOMMENDED)

```
docker compose -f docker-compose.yaml -f docker-compose.api.yaml up -d --build
```

3.2. Or with both GPU support and Ollama API visible:

```
docker compose -f docker-compose.yaml -f docker-compose.api.yaml -f docker-compose.gpu.yaml up -d --build
```
> NOTE: For GPU support, you need to have both CUDA Toolkit and Nvidia Container Runtime setup

> NOTE 2: Ommit the --build from the commands if you want to run a prebuild container for open-webui

## Usage

If the setup worked, you should be able to access the ollama API on http://localhost:11434, and a ChatGPT like interface on http://localhost:3000

You can use the webinterface, or use the openai compatible API. For the OpenAI compatible API, use http://localhost:11434/v1/ as the base URL.

## Setup for class

1. Open the repository inside a devcontainer
2. Follow the basic setup provided earlier to get ollama and openwebui up and running
3. run `poetry install` and then `poetry shell`, or use the requirements.txt
4. run `python background_install_models.py` to download models (this should take some time)
5. run `./quick_start_terrarium.sh` on a terminal

(optional)
6. After the class, run `cleanup.sh` to reutilize the same devcontainer

Quick start:

```
chmod +x quick_start_terrarium.sh && ./quick_start_terrarium.sh
```

```
poetry install && poetry shell; python background_install_models.py
```

## Usage for class

1. Use `python main.py` to run a quick demo of the openai compatibility layer of ollama, along with llama3.1 function calling capabilities