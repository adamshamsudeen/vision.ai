#!/bin/bash
# Directory containing model checkpoints.
CHECKPOINT_DIR="${HOME}/im2txt/model/train"

# Vocabulary file generated by the preprocessing script.
VOCAB_FILE="${HOME}/im2txt/data/mscoco/word_counts.txt"

# JPEG image file to caption.
IMAGE_FILE="/home/ubuntu/im2txt/images/$1"

# Build the inference binary.
#bazel build -c opt im2txt/run_inference

# Ignore GPU devices (only necessary if your GPU is currently memory
# constrained, for example, by running the training script).
#export CUDA_VISIBLE_DEVICES=""

# Run inference to generate captions.
bazel-bin/im2txt/run_inference \
  --checkpoint_path=${CHECKPOINT_DIR} \
  --vocab_file=${VOCAB_FILE} \
  --input_files=${IMAGE_FILE}
