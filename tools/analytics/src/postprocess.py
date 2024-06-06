import pandas as pd
from config import HIGHLIGHTED_METRIC, METRICS, NVIDIA_SMI_OUTPUT


def postprocess_csv(df: pd.DataFrame) -> pd.DataFrame:
    df.sort_values(by=[METRICS[0]], inplace=True, ascending=False)
    first = max(df[METRICS[0]])
    df["first%"] = df["mean"] / first * 100

    return df


def postprocess_free(df: pd.DataFrame) -> pd.DataFrame:
    cols = [col for col in df.columns if col != "title"]
    df[cols] = df[cols].astype(int)
    (metric, _) = HIGHLIGHTED_METRIC["free"]
    df.sort_values(by=metric, inplace=True, ascending=True)
    return df


def postprocess_mpstat(df: pd.DataFrame) -> pd.DataFrame:
    (metric, _) = HIGHLIGHTED_METRIC["mpstat"]
    df.sort_values(by=metric, inplace=True, ascending=True)
    return df


def postprocess_nvidia_smi(df: pd.DataFrame) -> pd.DataFrame:
    df = df[NVIDIA_SMI_OUTPUT]
    int_cols = ["MaxVRAM", "InfVRAM", "InfGPU%", "InfVRAMBW%"]
    df[int_cols] = df[int_cols].astype(int)
    (metric, _) = HIGHLIGHTED_METRIC["nvidia-smi"]
    df.sort_values(by=metric, inplace=True, ascending=True)
    return df
