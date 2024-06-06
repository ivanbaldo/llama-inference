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

## File preprocessing
Example .free file before preprocessing:
```
               total        used        free      shared  buff/cache   available
Mem:         1148221        7438      881686           9      264579     1140783
Swap:              0           0           0

               total        used        free      shared  buff/cache   available
Mem:         1148221        8174      880949           9      264582     1140046
Swap:              0           0           0

               total        used        free      shared  buff/cache   available
Mem:         1148221        8434      880687           9      264584     1139786
Swap:              0           0           0
...
```

After preprocessing:
```
type	total	used	free	shared	buff/cache	available
Mem:	1148221	7438	881686	9	264579	1140783
Swap:	0	0	0

Mem:	1148221	8174	880949	9	264582	1140046
Swap:	0	0	0

Mem:	1148221	8434	880687	9	264584	1139786
Swap:	0	0	0
...
```
