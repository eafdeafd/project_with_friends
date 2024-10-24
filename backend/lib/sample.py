import random
from pathlib import Path

def stream_sample(prompt: str):
    if prompt:
        random.seed(prompt)

    samples = Path(__file__).parent / "sample_responses"
    sample_file = random.choice(list(samples.glob("*.txt")))
    with open(samples / sample_file, "r") as f:
        entire_file = f.read()
        current_pos = 0
        while current_pos < len(entire_file):
            chunk_size = random.randint(50, 500)
            chunk = entire_file[current_pos : current_pos + chunk_size]
            current_pos += chunk_size
            yield chunk