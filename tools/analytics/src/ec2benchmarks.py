import pandas as pd

# from config import METRICS

def __get_avg_tok_p_s(path: str):
    df = pd.read_csv(path).drop("note", axis=1)
    df["tok_per_sec"] = df["tok_count"] / df["time"]
    data = df["tok_per_sec"]
    return (data.mean(), data.max(), data.min(), data.std())


# def process(files):
#     data = [ (name[:-4], *__get_avg_tok_p_s(p)) for (p,name) in files ]
#     df = pd.DataFrame(data, columns=["benchmark", *METRICS]).set_index("benchmark")
#     df.sort_values(by=[METRICS[0]], inplace=True, ascending=False)
#     first = max(df[METRICS[0]])
#     df["first%"] = df["mean"] / first * 100
#
#     return df



def process(file):
    # name = os.path.basename(file)
    # data = (name[:-4], *__get_avg_tok_p_s(file))
    # df = pd.DataFrame(data, columns=["benchmark", *METRICS]).set_index("benchmark")
    # df.sort_values(by=[METRICS[0]], inplace=True, ascending=False)
    # first = max(df[METRICS[0]])
    # df["first%"] = df["mean"] / first * 100

    # return data
    return __get_avg_tok_p_s(file)


