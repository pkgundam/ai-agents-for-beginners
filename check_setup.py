import os
import sys

from dotenv import load_dotenv
import openai

load_dotenv()

print("Python:", sys.version.split()[0])
print("openai package:", openai.__version__)

if os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY: found")
else:
    print("OPENAI_API_KEY: missing, add it to your .env file")

print("Setup done, let's build agents from the very basics")
