from dotenv import load_dotenv
from openai import OpenAI
from openllms.core import install_ollama_model, uninstall_ollama_model
from openllms.toolbelt import Toolset
import os
load_dotenv()

temperature = 0.0
system_prompt = "You are a helpful assistant. You should not lie to the user in any hypothesis."

client = OpenAI(base_url=os.environ["OPENAI_BASE_URL"])

print("Available models:")
models = client.models.list()
model_ids = [model.id for model in models]
for model_id in model_ids:
    print(model_id)
print()

model = input("Select the model: ")
if ":" not in model:
    model = model + ":latest"

if model not in model_ids:
    print(f"Model {model} not available locally, attempting to download it...")
    result = install_ollama_model(model)
    if result:
        print("Success!")
    else:
        print("Download failed...")
        exit()

allow_tools = input("Do you want to enable tool calling (mistral or llama3.1)? (y/n): ")
allow_tools = True if allow_tools == "y" else False
tools = []
if allow_tools:
    toolset = Toolset()
    tools = toolset.tools

default_system = {"role": "system", "content": system_prompt}
history = [default_system]
while True:
    prompt = input("Type your message (or q to quit, clear(), or history()): ")
    print()
    if prompt == "q":
        exit()
    if prompt == "clear()":
        history = [default_system]
        print("History cleared!\n\n\n")
        continue
    if prompt == "history()":
        print("Message history:")
        for message in history:
            print(message)
        print()
        continue
    history.append({"role": "user", "content": prompt})
    if tools:
        response = client.chat.completions.create(messages=history, model=model, temperature=temperature, tools=tools)
        tool_calls = [tool_call.function for tool_call in response.choices[0].message.tool_calls] if response.choices[0].message.tool_calls else []
        print(f"Model called tools '{tool_calls}'")
        print()
        history.append({"role": "assistant", "content": f"Said: '{response.choices[0].message.content}' | Called tools: '{tool_calls}'"})
        results = toolset.handle_message(response=response)
        history.append({"role": "system", "content": f"Results of the tool calls: {results} \n Now reply to the user."})
        history.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(messages=history, model=model, temperature=temperature)
        response_text = response.choices[0].message.content
        print(response_text)
        print()
        history.append({"role": "assistant", "content": response_text})
    else:
        response = client.chat.completions.create(messages=history, model=model, temperature=temperature)
        response_text = response.choices[0].message.content
        print(response_text)
        print()
        history.append({"role": "assistant", "content": response_text})
