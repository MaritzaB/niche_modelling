# KDE with sklearn
from sklearn.neighbors import KernelDensity
import numpy as np

# Create grid
x_grid = np.linspace(min_lon, max_lon, 100)
y_grid = np.linspace(min_lat, max_lat, 100)
X, Y = np.meshgrid(x_grid, y_grid)

# Create training data
xy = np.vstack([geo_df['longitude'], geo_df['latitude']]).T
xy *= np.pi / 180.  # Convert lat/long to radians
xy = np.radians(xy)

# Create KDE
kde = KernelDensity(
    bandwidth=0.03, metric='haversine', 
    kernel='gaussian')
kde.fit(xy)

# Evaluate KDE
xy_grid = np.vstack([Y.ravel(), X.ravel()]).T
xy_grid *= np.pi / 180.
xy_grid = np.radians(xy_grid)
Z = np.exp(kde.score_samples(xy_grid))
Z = Z.reshape(X.shape)

# Plot KDE
plt.figure(figsize=(25, 10))
plt.xlim(min_lon, max_lon)
plt.ylim(min_lat, max_lat)
plt.pcolormesh(X, Y, Z, shading='auto')
plt.colorbar()
plt.show()
