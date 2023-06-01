from pyntcloud import PyntCloud
anlaegshul = PyntCloud.from_file("path/to/point/clouds/filename.ply")
convex_hull_id = anlaegshul.add_structure("convex_hull")
convex_hull = anlaegshul.structures[convex_hull_id]
anlaegshul.mesh = convex_hull.get_mesh()
anlaegshul.to_file("path/to/output/filename.ply", also_save=["mesh"])
volume = convex_hull.volume
print("The calculated volume of the point cloud using PyntCloud is:", volume,"m3")