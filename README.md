# pointcloud_processing
This repository is about preprocessing of data in order to perform semantic segmentation on 3D point clouds of utilities in open trenches. 
Furthermore, this repository includes scripts for the three following metods of volume calculation in 3D point clouds:
- Convex hull
- Delauney tetrahedralization
- Raster

The overall objective of the project is to segment 3D point clouds in order to get the utilities. Volume calculation is a way of extracting more knowledge from the pointclouds. To run the three scripts for volume calculation you will need to install the following packages in your python envoironment:
- Pyntcloud
- Scipy
- Plyfile
- Numpy
- Meshio
- Open3d
- Pdal
