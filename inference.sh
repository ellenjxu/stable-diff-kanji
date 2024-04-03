export CUDA_VISIBLE_DEVICES=0
export MODEL_PATH="sd-kanji-model2"
export PROMPT="magic forest"
export NUM_IMAGES=5
export OUTPUT_DIR="outputs"
export CHECKPOINT=15000

python  inference.py \
  --model_path="$MODEL_PATH" \
  --output_dir="$OUTPUT_DIR" \
  --prompt="$PROMPT" \
  --num_images=$NUM_IMAGES \
  --checkpoint=$CHECKPOINT
