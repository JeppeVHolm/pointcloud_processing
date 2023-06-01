import os
import pdal 
import json

input_path = "path/to/point/clouds"
output_path = "path/to/output"

# make sure output directory exists
if not os.path.exists(output_path):
    os.makedirs(output_path)

# list ply files in input the input directory
ply_files = [f for f in os.listdir(input_path) if f.endswith('.ply') and not f.startswith('.')] # added startswith condition to aviod inclussion of ._files

# Origin Coordinates

Area1 = "1  0  0  0  0 1  0  0  0  0  1  0.00  0  0  0  1"
Area2 = "1  0  0  0 0  1  0  0  0  0  1  0.00  0  0  0  1"
Area3 = "1  0  0  0 0  1  0  0  0  0  1  0.00  0  0  0  1"
Area4 = "1  0  0  0 0  1  0  0  0  0  1  0.00  0  0  0  1"
Area5 = "1  0  0  0 0  1  0  0  0  0  1  0.00  0  0  0  1"

def transformation_pdal(x_coord, y_coord, z_coord=0.00):
   transfromMatrix = f"1  0  0  {x_coord} 0  1  0  {y_coord}  0  0  1  {z_coord}  0  0  0  1"
   return transfromMatrix
   
### PDAL Pipelines ###

# 0 = Never classified
# 1 = Unassigned
# 2 = Ground
# 3 = Low Vegetation
# 4 = Medium Vegetation
# 5 = High Vegetation
# 6 = Building
# 7 = Low Point
# 8 = Reserved
# 9 = Water

# "filename":os.path.join(output_path,filename.replace('ply','las')) 
def pdal_pipeline_to_LAS(filename):
    pipeline_dict = [
        {
            "type":"readers.ply",
            "filename":input_path+filename,
        },
        {
            "type": "filters.ferry",
            "dimensions": "=>Classification"
        },
        {
            "type":"filters.ferry",
            "dimensions":"label => Classification"
        },
        {
            "assignment": "Classification[2:2]=9",
            "type": "filters.assign"
        },
        {
            "assignment": "Classification[1:1]=6",
            "type": "filters.assign"
        },
        {
            "assignment": "Classification[0:0]=2",
            "type": "filters.assign"
        },
        {
            "type":"filters.transformation",
            "matrix":"1  0  0  0  0  1  0  0  0  0  1  0.00  0  0  0  1"
        },
        {
            "type":"writers.las",
            "scale_x":"0.0000001",
            "scale_y":"0.0000001",
            "scale_z":"0.0000001",
            "offset_x":"auto",
            "offset_y":"auto",
            "offset_z":"auto",
            "filename":os.path.join(output_path,filename.replace('ply','las'))
        }
    ]
    return pipeline_dict

def pdal_pipeline_update_classes(filename):
    pipeline_dict = [
        {
            "type":"readers.ply",
            "filename":input_path+filename,
        },
        {
            "type": "filters.ferry",
            "dimensions": "=>Classification"
        },
        {
            "type":"filters.ferry",
            "dimensions":"scalar_classification => Classification"
        },
        {
            "assignment": "Classification[2:2]=6",
            "type": "filters.assign"
        },
        {
            "assignment": "Classification[1:1]=2",
            "type": "filters.assign"
        },
        {
            "assignment": "Classification[3:3]=9",
            "type": "filters.assign"
        },
        {
            "assignment": "Classification[4:4]=7",
            "type": "filters.assign"
        },
        {
            "type":"writers.ply",
            "storage_mode":"big endian",
            "filename":output_path+filename
        }
    ]
    return pipeline_dict

def pdal_pipeline_noise_removal(filename):
    pipeline_dict = [
        {
            "type":"readers.ply",
            "filename":input_path+filename
        },
        {
            "type": "filters.ferry",
            "dimensions": "=>Classification"
        },
        {
            "type":"filters.ferry",
            "dimensions":"scalar_classification => Classification"
        },
        {
            "type":"filters.outlier",
            "method":"statistical",
            "mean_k":60,
            "multiplier":6.0,
            "class":7
        },
        {
            "type":"filters.range",
            "limits":"Classification![7:7]"
        },
        {
            "type":"writers.ply",
            "storage_mode":"big endian",
            "filename":output_path+filename
        }
    ]
    return pipeline_dict

def pdal_pipeline_noise_classify(filename):
    pipeline_dict = [
        {
            "type":"readers.ply",
            "filename":input_path+filename
        },
        {
            "type": "filters.ferry",
            "dimensions": "=>Classification"
        },
        {
            "type":"filters.ferry",
            "dimensions":"scalar_classification => Classification"
        },
        {
            "assignment": "Classification[2:2]=9",
            "type": "filters.assign"
        },
        {
            "assignment": "Classification[1:1]=6",
            "type": "filters.assign"
        },
        {
            "assignment": "Classification[0:0]=2",
            "type": "filters.assign"
        },
        {
            "type":"filters.outlier",
            "method":"statistical",
            "mean_k":60,
            "multiplier":6.0,
            "class":7
        },
        {
            "type":"filters.transformation",
            "matrix":"1  0  0  0  0  1  0  0  0  0  1  0.00  0  0  0  1"
        },
        {
            "type":"writers.ply",
            "storage_mode":"big endian",
            "filename":output_path+filename
        }
    ]
    return pipeline_dict

def pdal_pipeline_transform_and_downsample(filename, offset):
    pipeline_dict = [
        {
            "type":"readers.ply",
            "filename":input_path+filename
        },
        {
            "type":"filters.transformation",
            "matrix":offset
        },
        {
            "type":"filters.voxelcenternearestneighbor",
            "cell":0.003
        },
        {
            "type":"writers.ply",
            "storage_mode":"big endian",
            "filename":output_path+filename
        }
    ]
    return pipeline_dict

def pdal_pipeline_downsample(filename, downsample_value):
    pipeline_dict = [
        {
            "type":"readers.ply",
            "filename":input_path+filename
        },
        {
            "type":"filters.voxelcenternearestneighbor",
            "cell":downsample_value
        },
        {
            "type":"writers.ply",
            "storage_mode":"big endian",
            "filename":output_path+filename
        }
    ]
    return pipeline_dict

def pdal_pipeline_prepare(filename, offset):
    pipeline_dict = [
        {
            "type":"readers.ply",
            "filename":input_path+filename
        },
        {
            "type":"filters.transformation",
            "matrix":offset
        },
        {
            "type":"filters.voxelcenternearestneighbor",
            "cell":0.003
        },
        {
            "type": "filters.ferry",
            "dimensions": "=>Classification"
        },
        {
            "type":"filters.ferry",
            "dimensions":"scalar_Classification => Classification"
        },
        {
            "type":"filters.outlier",
            "method":"statistical",
            "mean_k":60,
            "multiplier":6.0,
            "class":7
        },
        {
            "type":"filters.range",
            "limits":"Classification![7:7]"
        },
        {
            "type":"writers.ply",
            "storage_mode":"big endian",
            "filename":output_path+filename
        }
    ]
    return pipeline_dict

def pdal_pipeline_inference_prepare(filename):
    pipeline_dict = [
        {
            "type":"readers.ply",
            "filename":input_path+filename
        },
        {
            "type":"filters.voxelcenternearestneighbor",
            "cell":0.003
        },
        {
            "type": "filters.ferry",
            "dimensions": "=>Classification"
        },
        {
            "type":"filters.assign",
            "assignment":"Classification[:]=0"
        },
        {
            "type":"filters.outlier",
            "method":"statistical",
            "mean_k":60,
            "multiplier":6.0,
            "class":7
        },
        {
            "type":"filters.range",
            "limits":"Classification![7:7]"
        },
        {
            "type":"writers.ply",
            "storage_mode":"big endian",
            "filename":output_path+filename
        }
    ]
    return pipeline_dict

def pdal_pipeline_prepare_from_LAS(filename, offset):
    pipeline_dict = [
        {
            "type":"readers.las",
            "filename":input_path+filename
        },
        {
            "type":"filters.transformation",
            "matrix":offset
        },
        {
            "type":"filters.voxelcenternearestneighbor",
            "cell":0.003
        },
        {
            "type": "filters.ferry",
            "dimensions": "=>Classification"
        },
        {
            "type":"filters.assign",
            "assignment":"Classification[:]=0"
        },
        {
            "type":"filters.outlier",
            "method":"statistical",
            "mean_k":60,
            "multiplier":6.0,
            "class":7
        },
        {
            "type":"filters.range",
            "limits":"Classification![7:7]"
        },
        {
            "type":"writers.ply",
            "storage_mode":"big endian",
            "filename":os.path.join(output_path, filename.replace(".las", ".ply"))
        }
    ]
    return pipeline_dict


### Loop PLY files and execute PDAL Pipeline ###

for ply_file in ply_files:
    print(f"{ply_file} is processing ...")
    pipeline_json = json.dumps(pdal_pipeline_transform_and_downsample(ply_file, Area1))
    pipeline = pdal.Pipeline(pipeline_json)
    count = pipeline.execute()
    arrays = pipeline.arrays
    metadata = pipeline.metadata
    log = pipeline.log

