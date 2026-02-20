from app.config import CHUNK_SIZE, OVERLAP_SIZE

# split the given docs up in chunks without spliting up words
def chunking(docs: str) -> list[str]:
    chunks : list[str] = []
    start : int = 0
    while start < len(docs):
        end : int = start + CHUNK_SIZE
        if end >= len(docs):
            chunks.append(docs[start:])
            break
        else:
            # find last space before end
            last_space : int = docs.rfind(" ", start, end)
            # if no space found, just split at end
            if last_space == -1:
                last_space = end
            chunks.append(docs[start:last_space])
            start = last_space - OVERLAP_SIZE
    return chunks