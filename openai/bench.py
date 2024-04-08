import sys
import pandas as pd

from client import args, chat

sys.path.append("../common/")
from questions import questions

if __name__ == "__main__":
    counter = 1
    responses = []
    for q in questions:
        response = chat(q)
        if counter >= 2:  # allow for a warmup
            responses.append(response)
        counter += 1

    df = pd.DataFrame(responses)
    df.to_csv(args.filename, index=False)
