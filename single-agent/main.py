# single-agent/main.py

from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
print("DEBUG: OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))  # debug

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pathlib import Path


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set")

output_path = Path(__file__).parent / "generated" / "pod.yaml"
output_path.parent.mkdir(parents=True, exist_ok=True)

def generate_pod_yaml():
    chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.2, model="gpt-4")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Kubernetes expert. Your task is to create pod configuration files in YAML format based on user requests. Ensure the YAML is minimal and efficient without comments. Do not include any additional explanations or text."),
        ("human", "Write a minimal Kubernetes pod YAML that runs an nginx container with very low resource usage.")
    ])
    response = chat(prompt.format_messages())
    yaml_content = response.content.strip()

    with open(output_path, "w") as f:
        f.write(yaml_content)

    print(f"pod.yaml saved to {output_path}")

if __name__ == "__main__":
    generate_pod_yaml()
