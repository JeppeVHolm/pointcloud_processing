
from scipy.spatial import Delaunay
import plyfile
import numpy as np
import meshio


def load_ply_file(filename):
    # Load the PLY file
    plydata = plyfile.PlyData.read(filename)

    # Get the x, y, z coordinates from the PLY file
    x = plydata['vertex']['x']
    y = plydata['vertex']['y']
    z = plydata['vertex']['z']

    # Create a numpy array of the points
    points = np.column_stack((x, y, z))

    return points

# Load points
points = load_ply_file("path/to/point/cloud")

# Compute the Delaunay tetrahedralization
tetra = Delaunay(points)

# Extract the tetrahedra from the Delaunay tetrahedralization
tetrahedra = tetra.simplices

# Extract the surface triangles from the tetrahedral mesh
surface = tetra.convex_hull

# Create a meshio mesh object from the surface triangles
mesh = meshio.Mesh(points, [("triangle", surface)])

# Write the mesh to a file
meshio.write("path/to/output/file_name.ply", mesh, file_format="ply")

# Compute the volume of each tetrahedron in the mesh
volumes = np.zeros(tetrahedra.shape[0])
for i, tetra in enumerate(tetrahedra):
    p0, p1, p2, p3 = points[tetra]
    volumes[i] = np.abs(np.dot(p3 - p0, np.cross(p1 - p0, p2 - p0))) / 6

# Compute the total volume of the mesh
total_volume = np.sum(volumes)
print("Total volume:", total_volume)

import open3d as o3d

# Convert the numpy array of points to an Open3D point cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Create an Open3D mesh object from the tetrahedra
mesh = o3d.geometry.TetraMesh()
mesh.vertices = pcd.points
mesh.tetras = o3d.utility.Vector4iVector(tetrahedra)

# Visualize the tetrahedra
o3d.visualization.draw_geometries([mesh, pcd])

# Convert the numpy array of points to an Open3D point cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Create an Open3D mesh object from the tetrahedra
mesh = o3d.geometry.TetraMesh()
mesh.vertices = pcd.points
mesh.tetras = o3d.utility.Vector4iVector(tetrahedra)

# Visualize the tetrahedra
o3d.visualization.draw_geometries([mesh])


