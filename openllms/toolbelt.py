from pathlib import Path
import os
import json
import requests

class Toolset:
    def __init__(self, input_dir: str | Path = "inputs") -> None:
        self.input_dir = Path(input_dir)

    @property
    def tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "open_file",
                    "description": "Opens and returns the file. The file should be listed using the list_files function first.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the file to be opened. Use the list_files function first to ensure the file exists."
                            },
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "lists all available files. This should be used before opening any file.",
                    "parameters": {}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_code",
                    "description": "Run multiline code strings and returns the result. The code is run on a sandbox, and therefore every call is ethereal. All subsequent calls will not create anything that persists on the next calls or on the system.",
                    "parameters": {
                        "code_multiline_string": {
                            "type": "string",
                            "description": "The multiline code string to be run. It doesn't support running files. Provide only the multiline string of the code to be ran. Provide only the MULTILINE STRING."
                        },
                        "required": ["code_multiline_string"]
                    }
                }
            }
        ]

    @property
    def tool_name_to_func(self):
        tools = {
            "open_file": self.open_file,
            "list_files": self.ls,
            "run_code": self.run_code,
        }
        return tools

    def open_file(self, name: str):
        try:
            file_path = self.input_dir / name
            with open(file_path) as f:
                file = f.readlines()
                file = " ".join(file)
        except FileNotFoundError:
            return "The file doesn't exist. Did you use list_files before actually trying to open a file? Please use list_files before trying to open any file."
        return file

    def ls(self):
        """
        List the available files to be accessed
        """
        return os.listdir(self.input_dir)
    
    def run_code(self, code_multiline_string: str):
        url = "http://localhost:8080"
        headers = {"Content-Type": "application/json"}
        data = {"code": code_multiline_string}

        response = requests.post(url, headers=headers, json=data)

        return response.text
    
    def handle_tool_calls(self, message):
        # message is request.choices[0], for example
        results = []
        if message.tool_calls:
            for tool_call in message.tool_calls:
                arguments = json.loads(tool_call.function.arguments)
                try:
                    result = self.tool_name_to_func[tool_call.function.name](**arguments)
                    results.append({f"{tool_call.function.name}({arguments})": result})
                except Exception as e:
                    results.append({f"{tool_call.function.name}({arguments})": e.message})
        return results

    def handle_message(self, response):
        return self.handle_tool_calls(response.choices[0].message)
