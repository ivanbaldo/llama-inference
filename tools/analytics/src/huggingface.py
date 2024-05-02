import pandas as pd
import numpy as np


def free(file, inf_mem_row=-3):
    """
    file: archivo desde donde leer los datos
    inf_mem_row: fila que tomamos como el pico de uso de memoria durante la inferencia 
    Por defecto es el tercer valor de atrás para adelante

    info sobre la prueba:
    Linux 6.8.0-11-generic (ibaldoryzen) 	26/03/24 	_x86_64_	(16 CPU)
    """
    df = pd.read_csv(file, sep="\t")
    chunk_size = len(df)//2
    chunked = np.array_split(df["used"], chunk_size)
    sums = np.empty(chunk_size)
    for (i, chunk) in enumerate(chunked):
        sums[i] = chunk.iloc[0].sum()

    inf_mem = sums[inf_mem_row] 
    return sums.max(), inf_mem


def mpstat(file, start=-13, end=-3):
    """
    file: archivo donde leer los datos
    start:end : rango de tiempo en segundos
    por defecto toma desde los últimos 13 segundos a los últimos 3

    Métricas:
    MaxCPU: maximal percentage of a single CPU usage during inference
    InfCPU: average percentage of all CPUs usage during inference
    """
    df = pd.read_csv(file, sep="\t")
    # Promedio del %idle
    agg = df[ df["CPU"] == "all" ][["time", "%idle"]].iloc[start:end]
    agg["%use"] = 100 - agg["%idle"]
    infcpu = agg["%use"].mean()
    
    # maxcpu = 100 - df[ df["CPU"] == str(max_cpu_target) ]["%idle"].iloc[start:end].min()
    group = df[ df["CPU"] != "all" ].groupby("time").min()["%idle"][start:end]
    maxcpu = 100 - min(group)
    return (infcpu, maxcpu)


def nvidia_smi(file, start=-13, end=-3):
    """
    Por las dudas dejo el header del archivo con las unidades 
    gpu (Idx)	pwr (W)	gtemp (C)	mtemp (C)	sm (%)	mem (%)	
    enc (%)	dec (%)	jpg (%)	ofa (%) mclk (MHz)	pclk (MHz)
    pviol (%)	tviol (bool)	fb (MB)	bar1 (MB)	ccpm (MB)
    sbecc (errs)	dbecc (errs)	pci (errs)	rxpci (MB/s)	txpci (MB/s)

    Métricas a calcular:
    InfGPU%: es de -3 a -13s el promedio del promedio del sm%, es decir, por cada segundo de esos 10s, promediar el sm% de todas las GPUs y a ese promedio promediarlo en esos 10 segundos.
    InfMaxSinglGPU% es de esos -3s a -13s cual GPU tuvo el máximo sm% y ese es el valor.
    """
    df = pd.read_csv(file, sep="\t")
    n_gpus = df["gpu"].nunique()
    # chunk_size = n_gpus
    n_chunks = int(len(df) / n_gpus)
    sums = np.empty(n_chunks)
    
    # Como no podemos agrupar por campo de tiempo porque no hay, tomamos chunks que contienen una medida por cada tarjeta
    # Nos quedamos solo con las métricas q vamos a querer usar después
    chunked = np.array_split(df[["fb", "sm", "mem"]], n_chunks)

    for (i, chunk) in enumerate(chunked):
        sums[i] = chunk["fb"].sum()
    infvram = sums[end]
    maxvram = sums.max()

    # Tomamos el promedio de cada chunk y hacemos el promedio de eso
    # `abs(start-end)` es el largo del timeframe que elegimos
    infgpu = max([
        x for x in 
        map(lambda chunk: chunk["sm"].max(), chunked[start:end])]) #/ abs(start - end)

    # infvram_bw_percent = sum([x for x in map(lambda chunk: chunk["mem"].max(), chunked[start:end])]) / abs(start - end)
    infvram_bw_percent = max([x for x in map(lambda chunk: chunk["mem"].max(), chunked[start:end])]) 

    # infmaxsinglgpu_percent = df[start:end]["sm"].max()
    infmaxsinglgpu_percent = max([ch["sm"].max() for ch in chunked[start:end]])
    # infmaxsinglvrambw = df[start:end]["mem"].max()
    infmaxsinglvrambw = max([ch["mem"].max() for ch in chunked[start:end]])
    
    return (maxvram,infvram, infgpu, infvram_bw_percent, infmaxsinglgpu_percent, infmaxsinglvrambw)

