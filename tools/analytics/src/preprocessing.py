import os, sys
from typing import List

import shutil

from config import MPSTAT_HEADER


def preprocess_files(files: List[str]):
    for file in files:
        parent_dir = os.path.dirname(file).split("/")[0]
        rest = os.path.dirname(file).split("/")[1:]
        outdir = parent_dir + "_preprocessed/" + "/".join(rest) 
        if not os.path.exists(outdir):
            os.makedirs(outdir, exist_ok=True)
        filename = os.path.basename(file)
        dst = f"{outdir}/{filename}"
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        match file.split(".")[-1]:
            case "mpstat":
                result = _preprocess_mpstat(file)
            case "free":
                result = _preprocess_free(file)
            case "nvidia-smi":
                result = _preprocess_nvidia_smi(file)
            case "csv":
                # Already correct formatting, just copy it over
                shutil.copy(file, dst)  
                continue
            case _:
                print(f"[WARNING] Unsupported file format: {dst}", file=sys.stderr)
                continue

        with open(dst, "w+") as f:
            f.write(result)


def _preprocess_mpstat(file) -> str:
    with open(file) as f:
        data = f.readlines()
        # Filter out blank lines and useless or redundant headers
        keep = [
            _replace_spaces_with_tabs(line)
            for line in data
            if len(line) > 0 and "CPU" not in line and not line.startswith("Linux")
        ]
        keep.insert(0, MPSTAT_HEADER)
        return "".join(keep)


def _preprocess_free(file) -> str:
    with open(file) as f:
        lines = f.readlines()
        header = lines[0]
        rest = lines[1:]
        data = "".join([
            _replace_spaces_with_tabs(l) 
            for l in rest
            if "free" not in l
        ])
    # the column which indicates Mem or Swap lacks a name, call it type and add it to the header
    return f"type\t{_replace_spaces_with_tabs(header)}{data}"

def _preprocess_nvidia_smi(file) -> str:
    with open(file) as f:
        lines = f.readlines()
        # Remove the two first lines that start with '#'
        header = lines[0][2:]
        # Skip units
        rest = lines[2:]
        data = [
            _replace_spaces_with_tabs(l)
            for l in rest
            if "#" not in l
        ]
        return _replace_spaces_with_tabs(header) + "".join(data)

def _replace_spaces_with_tabs(text):
    return "\t".join([x for x in text.split(" ") if x != ""])
