from app.config import CHUNK_SIZE, OVERLAP_SIZE

def chunking(docs: str) -> list[str]:
    """Split documentation into chunks of approximately CHUNK_SIZE without breaking words."""
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

def apply_overlap(chunks: list[str]) -> list[str]:
    """Apply overlap to chunks by prepending the last OVERLAP_SIZE characters
    from the previous chunk to each subsequent chunk"""
    if OVERLAP_SIZE <= 0:
        return chunks

    overlapped : list[str]= []

    for i, chunk in enumerate(chunks):
        if i == 0:
            overlapped.append(chunk)
        else:
            # get the last OVERLAP_SIZE characters from the previous chunk and prepend to the current chunk
            overlap_text : str = chunks[i - 1][-OVERLAP_SIZE:]
            # overlapped.append(overlap_text+chunk)
            new_chunk : str= (overlap_text + chunk)
            overlapped.append(new_chunk[:CHUNK_SIZE])
    return overlapped


def recursive_chunking(docs: str, separators: list[str] = ["\n\n", "\n", ". ", " ", ""]):
    """Split text recursively using a hierarchy of separators. """
    # base case
    if len(docs) <= CHUNK_SIZE:
        return [docs]

    sep : str = separators[0]
    parts : list[str] = docs.split(sep)

    chunks : list[str] = []
    current_chunk : str = ""

    for part in parts:
        # skip empty parts
        if not part.strip():
            continue

        piece : str = part + sep

        # accumulate until chunk would exceed size
        if len(current_chunk) + len(piece) <= CHUNK_SIZE:
            current_chunk += piece
        else:
            # finalize current chunk
            if len(current_chunk) > CHUNK_SIZE and len(separators) > 1:
                chunks.extend(
                    recursive_chunking(current_chunk, separators[1:])
                )
            else:
                chunks.append(current_chunk.strip())
            # start new chunk
            current_chunk = piece  

    # append remaining chunk
    if current_chunk:
        if len(current_chunk) > CHUNK_SIZE and len(separators) > 1:
            chunks.extend(
                recursive_chunking(current_chunk, separators[1:])
            )
        else:
            chunks.append(current_chunk.strip())

    return chunks
