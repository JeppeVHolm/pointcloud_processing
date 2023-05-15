from pyntcloud import PyntCloud
anlaegshul = PyntCloud.from_file("C:/Users/sguld/OneDrive/Dokumenter/OneDrive - Aalborg Universitet/Uni/P8/Projekt/Data/Test_data_volume/papkasse_1.ply")
convex_hull_id = anlaegshul.add_structure("convex_hull")
convex_hull = anlaegshul.structures[convex_hull_id]
anlaegshul.mesh = convex_hull.get_mesh()
anlaegshul.to_file("C:/Users/sguld/OneDrive/Dokumenter/OneDrive - Aalborg Universitet/Uni/P8/Projekt/Data/Test_data_volume/Visuelle net/papkasse_1_net.ply", also_save=["mesh"])
volume = convex_hull.volume
print("The calculated volume of the point cloud using PyntCloud is:", volume,"m3")