import os
from app.config import PATH_DIR

# read the docs and return as a single string
def read_docs() -> str:
    # search for all .md files in the directory
    docs : str = ""
    for root, _, files in os.walk(str(PATH_DIR)):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r") as f:
                    docs += f.read() + "\n"
    return docs