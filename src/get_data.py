import requests
import wget

def get_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error al descargar la página. Código de estado: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None

# URL de la página que deseas descargar
nivel = 'L4'
year = '2014'
fecha = '20140101'
variable = 'ghrsst'
data_type = 'MUR25'
day = '001'
data_file = f'{fecha}090000-JPL-L4_{variable}-SSTfnd-{data_type}-GLOB-v02.0-fv04.1.nc'
src = 'https://www.ncei.noaa.gov/data/oceans'
url_pagina = f'{src}/{variable}/{nivel}/GLOB/JPL/{data_type}/{year}/{day}/{data_file}'

print(url_pagina)
# Descargar la página
#sst_data = get_data(url_pagina)

# Si la descarga fue exitosa, puedes guardar el contenido en un archivo
if sst_data:
    nombre_archivo = data_file
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(sst_data)
    print(f"Página descargada y guardada en {nombre_archivo}")

def descargar_archivo(url, destino):
    try:
        # Utilizar wget para descargar el archivo
        wget.download(url, destino)
        print("\nDescarga completada.")
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")

# Ruta y nombre del archivo de destino
ruta_destino = f"data/{data_file}"

# Realizar la descarga
descargar_archivo(url_pagina, ruta_destino)
