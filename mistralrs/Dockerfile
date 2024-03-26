# syntax=docker/dockerfile:1

# From the parent directory (main directory of this repo) run:
#
# Note: if building on a machine with a different GPU or no GPU then check
# https://developer.nvidia.com/cuda-gpus and pass the value without the decimal point to
# CUDA_COMPUTE_CAP directly without the $(...), for example for an A100 is CUDA_COMPUTE_CAP=80 and
# for an A10 is CUDA_COMPUTE_CAP=86.
#
# docker build --build-arg USERID=$(id -u) --build-arg \
#   CUDA_COMPUTE_CAP=$(nvidia-smi --query-gpu=compute_cap --format=csv | tail -n1 | tr -d .) \
#   -t local/mistralrs-bench mistralrs
#
# docker run --rm -it --name mistralrs-bench \
#   -v$HOME/.cache/huggingface/:/home/user/.cache/huggingface/ \
#   -v$(pwd):/home/user/llama-inference --gpus all local/mistralrs-bench \
#   --port 8080 llama -m meta-llama/Llama-2-7b-chat-hf
# (or mixtral, etc.)
#
# In another terminal:
#
# docker exec -it -u0:0 mistralrs-bench sh -c 'dnf -y install python3-requests python3-pip && \
#   pip3 install transformers pandas'
# docker exec -it -uuser mistralrs-bench sh -c 'cd /home/user/llama-inference/anyscale && \
#   OPENAI_API_BASE=http://localhost:8080/v1 OPENAI_API_KEY=none python3 bench.py'
#
# If using Podman with CDI substitute
#   --gpus all
# for
#   --device nvidia.com/gpu=all --security-opt=label=disable

# Select an available version from
# https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/supported-tags.md:
FROM nvcr.io/nvidia/cuda:12.3.2-cudnn9-devel-rockylinux9 as build
ARG CUDA_COMPUTE_CAP
RUN dnf install -y git openssl-devel && dnf clean all && rm -rf /var/cache/dnf/*
# package `clap v4.5.2` cannot be built because it requires rustc 1.74 and Rocky 9 has 1.71:
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y && ln -s /root/.cargo/bin/* /usr/local/bin
# Not supported by Podman / Buildah https://github.com/containers/buildah/issues/4974:
#ADD https://github.com/EricLBuehler/mistral.rs.git#master /mistral.rs
RUN git clone https://github.com/EricLBuehler/mistral.rs.git
WORKDIR /mistral.rs
RUN cargo install --path mistralrs-server --features cuda,cudnn,flash-attn

FROM nvcr.io/nvidia/cuda:12.3.2-cudnn9-runtime-rockylinux9 as runtime
ARG USERID=1000
COPY --from=build /root/.cargo/bin/mistralrs-server /usr/local/bin
RUN adduser -u $USERID user
USER user
ENTRYPOINT ["/usr/local/bin/mistralrs-server"]
CMD ["--port", "8080", "llama"]
