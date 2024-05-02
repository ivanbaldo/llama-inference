METRICS = ["mean", "max", "min", "stddev"]
COLOR_SCHEME = 'coolwarm'

GRAPH_STYLE = {
    "rot":45,
    "fontsize":6,
    "legend":None,
    "title": "Tokens per second (average)",
    "x": "title",
    "xlabel": "Model"
}

SUPPORTED_FORMATS = ["free", "mpstat", "csv", "nvidia-smi"]

OUTPUT_FORMAT = "png"

MPSTAT_HEADER = "time\tCPU\t%usr\t%nice\t%sys\t%iowait\t%irq\t%soft\t%steal\t%guest\t%gnice\t%idle\n"

# ---- DATOS DE INTERÉS ----
MPSTAT_OUTPUT = ["title", "InfCPU", "MaxCPU"]
FREE_OUTPUT = ["title", "MaxMem", "InfMem"]
NVIDIA_SMI_OUTPUT = ["title","InfVRAM",  "MaxVRAM", "InfVRAMBW%", "InfMaxSinglVRAMBW%", "InfGPU%",  "InfMaxSinglGPU%" ]

OUTPUT_SCHEMAS = {
    "csv": ["title", *METRICS],
    "free": FREE_OUTPUT,
    "mpstat": MPSTAT_OUTPUT,
    "nvidia-smi": NVIDIA_SMI_OUTPUT
}

# dict[str, (métrica, menor_a_mayor?)]
# Métrica coloreada que se usa para ordenar y criterio de orden
HIGHLIGHTED_METRIC = {
    "csv": ("first%", False),
    "free": (FREE_OUTPUT[1], True),
    "mpstat": (MPSTAT_OUTPUT[1], True),
    "nvidia-smi": (NVIDIA_SMI_OUTPUT[1], True)
}
