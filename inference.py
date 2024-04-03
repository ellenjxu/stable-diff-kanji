import os
import argparse
import torch
from diffusers import StableDiffusionPipeline, UNet2DConditionModel

def parse_args():
    parser = argparse.ArgumentParser(description='kanji inference')
    parser.add_argument('--model_path', type=str, default='sd-kanji-model2')
    parser.add_argument('--prompt', type=str, default='test')
    parser.add_argument('--num_images', type=int, default=1)
    parser.add_argument('--output_dir', type=str, default='outputs/')
    parser.add_argument('--checkpoint', type=int, default=0)
    
    args = parser.parse_args()

    return args

def main():
    args = parse_args()
    os.makedirs(f'{args.output_dir}', exist_ok=True)

    if args.checkpoint:
        model_path = args.model_path
        print("path", model_path)
        unet = UNet2DConditionModel.from_pretrained(model_path + f"/checkpoint-{args.checkpoint}/unet", torch_dtype=torch.float16)

        pipe = StableDiffusionPipeline.from_pretrained(model_path, unet=unet, torch_dtype=torch.float16)
        pipe.to("cuda")

    else: 
        model_path = args.model_path
        pipe = StableDiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
        pipe.to("cuda")

    for i in range(args.num_images):
        image = pipe(prompt=args.prompt, height=128, width=128).images[0]
        image.save(f"{args.output_dir}/{args.prompt}_{i}.png")


if __name__ == '__main__':
    main()
