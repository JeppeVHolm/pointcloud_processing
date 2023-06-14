import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d

pcd = o3d.io.read_point_cloud("C:/Users/Ejer/OneDrive - Aalborg Universitet/Skrivebord/Vol_beregning/Vol_original_filer/output_class1/Area_2_cloud_3_class1_cut.ply")

segment_models = {}
segments = {}
max_plane_idx = 20
rest = pcd
d_threshold = 0.01

inlier_cloud = o3d.geometry.PointCloud()  # Inlier point cloud
outlier_cloud = o3d.geometry.PointCloud()  # Outlier point cloud

for i in range(max_plane_idx):
    colors = plt.get_cmap("tab20")(i)
    segment_models[i], inliers = rest.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)
    segments[i] = rest.select_by_index(inliers)
    labels = np.array(segments[i].cluster_dbscan(eps=d_threshold * 10, min_points=10))
    candidates = [len(np.where(labels == j)[0]) for j in np.unique(labels)]
    best_candidate = int(np.unique(labels)[np.where(candidates == np.max(candidates))[0]])
    print("the best candidate is: ", best_candidate)
    
    # Update inlier and outlier point clouds
    inlier_cloud += segments[i].select_by_index(list(np.where(labels == best_candidate)[0]))
    outlier_cloud += rest.select_by_index(inliers) + segments[i].select_by_index(list(np.where(labels != best_candidate)[0]))
    
    rest = rest.select_by_index(inliers, invert=True) + segments[i].select_by_index(list(np.where(labels != best_candidate)[0]))
    segments[i] = segments[i].select_by_index(list(np.where(labels == best_candidate)[0]))
    segments[i].paint_uniform_color(list(colors[:3]))
    print("pass", i + 1, "/", max_plane_idx, "done.")

# Radius outlier removal
radius = 0.1
nb_points = 5
outlier_cloud += rest
outlier_cloud, _ = outlier_cloud.remove_radius_outlier(nb_points, radius)

# Visualize the inlier and outlier point clouds
o3d.visualization.draw_geometries([inlier_cloud])  # Inlier point cloud
o3d.visualization.draw_geometries([outlier_cloud])  # Outlier point cloud

# Export inlier cloud as .ply file
inlier_file_path = "C:/Users/Ejer/OneDrive - Aalborg Universitet/Skrivebord/Vol_beregning/Vol_original_filer/output_class1/Area_2_cloud_3_class1_cut_inlier_cloud.ply"
o3d.io.write_point_cloud(inlier_file_path, inlier_cloud)
print("Inlier cloud saved as:", inlier_file_path)

# Export outlier cloud as .ply file
outlier_file_path = "C:/Users/Ejer/OneDrive - Aalborg Universitet/Skrivebord/Vol_beregning/Vol_original_filer/output_class1/Area_2_cloud_3_class1_cut_outlier_cloud.ply"
o3d.io.write_point_cloud(outlier_file_path, outlier_cloud)
print("Outlier cloud saved as:", outlier_file_path)
