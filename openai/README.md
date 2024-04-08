# OpenAI Chat API compatible benchmark

Benchmark for servers compatible with the [OpenAI Chat Completions API](https://platform.openai.com/docs/guides/text-generation/chat-completions-api).

You can follow the instructions in the [Dockerfile](Dockerfile) to build a container to run the benchmark.

Or alternatively on your own machine:
```sh
cd openai
pip3 -r requirements.txt
export OPENAI_API_KEY='secret' #obtain from https://platform.openai.com/api-keys
python3 client.py #to test a single run
python3 bench.py --help #get usage help
python3 bench.py --baseurl https://api.openai.com:443/v1 --model gpt-3.5-turbo \
    --filename gpt-3.5-turbo.bench.csv --note "gpt-3.5-turbo"
```
