import argparse
import os
import time

import torch
from diffusers import StableDiffusionPipeline, DiffusionPipeline


def main(args):
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    model_id = args.model
    if model_id == "runwayml/stable-diffusion-v1-5":
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    elif model_id == "andite/anything-v4.0":
        pipe = DiffusionPipeline.from_pretrained(model_id)
    else:
        pipe = DiffusionPipeline.from_pretrained(model_id)
    pipe.safety_checker = lambda images, clip_input: (images, False)
    pipe = pipe.to("cuda")

    while True:
        prompt = input("prompt: ")
        start_time = time.time()
        image = pipe(prompt).images[0]
        end_time = time.time()
        print(f"time used: {end_time - start_time:.2f} seconds")
        image.save(os.path.join(output_dir, f"{prompt}.png"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='andite/anything-v4.0',
                        choices=['andite/anything-v4.0', 'runwayml/stable-diffusion-v1-5'])
    parser.add_argument('--output_dir', type=str, default='outputs')
    args_ = parser.parse_args()
    main(args_)
