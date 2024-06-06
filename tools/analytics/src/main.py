import os
import sys
from typing import List

import seaborn as sns
from config import COLOR_SCHEME
from ec2benchmarks import process as process_ec2_data
from huggingface import free, mpstat, nvidia_smi
from preprocessing import preprocess_files
from render import AnalysisResults


def main(args):
    directory = args[1]
    out = args[2]
    files = get_data_files(directory)
    results = AnalysisResults(out)
    results.set_destdir(out)

    for file in files:
        ext = file.split(".")[-1]
        match ext:
            case "csv":
                data = process_ec2_data(file)
                results.add_entry(file, data)

            case "free":
                (max_mem, inf_mem) = free(file)
                results.add_entry(file, [max_mem, inf_mem])

            case "mpstat":
                (infcpu, maxcpu) = mpstat(file)
                results.add_entry(file, [infcpu, maxcpu])

            case "nvidia-smi":
                (
                    maxvram,
                    infvram,
                    infgpu,
                    infvram_bw_percent,
                    infmaxsinglgpu_percent,
                    infmaxsinglvrambw,
                ) = nvidia_smi(file, start=-20, end=-10)

                results.add_entry(
                    file,
                    [
                        maxvram,
                        infvram,
                        infvram_bw_percent,
                        infmaxsinglvrambw,
                        infgpu,
                        infmaxsinglgpu_percent,
                    ],
                )

            case "vmstat":
                pass

    results.render_all()


def get_data_files(dir: str) -> List[str]:
    paths = []
    walk = os.walk(dir)
    for root, _, files in walk:
        for f in files:
            paths.append(f"{root}/{f}")
    return paths


if __name__ == "__main__":
    help_text = "Usage: \n\t py main.py [--preprocess] [directory]"
    sns.set_theme(style="darkgrid", palette=COLOR_SCHEME)
    if len(sys.argv) <= 1:
        print(help_text)
        exit(1)
    if sys.argv[1] == "--preprocess":
        preprocess_files(get_data_files(sys.argv[2]))
    else:
        main(sys.argv)
