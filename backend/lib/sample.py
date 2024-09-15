import os
import random
from pathlib import Path

def stream_sample(prompt: str):
    samples = Path(__file__).parent / "sample_responses"
    sample_file = random.choice(list(samples.glob("*.txt")))
    with open(samples / sample_file, "r") as f:
        chunks = f.read().split('=')
        for chunk in chunks:
            yield chunk