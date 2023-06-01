import pyntcloud
import numpy as np
import open3d as o3d
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objs as go

# Load the point cloud from .ply file
cloud = pyntcloud.PyntCloud.from_file("path/to/point/clouds/filename.ply")

# Get the lowest z value in the point cloud
max_z = cloud.points["z"].max()

# Subtract the lowest z value from all z values
cloud.points["z"] -= max_z

# Save the modified point cloud to a new .ply file
cloud.to_file("modified_point_cloud.ply")



# Load the modified point cloud from .ply file
cloud = pyntcloud.PyntCloud.from_file("modified_point_cloud.ply")

# Define the transformation matrix for mirroring in the x,y plane
mirror_matrix = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]])

# Apply the transformation to the point coordinates
cloud.points = pd.DataFrame.from_dict(cloud.points)
cloud.points[["x", "y", "z"]] = np.dot(cloud.points[["x", "y", "z"]], mirror_matrix)

# Save the mirrored point cloud to a new .ply file
cloud.to_file("path/to/pcp_mirrored.ply")

# Load the mirrored point cloud from .ply file
mirrored_cloud = pyntcloud.PyntCloud.from_file("path/to/pcp_mirrored.ply")

# Create a 3D figure and add a 3D scatter plot of the point cloud
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(mirrored_cloud.points["x"], mirrored_cloud.points["y"], mirrored_cloud.points["z"])

# Load PLY fil
pcd = o3d.io.read_point_cloud("path/to/pcp_mirrored.ply")

# Konverter point cloud over til numpy array
points = np.asarray(pcd.points)

# Projecter point cloud over i xy plan
xy_points = points[:, :2]

# Definer grid parametre
x_min, x_max = np.min(xy_points[:, 0]), np.max(xy_points[:, 0])
y_min, y_max = np.min(xy_points[:, 1]), np.max(xy_points[:, 1])
grid_size = 0.05  # grid størrelse i meter

# Oprettelse af grid
x_grid, y_grid = np.meshgrid(np.arange(x_min, x_max, grid_size),
                             np.arange(y_min, y_max, grid_size))

# Interpoler z værdier over i grid
z_grid = np.zeros_like(x_grid)
for i in range(x_grid.shape[0]):
    for j in range(x_grid.shape[1]):
        x, y = x_grid[i, j], y_grid[i, j]
        indices = np.where((xy_points[:, 0] >= x - grid_size/2) &
                           (xy_points[:, 0] < x + grid_size/2) &
                           (xy_points[:, 1] >= y - grid_size/2) &
                           (xy_points[:, 1] < y + grid_size/2))
        if len(indices[0]) > 0:
            z_grid[i, j] = np.min(points[indices, 2])

# Gem fil i CSV fil
np.savetxt("Raster_text_file.csv", z_grid, delimiter=",") #Fil skal have nyt navn hver gang

# Beregen volume
cell_volume = grid_size ** 2
total_volume = (np.sum(z_grid * cell_volume)*-1)
print("Beregnet volume:", total_volume, "m3")

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("Raster_text_file.csv", header=None)

# Create a grid of x, y, and z values
x = np.linspace(0, df.shape[1] - 1, df.shape[1])
y = np.linspace(0, df.shape[0] - 1, df.shape[0])
x, y = np.meshgrid(x, y)
z = np.flipud(df.values)  # reverse the order of the rows in the DataFrame

# Create the 3D surface plot
fig = go.Figure(data=[go.Surface(x=x, y=y, z=z)])
fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))

fig.show()

