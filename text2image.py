import os
import time

import torch
from diffusers import StableDiffusionPipeline

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.safety_checker = lambda images, clip_input: (images, False)
pipe = pipe.to("cuda")

os.makedirs("outputs", exist_ok=True)

while True:
    prompt = input("prompt: ")
    start_time = time.time()
    image = pipe(prompt).images[0]
    end_time = time.time()
    print(f"time used: {end_time - start_time:.2f} seconds")
    image.save(os.path.join("outputs", f"{prompt}.png"))
