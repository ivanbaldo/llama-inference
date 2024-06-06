import numpy as np
import pandas as pd


def free(file, inf_mem_row=-3):
    """
    file: name of the file to read
    inf_mem_row: row to be used as peak inference memory usage
    By default it's the third-to-last value
    """
    df = pd.read_csv(file, sep="\t")
    chunk_size = len(df) // 2
    chunked = np.array_split(df["used"], chunk_size)
    sums = np.empty(chunk_size)
    for i, chunk in enumerate(chunked):
        sums[i] = chunk.iloc[0].sum()

    inf_mem = sums[inf_mem_row]
    return sums.max(), inf_mem


def mpstat(file, start=-13, end=-3):
    """
    file: name of the file to read
    start:end : time interval to consider, in seconds
    The default range starts at the last 13 seconds and ends in the last 3

    Metrics:
    MaxCPU: maximal percentage of a single CPU usage during inference
    InfCPU: average percentage of all CPUs usage during inference
    """
    df = pd.read_csv(file, sep="\t")
    # Mean of %idle
    agg = df[df["CPU"] == "all"][["time", "%idle"]].iloc[start:end]
    agg["%use"] = 100 - agg["%idle"]
    infcpu = agg["%use"].mean()

    # maxcpu = 100 - df[ df["CPU"] == str(max_cpu_target) ]["%idle"].iloc[start:end].min()
    group = df[df["CPU"] != "all"].groupby("time").min()["%idle"][start:end]
    maxcpu = 100 - min(group)
    return (infcpu, maxcpu)


def nvidia_smi(file, start=-13, end=-3):
    """
    Keeping the header with units around for reference:
    gpu (Idx)	pwr (W)	gtemp (C)	mtemp (C)	sm (%)	mem (%)
    enc (%)	dec (%)	jpg (%)	ofa (%) mclk (MHz)	pclk (MHz)
    pviol (%)	tviol (bool)	fb (MB)	bar1 (MB)	ccpm (MB)
    sbecc (errs)	dbecc (errs)	pci (errs)	rxpci (MB/s)	txpci (MB/s)

    file: name of the file to read
    start:end : time interval to consider, in seconds
    The default range starts at the last 13 seconds and ends in the last 3

    Metrics:
    InfGPU%: average of the per second average of sm% in the start:end time interval.
    InfMaxSinglGPU%: max value of sm% among all GPUS in the start:end time interval
    """
    df = pd.read_csv(file, sep="\t")
    n_gpus = df["gpu"].nunique()
    n_chunks = int(len(df) / n_gpus)
    sums = np.empty(n_chunks)

    # As there are no time fields, separate the input in chunks, with a single entry in each chunk for every GPU
    # Then keep only the metrics of interest
    chunked = np.array_split(df[["fb", "sm", "mem"]], n_chunks)

    for i, chunk in enumerate(chunked):
        sums[i] = chunk["fb"].sum()
    infvram = sums[end]
    maxvram = sums.max()

    # Average of the average of each chunk
    # `abs(start-end)` is the duration of the chosen timeframe
    infgpu = max(
        [x for x in map(lambda chunk: chunk["sm"].max(), chunked[start:end])]
    )  # / abs(start - end)

    infvram_bw_percent = max(
        [x for x in map(lambda chunk: chunk["mem"].max(), chunked[start:end])]
    )

    infmaxsinglgpu_percent = max([ch["sm"].max() for ch in chunked[start:end]])
    infmaxsinglvrambw = max([ch["mem"].max() for ch in chunked[start:end]])

    return (
        maxvram,
        infvram,
        infgpu,
        infvram_bw_percent,
        infmaxsinglgpu_percent,
        infmaxsinglvrambw,
    )
