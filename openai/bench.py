from client import chat,args
import sys
sys.path.append('../common/')
from questions import questions
import pandas as pd

if __name__ == '__main__':
    counter = 1
    responses = []
    for q in questions:
        response = chat(q)
        if counter >= 2: # allow for a warmup
            responses.append(response)
        counter +=1

    df = pd.DataFrame(responses)
    df.to_csv(args.filename, index=False)
