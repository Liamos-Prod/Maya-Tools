import os
import maya.cmds as cmds
import rfm2
import maya.mel as mel


def find_Vdb_File (vdb_path):


    clouds_shader_path = "//Storage/esma/3D4/paperPlane/04_asset/FX/shader/"
    clouds_shader_name = "clouds_shader"
    clouds_shader_extension = ".ma"
    clouds_shader_FP = clouds_shader_path+clouds_shader_name+clouds_shader_extension

    vbd_folders = [vdb_path+"BG",vdb_path+"FG",vdb_path+"MG"]
    group_names = []
    vdb_folder_list = []
    vdb_list = []
    vdb_files = []
    vdb_names = []
    vdb_vis_shapes = []



    error_message_folder = "Pas de dossiers existants mon GAAAAH ! "
    error_message_files = "Pas de VBD dans les dossiers mon GAAAAH ! "
    cmds.file( clouds_shader_FP, reference=True, namespace = clouds_shader_name )
    clouds_shaders = cmds.ls("clouds_shader:*",type="shadingEngine")
    # __look for all the folders in the specified path
    for file in os.listdir(vdb_path):
        f = os.path.join(vdb_path,file)
        if os.path.isdir(f):
            vdb_folder_list.append(f)
        group_names.append(f.split("/")[-1])

    if vdb_folder_list != [] : # __check if the list of folders is not empty
        for vdb_folder in vbd_folders : 
            for vdb_analyse in vdb_folder_list : 
                if vdb_analyse == vdb_folder :
                    for vdb_file in os.listdir(vdb_analyse):
                        vdb_final_name = vdb_file.split(".")[0]
                        vdb_names.append(vdb_final_name)
                        vdb_files.append(vdb_file)
                    vdb_list.append(vdb_analyse)
        if vdb_files !=[] :
            # __create groups from folders
            for group_name in group_names :
                cmds.createNode('transform',n=group_name)
            for vdb in vdb_names : 
                open_vdb = rfm2.api.nodes.create_openvdb()
                cmds.rename(open_vdb,vdb+"_VdbRead")
                input_path = vdb_path+vdb.split("_")[0]+"/"+vdb+".vdb"
                vdb_connections = cmds.listConnections(sh=True)
                for vdb_connection in vdb_connections :
                    if "Shape" in vdb_connection :
                        cmds.setAttr(vdb_connection+".ActiveValueBoundingBox",0)
                        cmds.setAttr(vdb_connection+".LeafNodes",0)
                        cmds.setAttr(vdb_connection+".ActiveTiles",0)
                        cmds.setAttr(vdb_connection+".ActiveVoxels",1)
                        pxr_volumes = cmds.listConnections(vdb_connection,type="shadingEngine")
                        for pxr_volume in pxr_volumes :
                            cmds.disconnectAttr(pxr_volume+".message", vdb_connection+".rman__torattr___customShadingGroup")
                        for clouds_shader in clouds_shaders :
                            cmds.connectAttr(clouds_shader+".message", vdb_connection+".rman__torattr___customShadingGroup")
                        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
                        vdb_visualise_parent = cmds.listRelatives(vdb_connection,p=True)
                        vdb_visualise_parent_good_name = cmds.rename(vdb_visualise_parent,vdb)
                cmds.setAttr(vdb+"_VdbRead"+".VdbFilePath",input_path,type="string")
                vdb_forename = vdb.split("_")[0]
                for group_name in group_names :
                    if vdb_forename in group_name : 
                        cmds.parent(vdb_visualise_parent_good_name,group_name)
                print(vdb_visualise_parent_good_name)
            selection = cmds.ls(type="OpenVDBVisualize")
            cmds.select(selection)
            volume_aggregate_rman  = rfm2.api.nodes.create_volume_aggregate_set()
            cmds.setAttr("PxrPathTracer.volumeAggregate",volume_aggregate_rman,type="string")
            print(group_name)
            
        else :
            return cmds.inViewMessage(amg=error_message_files,f=True)        
    else :
        return cmds.inViewMessage(amg=error_message_folder,f=True)