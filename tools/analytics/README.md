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
