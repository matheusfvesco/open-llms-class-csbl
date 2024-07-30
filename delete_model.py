from openllms.core import uninstall_ollama_model
import argparse
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser(description="Uninstall OLLAMA model")
parser.add_argument("model_name", help="Model name to uninstall")

args = parser.parse_args()

uninstall_ollama_model(model_name=args.model_name)