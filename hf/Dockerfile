# From the parent directory (main directory of this repo) run:
#
# docker build --build-arg USERID=$(id -u) -t local/hf-bench hf
#
# If not already using and having a $HOME/.cache/huggingface/ then:
#
# mkdir $HOME/.cache/huggingface/
# docker run --rm -it -v$HOME/.cache/huggingface/:/home/user/.cache/huggingface/ local/hf-bench \
#   huggingface-cli login
# Answer n to: Add token as git credential? (Y/n) n
#
# docker run --rm -it -v$HOME/.cache/huggingface/:/home/user/.cache/huggingface/ \
#   -v$(pwd):/home/user/llama-inference --gpus all local/hf-bench \
#   sh -c 'cd /home/user/llama-inference/hf && python3 bench.py'
#
# You can substitute bench.py by bench-bb.py, bench-gptq.py or any other.
# If using Podman with CDI substitute
#   --gpus all
# for
#   --device nvidia.com/gpu=all --security-opt=label=disable

# Select an available version from
# https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/supported-tags.md:
# 2024-04-02 PyTorch was compiled for CUDNN8:
#FROM nvcr.io/nvidia/cuda:12.3.2-cudnn9-runtime-rockylinux9
FROM nvcr.io/nvidia/cuda:12.2.2-cudnn8-runtime-rockylinux9

RUN dnf install -y \
  python3-pip cuda-cupti-$(echo $CUDA_VERSION | sed -r 's/(.+)[.](.+)[.].*/\1-\2/') && \
  dnf clean all && rm -rf /var/cache/dnf/*

RUN pip install --no-cache-dir transformers accelerate optimum bitsandbytes auto_gptq scipy

ARG USERID=1000
RUN adduser -u $USERID user
USER user

