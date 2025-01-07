import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import cartopy.crs as ccrs
import os

# Cargar el archivo CSV
file_path = "src/data/continents_shapefile.csv"
df = pd.read_csv(file_path)

# Carga polígono de cóncava convexa
convex_hull_file = "src/data/convex_hull.csv"
convex_hull = pd.read_csv(convex_hull_file)

# Carga polígono de isla Guadalupe
guadalupe_file = "src/data/guadalupe_island.csv"
guadalupe = pd.read_csv(guadalupe_file)

# Convertir la geometría WKT a objetos de geometría Shapely
df['geometry'] = df['geom'].apply(loads)
convex_hull['geometry'] = convex_hull['geom'].apply(loads)
guadalupe['geometry'] = guadalupe['geom'].apply(loads)

# Crear GeoDataFrames
gdf = gpd.GeoDataFrame(df, geometry='geometry')
convex_hull = gpd.GeoDataFrame(convex_hull, geometry='geometry')
guadalupe = gpd.GeoDataFrame(guadalupe, geometry='geometry')

# Configurar el CRS
gdf.set_crs(epsg=4326, inplace=True)  # EPSG:4326 corresponde a WGS 84
convex_hull.set_crs(epsg=4326, inplace=True)
guadalupe.set_crs(epsg=4326, inplace=True)

# Crear la figura con proporciones personalizadas
fig = plt.figure(figsize=(21, 15))
fig.suptitle("Área de estudio para la predicción de la probabilidad de presencia del albatros de Laysan\n", fontsize=30)
grid_spec = fig.add_gridspec(
    2, 2,  # 2 filas, 2 columnas
    width_ratios=[1, 3],  # Segunda columna más ancha
    height_ratios=[1.5, 3]  # Filas iguales
)

# Subgráfico pequeño 1 (Primera columna, primera fila)
ax1 = fig.add_subplot(grid_spec[0, 0], projection=ccrs.PlateCarree(central_longitude=180))
ax1.set_facecolor("lightcyan")

# Graficar el primer mapa pequeño
gdf.plot(
    ax=ax1, color="olivedrab", 
    transform=ccrs.PlateCarree(),
    edgecolor="olive", linewidth=0.2, 
    alpha=0.6,
    label="Área de predicción"
)
convex_hull.boundary.plot(ax=ax1, 
                          transform=ccrs.PlateCarree(), 
                          color="red", linewidth=1.5, 
                          label="Convex Hull",
                          hatch="...")
ax1.set_extent([-180, 180, -60, 90], crs=ccrs.PlateCarree())
ax1.set_title("Área de estudio\n", fontsize=24)

from matplotlib.patches import ConnectionPatch

# Subgráfico pequeño 2 (Primera columna, segunda fila)
ax2 = fig.add_subplot(grid_spec[1, 0], projection=ccrs.PlateCarree(central_longitude=0))
ax2.set_facecolor("lightcyan")

# Configurar cuadrícula
gridlines_ax2 = ax2.gridlines(draw_labels=True, linewidth=0.5, color="gray", alpha=0.7, linestyle="--")
gridlines_ax2.xlabel_style = {"size": 22}
gridlines_ax2.ylabel_style = {"size": 22, "rotation": 90}
gridlines_ax2.top_labels = False  
gridlines_ax2.right_labels = False

# Graficar el segundo mapa pequeño con el polígono de isla Guadalupe
guadalupe.plot(
    ax=ax2, 
    transform=ccrs.PlateCarree(),
    color="olivedrab", 
    edgecolor="olive", 
    linewidth=1.5,
    alpha=0.6,
    label="Isla Guadalupe"
)
ax2.set_extent([-118.45, -118.15, 28.8, 29.25], crs=ccrs.PlateCarree())  # Coordenadas de la isla Guadalupe
ax2.set_title("Isla Guadalupe: \n Zona de anidación de la especie\n", fontsize=24)

# Subgráfico grande (Segunda columna, ocupa dos filas)
ax3 = fig.add_subplot(grid_spec[:, 1], projection=ccrs.PlateCarree(central_longitude=0))
ax3.set_facecolor("lightcyan")

# Configurar cuadrícula
gridlines_ax3 = ax3.gridlines(draw_labels=True, linewidth=0.5, color="gray", alpha=0.7, linestyle="--")
gridlines_ax3.xlabel_style = {"size": 22}
gridlines_ax3.ylabel_style = {"size": 22, "rotation": 90}
gridlines_ax3.top_labels = False
gridlines_ax3.left_labels = False

# Graficar el mapa grande
gdf.plot(
    ax=ax3, color="olivedrab", 
    transform=ccrs.PlateCarree(),
    edgecolor="olive", linewidth=0.2, 
    alpha=0.6
)

convex_hull.boundary.plot(
    ax=ax3, transform=ccrs.PlateCarree(), 
    color="red", linewidth=1.5,
    label="Área de predicción",
)

convex_hull.plot(
    ax=ax3,
    transform=ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="red",
    linewidth=0.5,
    hatch="...",
    label="Área de predicción"
)
ax3.set_extent([-170, -90, 10, 70], crs=ccrs.PlateCarree())

legend_elements = [
    Patch(facecolor="none", edgecolor="red", 
          linewidth=1.5, label="Área de predicción",
          hatch="..."
          )
]

# Agregar la leyenda manualmente al subgráfico ax3
ax3.legend(
    handles=legend_elements,
    loc="lower right",  # Ubicación de la leyenda
    fontsize=22,  # Tamaño de la fuente
    title="Simbología",  # Título de la leyenda
    title_fontsize=24  # Tamaño de la fuente del título
)

# Coordenadas de Isla Guadalupe
guadalupe_coords = [-118.3, 28.9]  # Coordenadas aproximadas en el mapa grande

# Líneas de conexión entre ax2 (Isla Guadalupe) y ax3 (mapa grande)
line1 = ConnectionPatch(
    xyA=(guadalupe_coords[0], guadalupe_coords[1]),  # Coordenadas en el mapa grande (ax3)
    coordsA=ax3.transData,  # Sistema de coordenadas en ax3
    xyB=(-118.15, 29.25),  # Esquina superior izquierda del mapa pequeño (ax2)
    coordsB=ax2.transData,  # Sistema de coordenadas en ax2
    color="black", linewidth=1, linestyle="--", alpha=0.8
)
fig.add_artist(line1)

line2 = ConnectionPatch(
    xyA=(guadalupe_coords[0], guadalupe_coords[1]),  # Coordenadas en el mapa grande (ax3)
    coordsA=ax3.transData,  # Sistema de coordenadas en ax3
    xyB=(-118.15, 28.8),  # Esquina inferior derecha del mapa pequeño (ax2)
    coordsB=ax2.transData,  # Sistema de coordenadas en ax2
    color="black", linewidth=1, linestyle="--", alpha=0.8
)
fig.add_artist(line2)

# Ajustar disposición
plt.tight_layout()

# Guardar la figura en figures/, creando la carpeta si no existe
figures_dir = "figures/"
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)
output_file = figures_dir + "area_of_study.png"

plt.savefig(output_file, dpi=500, bbox_inches="tight")
plt.close()

print(f"Mapa guardado como {output_file}")
