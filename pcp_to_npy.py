from pyntcloud import PyntCloud
import os
# Set the input and output directories
input_dir = "path/to/point/clouds"
output_dir = "path/to/output"


# Loop over each PLY file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".ply"):
        # Load the PLY file into a PyntCloud object
        cloud = PyntCloud.from_file(os.path.join(input_dir, filename))

 # Save the data as an NPY file
        cloud.to_file(os.path.join(output_dir, filename + ".npy"))