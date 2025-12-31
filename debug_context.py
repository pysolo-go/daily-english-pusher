
from llama_index.core.workflow import Context
import inspect

print("Context methods:")
for name, method in inspect.getmembers(Context):
    if not name.startswith("_"):
        print(name)
