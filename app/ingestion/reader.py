import os
from app.config import PATH_DIR

def read_docs() -> str:
    """Traverse PATH_DIR and concatenate all markdown files."""
    docs : str = ""
    for root, _, files in os.walk(str(PATH_DIR)):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    docs += f.read() + "\n"
    return docs