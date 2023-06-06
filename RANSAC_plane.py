# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:31:06 2023

@author: Ejer
"""
import numpy as np
import open3d as o3d

#create paths and load data
input_path="C:/Users/Ejer/OneDrive - Aalborg Universitet/Skrivebord/Vol_beregning/vol_original_filer/transformeret/"
dataname="transformeretArea1_ikkekompletsky0.ply"

pcd = o3d.io.read_point_cloud(input_path+dataname)


#Normals computation - For bedre at kunne se strukturen i skyen når det bliver samme farve
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=16), fast_normal_computation=True)
pcd.paint_uniform_color([0.6, 0.6, 0.6])
o3d.visualization.draw_geometries([pcd]) 

#3D Shape Detection with RANSAC - plane
plane_model, inliers = pcd.segment_plane(distance_threshold=0.01,ransac_n=3,num_iterations=1000)
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
inlier_cloud = pcd.select_by_index(inliers)
outlier_cloud = pcd.select_by_index(inliers, invert=True)
inlier_cloud.paint_uniform_color([1.0, 0, 0])
outlier_cloud.paint_uniform_color([0.6, 0.6, 0.6])
o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])


# Load the second point cloud
segmented_pcd = o3d.io.read_point_cloud("C:/Users/Ejer/OneDrive - Aalborg Universitet/Skrivebord/Vol_beregning/vol_original_filer/transformeret/transformeretArea1_ikkekompletsky1.ply")

# Convert segmented point cloud to NumPy array
points = np.asarray(segmented_pcd.points)

# Segment the point cloud using the plane model
distances = plane_model[0] * points[:, 0] + \
            plane_model[1] * points[:, 1] + \
            plane_model[2] * points[:, 2] + \
            plane_model[3]

# Set a threshold to determine the plane's tolerance
distance_threshold = 0.01

# Separate the points based on their distances from the plane
above_plane_indices = np.where(distances > distance_threshold)[0]
below_plane_indices = np.where(distances <= distance_threshold)[0]

# Create separate point clouds for above and below the plane
above_plane_cloud = o3d.geometry.PointCloud()
above_plane_cloud.points = o3d.utility.Vector3dVector(points[above_plane_indices])

below_plane_cloud = o3d.geometry.PointCloud()
below_plane_cloud.points = o3d.utility.Vector3dVector(points[below_plane_indices])

# Visualize the segmented point clouds
above_plane_cloud.paint_uniform_color([1.0, 0, 0])  # Red color for above the plane
below_plane_cloud.paint_uniform_color([0, 0, 1.0])  # Blue color for below the plane
o3d.visualization.draw_geometries([above_plane_cloud, below_plane_cloud])

# Export the below-plane point cloud to a .ply file
o3d.io.write_point_cloud("C:/Users/Ejer/OneDrive - Aalborg Universitet/Skrivebord/Vol_beregning/Vol_original_filer/output_class1/ikkekompletsky_cut.ply", below_plane_cloud)
o3d.io.write_point_cloud("C:/Users/Ejer/OneDrive - Aalborg Universitet/Skrivebord/Vol_beregning/Vol_original_filer/output_class1/ikkekompletsky_cut_above.ply", above_plane_cloud)