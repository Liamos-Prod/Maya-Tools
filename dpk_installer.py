import os
import shutil

# paths
src_path = "//Storage/esma/3D4/paperPlane/02_ressource/05.ANIMATION/SCRIPTS/DPK"
dst_path = "C:/Users/3D4/Documents/maya"
dst_subpath = "C:/Users/3D4/Documents/maya/modules"


def copy_dpk_files() : 
    if os.path.isdir(dst_path) and not os.path.isdir(dst_subpath):
        shutil.copytree(src_path, dst_subpath)
    else : 
        print("DPK is already copied ! ")
        
copy_dpk_files()