from openai import OpenAI
import argparse
import time

#TODO: should use a parent parser without --filename here.
parser = argparse.ArgumentParser(description='Run LLM inference requests and save to a CSV.')
parser.add_argument('--filename', type=str, default='/dev/stdout',
                    help='Path to the output CSV file (stdout by default).')
parser.add_argument('--note', type=str,
                    help='Note to add to the rows of the file (--model by default).')
parser.add_argument('--model', type=str, default='gpt-3.5-turbo',
                    help='Model to use (gpt-3.5-turbo by default).')
parser.add_argument('--baseurl', type=str, default='https://api.openai.com:443/v1',
                    help='Endpoint base URL (https://api.openai.com:443/v1 by default).')
args = parser.parse_args()
if ('note' not in args):
    args.note = args.model

client = OpenAI(base_url=args.baseurl)

def chat(prompt:str):
    start = time.perf_counter()
    result = client.chat.completions.create(
        model=args.model,
        max_tokens=200,
        messages=[
            {"role": "system", "content": "You are a very verbose and helpful assistant"},
            {"role": "user", "content": prompt}
        ]
    )
    request_time = time.perf_counter() - start
    return {'tok_count': result.usage.completion_tokens,
        'time': request_time,
        'question': prompt,
        'answer': result.choices[0].message.content,
        'note': args.note}

if __name__ == '__main__':
    prompt = "San Francisco is a city in"
    result = chat(prompt)
    tokPerSec = result['tok_count']/result['time']
    print(f"User: {prompt}\n"
          f"Chatbot in {result['time']}s with {result['tok_count']} tokens ({tokPerSec} t/s):\n"
          f"{result['answer']}")
