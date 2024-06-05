<<<<<<< HEAD
# Análisis de performance de LLMs

## Cómo correr
Primero hay que preprocesar los archivos para que se arreglen los problemas con los formatos
Básicamente convertimos todos los formatos en TSV
```
rm -r <carpeta vieja preprocesada si existe>
python3 src/main.py --preprocess <carpeta con las benchmarks>
```

Esto genera una carpeta llamada `curated_data` con todos los archivos
Ahora podemos correr:
```
python3 src/main.py curated_data
```

Esto genera el archivo `tmp/index.html` que lo podés abrir en el navegador para ver las imágenes

Algunos aspectos sobre el formato de las imágenes es configurable en `src/config.py`
=======
# LLM performance analysis

## How to run
First, we preprocess the input to convert every file into TSV (tab separated values) format
Each input file type requires its own conversion function, the already supported formats are listed in `src/config.py`
```
rm -r <old preprocessed files directory if exists>
python3 src/main.py --preprocess <benchmarks directory>
```

This command generates a directory with all preprocessed files, named after the original directory with `_preprocessed` appended to it
Now we can run:
```
python3 src/main.py <benchmarks directory>_preprocessed <output directory>
```

This will generate `index.html` and the visualizations under `<output directory>`

Some options for data and image format are available in `src/config.py`


## Example run
Raw data directory:
```
examples
└── benchmarks
   ├── '2024-04 Llama2-70b p4d.24xlarge'
   │  ├── CTranslate2.csv
   │  ├── CTranslate2.free
   │  ├── CTranslate2.mpstat
   │  └── CTranslate2.nvidia-smi
   └── '2024-04 OpenAI'
      ├── 'OpenAI gpt-3.5-turbo.csv'
      ├── 'OpenAI gpt-3.5-turbo.free'
      ├── 'OpenAI gpt-3.5-turbo.mpstat'
      ├── 'OpenAI gpt-3.5-turbo.nvidia-smi'
      ├── 'OpenAI gpt-4-turbo-preview.csv'
      ├── 'OpenAI gpt-4-turbo-preview.free'
      ├── 'OpenAI gpt-4-turbo-preview.mpstat'
      └── 'OpenAI gpt-4-turbo-preview.nvidia-smi'
```

Running `python3 src/main.py --preprocess examples/benchmarks` creates:
```
examples_preprocessed
└── benchmarks
   ├── '2024-04 Llama2-70b p4d.24xlarge'
   │  ├── CTranslate2.csv
   │  ├── CTranslate2.free
   │  ├── CTranslate2.mpstat
   │  └── CTranslate2.nvidia-smi
   └── '2024-04 OpenAI'
      ├── 'OpenAI gpt-3.5-turbo.csv'
      ├── 'OpenAI gpt-3.5-turbo.free'
      ├── 'OpenAI gpt-3.5-turbo.mpstat'
      ├── 'OpenAI gpt-3.5-turbo.nvidia-smi'
      ├── 'OpenAI gpt-4-turbo-preview.csv'
      ├── 'OpenAI gpt-4-turbo-preview.free'
      ├── 'OpenAI gpt-4-turbo-preview.mpstat'
      └── 'OpenAI gpt-4-turbo-preview.nvidia-smi'
```
Each file is replicated with the same path and data but with a TSV format
Then, run `python3 src/main.py examples_preprocessed/benchmarks tmp` which creates:
```
tmp
├── graph.png
├── index.html
├── table_csv.png
├── table_free.png
├── table_mpstat.png
└── table_nvidia-smi.png
```


>>>>>>> a25d5d7 (translated docs and fixed inconsistencies)
