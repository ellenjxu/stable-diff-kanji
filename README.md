# stable-diff-kanji

Follow instructions in [CompVis stable diffusion](https://github.com/CompVis/stable-diffusion?tab=readme-ov-file) to set up environment. Make sure you are in the proper conda env (`conda activate ldm`).

1. Run `create_dataset.py` to create dataset. Extracts Kanji images and corresponding English description from .xml ([source](https://kanjivg.tagaini.net/)).

```
data/
├── kanji/
│ ├── kanji_id1.jpg
│ ├── kanji_id2.jpg
│ ├── ...
│ └── descriptions.txt
```

2. Modify `train.yaml` config file
3. Train Stable Diffusion1.4 model: `python3 stable-diffusion/train.py --base train.yaml --train True`
