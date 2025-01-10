import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import geopandas as gpd
import numpy as np
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from shapely.wkt import loads
import os

def generate_raster_name(breeding_season, nvars):
    """
    Genera el nombre del archivo raster basado en la temporada reproductiva y el número de variables.
    
    Args:
    - breeding_season (str): Temporada reproductiva (e.g., "crianza").
    - nvars (str): Número de variables (e.g., "2vars").
    
    Returns:
    - str: Nombre completo del raster.
    """
    return f"Phoebastria.Immutabilis/proj_{breeding_season}_{nvars}/proj_{breeding_season}_{nvars}_Phoebastria.Immutabilis.tif"

def generate_output_folder_and_name(breeding_season, nvars, model_name):
    """
    Genera la carpeta y el nombre del archivo de salida basado en la temporada reproductiva, número de variables y modelo.
    
    Args:
    - breeding_season (str): Temporada reproductiva.
    - nvars (str): Número de variables.
    - model_name (str): Nombre del modelo (e.g., "MAXNET").
    
    Returns:
    - tuple: (output_folder, output_file_name).
    """
    folder_name = f"mapas/{breeding_season}_{nvars}"
    output_folder = os.path.join(folder_name)
    output_file_name = f"prediction_maps_{breeding_season}_{nvars}_{model_name}.png"
    return output_folder, output_file_name

def plot_raster_bands_dynamic_names(breeding_season, nvars, polygon_file):
    """
    Genera mapas para cada banda de un raster basado en nombres dinámicos, agrega un polígono
    y organiza los mapas en carpetas específicas.
    
    Args:
    - breeding_season (str): Temporada reproductiva (e.g., "crianza").
    - nvars (str): Número de variables (e.g., "2vars").
    - polygon_file (str): Ruta al archivo CSV con los polígonos del continente.
    """
    # Generar el nombre del raster
    raster_file = generate_raster_name(breeding_season, nvars)
    
    # Cargar el archivo CSV con geopandas
    df = gpd.read_file(polygon_file)
    df['geometry'] = df['geom'].apply(loads)  # Convertir geometrías WKT a objetos Shapely
    continents_gdf = gpd.GeoDataFrame(df, geometry='geometry')
    continents_gdf.set_crs(epsg=4326, inplace=True)  # Configurar CRS como EPSG:4326
    
    # Abrir el archivo raster
    with rasterio.open(raster_file) as src:
        # Verificar CRS
        if src.crs.to_string() != "EPSG:4326":
            raise ValueError(f"El raster no está en CRS EPSG:4326, está en {src.crs}")
        
        # Obtener los límites y la transformación
        bounds = src.bounds  # Límites del raster
        transform = src.transform  # Transformación de georreferenciación
        
        # Iterar por todas las bandas
        for i in range(1, src.count + 1):  # Las bandas se indexan desde 1
            # Leer la banda
            band_data = src.read(i)
            # Enmascarar valores nulos
            band_data = np.ma.masked_equal(band_data, src.nodata)
            
            # Extraer la descripción de la banda y simplificar el título
            full_description = src.descriptions[i - 1] or f"Banda {i}"
            model_name = full_description.split('_')[-1]  # Extraer el último segmento después del "_"
            
            # Generar carpeta y nombre de archivo de salida
            output_folder, output_file_name = generate_output_folder_and_name(breeding_season, nvars, model_name)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            output_file = os.path.join(output_folder, output_file_name)
            
            # Crear la figura y eje con proyección PlateCarree
            fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
            ax.set_facecolor("lightcyan")  # Configurar el fondo como lightcyan
            
            # Mostrar la banda con los límites correctos
            norm = Normalize(vmin=0, vmax=1)  # Normalizar valores entre 0 y 1
            img = ax.imshow(band_data, cmap="plasma", norm=norm,
                            extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
                            transform=ccrs.PlateCarree())
            
            # Configurar el color para valores nulos
            img.cmap.set_bad(color='lightcyan')  # Asigna blanco a los valores enmascarados
            
            # Graficar el polígono del continente
            continents_gdf.plot(
                ax=ax,
                color="gray",
                edgecolor="olive",
                linewidth=1.5,
                alpha=0.4,
                transform=ccrs.PlateCarree(),
                label="Continentes"
            )
            
            # Ajustar la extensión geográfica del mapa
            ax.set_extent([-165, -110, 20, 60], crs=ccrs.PlateCarree())
            
            # Agregar barra de colores
            cbar = plt.colorbar(img, ax=ax, orientation="vertical", pad=0.02, shrink=0.8)
            cbar.set_label("Probabilidad de Presencia", fontsize=12)
            
            # Configurar el título con el nombre del modelo
            ax.set_title(model_name, fontsize=16, pad=15)
            
            # Configurar las líneas de cuadrícula
            gridlines = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
            gridlines.top_labels = False
            gridlines.right_labels = False
            gridlines.xlabel_style = {'size': 10}
            gridlines.ylabel_style = {'size': 10}
            gridlines.xformatter = LONGITUDE_FORMATTER  # Formato personalizado para longitud
            gridlines.yformatter = LATITUDE_FORMATTER  # Formato personalizado para latitud
            
            # Guardar el mapa en un archivo
            plt.savefig(output_file, dpi=300, bbox_inches="tight")
            plt.close()
            
            print(f"Mapa guardado como {output_file}")

# Listas de temporadas reproductivas y número de variables
breeding_seasons = ["incubacion", "empollamiento", "crianza"]
nvars_list = ["2vars", "4vars"]

# Iterar sobre cada combinación de temporada y número de variables
for breeding_season in breeding_seasons:
    for nvars in nvars_list:
        print(f"Procesando temporada: {breeding_season}, con {nvars}")
        plot_raster_bands_dynamic_names(breeding_season, nvars, "src/data/continents_shapefile.csv")
