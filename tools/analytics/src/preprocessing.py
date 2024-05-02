import os, sys
from typing import List

from dataframe_image.converter.browser.chrome_converter import shutil

from config import MPSTAT_HEADER


def preprocess_files(files: List[str]):
    for file in files:
        parent_dir = os.path.dirname(file).split("/")[0]
        rest = os.path.dirname(file).split("/")[1:]
        outdir = parent_dir + "_preprocessed/" + "/".join(rest) 
        if not os.path.exists(outdir):
            os.makedirs(outdir, exist_ok=True)
            #os.mkdir(outdir)
        dst = f"{outdir}/{file}"
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        match file.split(".")[-1]:
            case "mpstat":
                result = _preprocess_mpstat(file)
            case "free":
                result = _preprocess_free(file)
            case "nvidia-smi":
                result = _preprocess_nvidia_smi(file)
            case "csv":
                # Solo copiamos el archivo xq ya está bien formateado
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
        # Borramos las líneas vacías o los headers inútiles/redundantes
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
    # agregamos type porque sino el campo de tipo de memoria queda pegado al total
    return f"type\t{_replace_spaces_with_tabs(header)}{data}"

def _preprocess_nvidia_smi(file) -> str:
    with open(file) as f:
        lines = f.readlines()
        # Empieza con "# " así q lo sacamos
        header = lines[0][2:]
        # Solamente salteamos las unidades
        rest = lines[2:]
        data = [
            _replace_spaces_with_tabs(l)
            for l in rest
            if "#" not in l
        ]
        return _replace_spaces_with_tabs(header) + "".join(data)

def _replace_spaces_with_tabs(text):
    return "\t".join([x for x in text.split(" ") if x != ""])
