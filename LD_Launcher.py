        # Import the Maya commands library
from cProfile import label
from maya import cmds
from functools import partial
import os
import re
import sys
import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup
import maya.app.renderSetup.model.connectionOverride as connectionOverride
import maya.app.renderSetup.model.modelCmds as modelCmds
import maya.app.renderSetup.views.overrideUtils as utils

        # CREATING A UI CLASS
class LD_Window(object) :
        #---------------------------------------------Constructor---------------------------------------------#
                #---------------------------------------------Function for Buttons---------------------------------------------#   
    def buttonPressed(*args):
            print("Button Pressed")

    def __init__(self):
    
        #-------------------------Variables for Layout-------------------------#
        #Var for the window
        self.window = "LD_Window"
        self.title = "LD Render Launcher v1.7"
        self.width = 400
        self.height = 200        
        self.sizeUI = (self.width,self.height)
        self.iconPath = '//Storage/esma/3D4/paperPlane/12_script/_liamos/icons/PP_R_Launcher.png'
        colorLayout= (0.7,0.2,0.1)
        colorButton= (0.65,0.25,0.1)
        #Var for the seperators
        self.smallSep = 20
        self.medSep = 40
        self.bigSep = 60
        #Checking if the window exists
        if cmds.window(self.window, exists=True) :
            (
            cmds.deleteUI(self.window)
            )
        #---------------------------------------------Creation of the window---------------------------------------------#
        self.window = cmds.workspaceControl( self.window, label=self.title,iw=self.width,ih=self.height)
        
        self.form= cmds.formLayout(nd=100)
        #------------------------#
        sep_before_title = cmds.separator( height=self.smallSep)
        #-------------------------Title and Logo-------------------------#
        title = cmds.text(self.title)
        #------------------------#
        sep_after_title = cmds.separator( height=self.smallSep)
        #-------------------------Menu Ratio Format-------------------------#
        #Var for Ratio Format 
        self.bigRatioFormat = "2048x858"
        self.medRatioFormat = "1280x540"
        self.smallRatioFormat = "540x360"
        #Creation of the commands
        ratioLayout = cmds.frameLayout( label="Ratio & Cameras", collapsable=True, cl=False, bgc=colorLayout, borderVisible=True, p =self.form)
        cmds.separator( style='none' )
        cmds.rowColumnLayout(nc=2,cs=([2,(self.width/30)],[1,(self.width/30)]), p=ratioLayout)
        self.RF = cmds.optionMenu("RatioFormat", l= "Ratio :", h=20, ann="Choisir le format de sortie de votre séquence",cc = self.ratioFormatChanger)
        self.FormatMenuB = cmds.menuItem(l=self.bigRatioFormat)
        self.FormatMenuM =cmds.menuItem(l=self.medRatioFormat)
        self.FormatMenuS = cmds.menuItem(l=self.smallRatioFormat)
        self.cameraMenu = cmds.optionMenu("Cameras", l= "Cameras :", h=20, ann="Choisir la caméra de votre séquence", cc= self.camRender)
        self.cameraItem = cmds.menuItem(l="CHOISIR LA CAMERA --")
        self.readCam()
        cmds.separator( style='none', p=ratioLayout)
        cmds.setParent( self.form)
    
        #------------------------#
        cmds.separator( height=self.smallSep)
        #------------------------#
        #-------------------------Menu Animation-------------------------#
        
        timeRangeLayout = cmds.frameLayout( label="Time Range", collapsable=True, cl=False, bgc=colorLayout,borderVisible=True,p =self.form)
        cmds.separator( style='none')
        self.current_frame_radio = cmds.radioButtonGrp("test",label="Render Type:", labelArray2=["Current Frame", "Animation"],adj=True,cal=[1,"center"], numberOfRadioButtons=2, select=2, on1=lambda *args: self.switchRenderSettingsMode("Current Frame"), on2=lambda *args: self.switchRenderSettingsMode("Animation"))
        playbackLayout = cmds.rowColumnLayout(nc=3, cw=[(1,100),(2,100),(3,100)],co=[(1,'left',3)],cs=([2,3],[3,3]),adj=True)
        cmds.text(l='Time Range :')
        #Getting the actual Time Range
        self.start = cmds.playbackOptions(q=True,minTime=True)
        self.end = cmds.playbackOptions(q=True,maxTime=True)
        #Printing the actual Time Range in the intField
        self.startTime = cmds.intField('startTime',minValue=0,maxValue=10000, v=self.start),
        self.endTime = cmds.intField('endTime',minValue=0,maxValue=10000, v=self.end)
        cmds.separator( style='none',height=3, p=timeRangeLayout) 
        cmds.setParent(timeRangeLayout)   
        cmds.button(l='Appliquer',command=self.timeRangeChanger)

        #------------------------#
        cmds.separator( height=3)	
        #------------------------#

        #-------------------------Menu Lookdev-------------------------# 
        lookdevLayout = cmds.frameLayout( label="Lookdev Options", collapsable=True, cl=False, bgc=colorLayout,borderVisible=True,p =self.form)
        rclLookdev = cmds.rowColumnLayout( nc=2, adjustableColumn=True,cat=[(1,"both",10),(2,"both",10)] )
        cmds.separator(style='none', height=3)
        cmds.separator(style='none', height=3)
        rclLPE = cmds.rowColumnLayout( nc=1, adjustableColumn=True,p=rclLookdev)
        cmds.text("LPE",p=rclLPE)
        self.LPEName = cmds.textField('Nom du LPE',p=rclLPE)
        cmds.separator(style='none', height=3,p=rclLPE)
        cmds.button(l='Ajouter à la sélection',c=self.getLPEName,p=rclLPE)
        rclCC = cmds.rowColumnLayout( nc=1, adjustableColumn=True,p=rclLookdev)
        checkCycles = cmds.text("Check Cycles",p=rclCC)
        cmds.separator(style='none', height=3,p=rclCC)
        cycleCheckButton = cmds.button (l="Checker Cycles de la selection", c=self.checkShadingCycle,p=rclCC)
       
        


        cmds.setParent( self.form)
        #------------------------#
        sep_rendre = cmds.separator( height=2,p=self.form)
        #------------------------#

        #-------------------------Menu Render-------------------------# 
        renderLayout = cmds.frameLayout( label="Render", collapsable=True, cl=False, bgc=colorLayout,borderVisible=True,p=self.form)
        renderShelf = cmds.shelfTabLayout(p=renderLayout)

        renderUses = cmds.rowColumnLayout('Render Options',adj=True,p=renderShelf)
        cmds.setParent(renderUses)
        cmds.separator( style='none', height=3)
        cmds.text("Subdivide Options :")
        cmds.separator( style='none', height=3)
        rmanLayout = cmds.rowColumnLayout( nc=2,adj=True,cat=[(1,"both",10),(2,"both",10)] )
        rmanUnSubdivButton = cmds.button(l='Annuler toute les subdivisons',ann="Annuler toutes les subdivisons Catmull And Clark", c = self.rmanUnSubdiv,ebg = True, bgc = colorButton, p=rmanLayout)
        rmanSubdivSelectedButton = cmds.button(l='Subdiviser la selection',ann="Sélectionner vos meshes pour applique la subdivision de rendu", c = self.rmanSubdivSelected,ebg = True, p =rmanLayout)
        cmds.separator( style='none',height=5)
        cmds.separator( style='none',height=5)
        rmanDisp = cmds.rowColumnLayout('Render Options',adj=True,p=renderUses)
        cmds.text("Displace option : ",p=rmanDisp)
        cmds.separator( style='none', height=3)
        discoDispButton = cmds.button(l="Déco le Displace", c=self.discoDisplace,p=rmanDisp)
        cmds.separator( style='none', height=6)
        rmanSettings = cmds.rowColumnLayout('Render Options',adj=True,p=renderUses)
        cmds.text("Render Uses : ",p=rmanSettings)
        cmds.separator( style='none', height=3)
        rmanSettingsLayout = cmds.rowColumnLayout( nc=2,adj=True,cat=[(1,"both",10),(2,"both",10)])
        cmds.button(l="Cryptomattes to Sample Filters", c=partial(self.crypto_creator,textN="StatutCrypto"))
        cmds.button(l="Accumulate Opacity",c=partial(self.accumulateOpacity,textN="SatutAcc"))


        renderCheckUses = cmds.rowColumnLayout('Render Check Up ',adj=True,p=renderShelf)
        cmds.separator( style='none', height=3,p=renderCheckUses)
        rclCheck = cmds.rowColumnLayout(nc=3,adj=True,cat=[(1,"both",3),(2,"both",3)],cw=[(1,60),(2,60),(3,100)],p=renderCheckUses)

        cmds.text(l="Accumulate Opacity --",al='left',p=rclCheck)
        cmds.text("SatutAcc",l="STATUT",bgc=[1, 0, 0],al='left',p=rclCheck)
        cmds.button(l="FIX",c=partial(self.accumulateOpacity,textN="SatutAcc"),p=rclCheck)

        cmds.text("cryptomattes",l="Sample Filters : Cryptos --",al='left',p=rclCheck)
        cmds.text("StatutCrypto",l="STATUT",al='left',bgc=[1, 0, 0],p=rclCheck)
        cmds.button(l="FIX",c=partial(self.crypto_creator,textN='StatutCrypto'),p=rclCheck)

        cmds.text("incrementalSamples",l="Incremental Samples : Off --",al='left',p=rclCheck)
        cmds.text("StatutIncremental",l="STATUT",al='left',bgc=[1, 0, 0],p=rclCheck)
        cmds.button(l="FIX",c=partial(self.incremental,textN="StatutIncremental"),p=rclCheck)

        cmds.text("cameraZDepth",l="Camera Z Depth : On --",al='left',p=rclCheck)
        cmds.text("StatutCZDepth",l="STATUT",al='left',bgc=[1, 0, 0],p=rclCheck)
        cmds.button(l="FIX",c=partial(self.camera_depth,textN="StatutCZDepth"),p=rclCheck)

        cmds.text("cameraDOF",l="Camera Depth Of Field : On --",al='left',p=rclCheck)
        cmds.text("StatutCDOF",l="STATUT",al='left',bgc=[1, 0, 0],p=rclCheck)
        cmds.button(l="FIX",c=partial(self.camera_dof,textN="StatutCDOF"),p=rclCheck)

        cmds.text("motionBlur",l="Motion Blur and Camera Blur : On --",al='left',p=rclCheck)
        cmds.text("StatutMB",l="STATUT",al='left',bgc=[1, 0, 0],p=rclCheck)
        cmds.button(l="FIX",c=partial(self.camera_dof,textN="StatutMB"),p=rclCheck)   

        cmds.text("cameraBokeh",l="Camera Bokeh : On --",al='left',p=rclCheck)
        cmds.text("StatutBokeh",l="STATUT",al='left',bgc=[1, 0, 0],p=rclCheck)
        cmds.button(l="FIX",c=partial(self.bokehs,textN="StatutBokeh"),p=rclCheck)

        cmds.text("spacelfill",l="Bucket Order : Spacefill --",al='left',p=rclCheck)
        cmds.text("StatutBucket",l="STATUT",al='left',bgc=[1, 0, 0],p=rclCheck)
        cmds.button(l="FIX",c=partial(self.bucket_spacefill,textN="StatutBucket"),p=rclCheck)

        cmds.text("spool",l="Spool : Tractor --",al='left',p=rclCheck)
        cmds.text("StatutTractor",l="STATUT",al='left',bgc=[1, 0, 0],p=rclCheck)
        cmds.button(l="FIX",c=partial(self.spool_tractor,textN="StatutTractor"),p=rclCheck)

        cmds.text("frame_per_server",l="Frame Per Server : 1 --",al='left',p=rclCheck)
        cmds.text("StatutFPS",l="STATUT",al='left',bgc=[1, 0, 0],p=rclCheck)
        cmds.button(l="FIX",c=partial(self.frame_per_sever,textN="StatutFPS"),p=rclCheck)

        cmds.text("project",l="Project : PaperPlane",al='left',p=rclCheck)
        cmds.text("statutProject",l="STATUT",al='left',bgc=[1, 0, 0],p=rclCheck)
        cmds.button(l="FIX",c=partial(self.project_setter,textN="statutProject"),p=rclCheck)

        rclReload = cmds.rowColumnLayout(nc=1,adj=True,p=renderCheckUses)
        cmds.setParent(rclReload)
        cmds.button(l='/// --- RELOAD --- ///',p=rclReload,c=task_checker)
        cmds.separator(st = "doubleDash")
        cmds.button(l='Visualizer Mode',p=rclReload,c=self.visualizer_mode)
        cmds.setParent("..")

        lights = cmds.rowColumnLayout('Lights',adj=True,p=renderShelf)
        rclLight = cmds.rowColumnLayout(adj=True,p=lights)
        cmds.button(l='Locator/Light',c=self.locator_to_light_baker,p=rclLight)
    
        #-------------------------Menu Fermer-------------------------# 
        close_button = cmds.button( label='Fermer', command=('cmds.deleteUI(\"' + self.window + '\", window=True)'),p=self.form )
        #------------------------#
        sep_final = cmds.separator( height=self.smallSep,p=self.form)
        #-------------------------Edit Layout-------------------------# 
        finalLayout = cmds.formLayout(self.form, edit=True,
                        attachForm=[(sep_before_title,'left',5),(sep_before_title,'right',5),
                                    (title,'top',0), (title,'left', 5), (title,'right',5),
                                    (ratioLayout,'left',0),(ratioLayout,'right',0),
                                    (timeRangeLayout,'left',0),(timeRangeLayout,'right',0),
                                    (lookdevLayout,'left',0),(lookdevLayout,'right',0),
                                    (renderLayout,'left',0),(renderLayout,'right',0),
                                    (close_button, 'left', 0), (close_button, 'bottom', 10), (close_button, 'right', 0),
                                    
                        ],
                        attachControl=[(sep_before_title,'bottom',3,title),
                                       (sep_after_title,'top',0,title),
                                       (ratioLayout,'top',3,sep_after_title),
                                       (timeRangeLayout,'top',10,ratioLayout),
                                       (lookdevLayout,'top',10,timeRangeLayout),
                                       (sep_rendre,'top',5,lookdevLayout),
                                       (renderLayout,'top',10,sep_rendre),
                                       (close_button,'top',10,renderLayout),
                                       (sep_final, 'top',5, close_button),

                        ])
        #-------------------------Show Window-------------------------# 
        cmds.showWindow()
    #---------------------------------------------Function for Ratio Format---------------------------------------------#
    def ratioFormatChanger(self,*args):
        format = cmds.optionMenu(self.RF, q=True, v=True)
        print(format)
        
        newWidth, newHeight = re.split("x",format)
    
        cmds.setAttr("defaultResolution.width", int(newWidth))
        cmds.setAttr("defaultResolution.height", int(newHeight))
        cmds.setAttr("defaultResolution.deviceAspectRatio" , (int(newWidth) / int(newHeight)))
        cmds.setAttr("defaultResolution.lockDeviceAspectRatio", 0)
        cmds.setAttr("defaultResolution.pixelAspect", 1.0)
    #---------------------------------------------Function for TimeChange---------------------------------------------#
    def timeRangeChanger(self,*args): 
        #Gets New start and end times stored in the intFiled
        startTimeUp = cmds.intField(self.startTime, q=True,v=True)
        endTimeUp = cmds.intField(self.endTime, q=True,v=True)
        #Change time for the range in the viewport
        cmds.playbackOptions(e=True,minTime=startTimeUp, maxTime=endTimeUp)
        cmds.playbackOptions(e=True,animationStartTime=startTimeUp, animationEndTime=endTimeUp)
        #Change time for the range for the render
        self.newStartFrame= cmds.setAttr('defaultRenderGlobals.startFrame',startTimeUp)
        self.newEndFrame= cmds.setAttr('defaultRenderGlobals.endFrame',endTimeUp)   
    #---------------------------------------------Function for Switch from Current Frame to Animation---------------------------------------------#    
    def switchRenderSettingsMode(self,mode):
        if mode == "Animation":
            cmds.setAttr("defaultRenderGlobals.animation", 1)

        elif mode == "Current Frame":
            cmds.setAttr("defaultRenderGlobals.animation", 0)
            askCurrentTime = cmds.currentTime( query=True )
            newCurrentTime = cmds.currentTime(askCurrentTime, e=True)
            print(newCurrentTime)
    #---------------------------------------------Functions for Cam Selecter---------------------------------------------#
    def updateOptionMenu(self,*args):
        self.camera = cmds.optionMenu("Cameras", query=True, value=True)
        #cmds.lookThru(self.camera)
        print(self.camera)
    def readCam(self,*args):
        allCameras = cmds.ls(type=('camera'), l=True)
        startup_cameras = [self.cameraShape for self.cameraShape in allCameras if cmds.camera(cmds.listRelatives(self.cameraShape, parent=True, s=False)[0], startupCamera=True, q=True)]
        non_startup_cameras = list(set(allCameras) - set(startup_cameras))
        for self.cameraShape in non_startup_cameras:
            cam_name = self.cameraShape.rpartition("|")[-1].rstrip(" Shape")
            cmds.menuItem(label=cam_name, parent="Cameras")              
    def camRender(self,*args):
        self.updateOptionMenu()

        cams = cmds.listCameras(perspective=True)

        for cam in cams:
            isRenderable = cmds.getAttr(cam + ".renderable")
            if isRenderable:
                cmds.setAttr(cam + ".renderable", 0)
        camRender = self.camera
        cmds.listRelatives(camRender, type="camera", s=True, fullPath=True)[0]
        cmds.setAttr(camRender + ".renderable", 1)
    #---------------------------------------------Functions for LPE and Cycles---------------------------------------------#
    def getLPEName(self,*args):
        LPEName = cmds.textField(self.LPEName, q=True,tx=True)
        selections = cmds.ls(selection=True)
        lpeGroupName = LPEName
        for selection in selections : 
            cmds.setAttr("{}.rman_lpeGroup".format(selection),lpeGroupName, type= "string")
    def getRenderLayer(self,*args):
        self.current_render_layer = cmds.optionMenu(self.renderLayerMenu, query=True, value=True)
        cmds.editRenderLayerGlobals(currentRenderLayer=self.current_render_layer)
        currentMinSamples = cmds.getAttr('rmanGlobals.hider_minSamples')
        currentMaxSamples = cmds.getAttr('rmanGlobals.hider_maxSamples')
        currentVariance = cmds.getAttr('rmanGlobals.ri_pixelVariance')
        cmds.intSliderGrp(self.minSample, edit=True, value=currentMinSamples)
        cmds.intSliderGrp(self.maxSample, edit=True, value=currentMaxSamples)
        cmds.floatSliderGrp(self.pixVar, edit=True, value=currentVariance)
    def is_default_render_layer(self,*args):
        self.current_render_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
        if self.current_render_layer == "defaultRenderLayer":
            return True
        return False 
    def checkShadingCycle(*args):
        selectionList = cmds.ls(sl=True,an=True)
        for obj in selectionList : 
            attributes = cmds.listConnections(obj,s=True,d=True,p=False)
            print(attributes)
            for attribute in attributes : 
                    if attribute == obj :
                        print ("Le Node " + obj +" créer un CYCLE, corrige le sac à merde ! ")
                        cmds.select(obj)
    #---------------------------------------------Functions for Renderman Subdivider---------------------------------------------#
    def rmanSubdivSelected(self,*args):
        #Lists the transform nodes of all selected objects
        selected_nodes = cmds.ls(selection=True)
        selected_descendants = cmds.listRelatives(selected_nodes,ad=True)
        print(selected_descendants)
        shapes = []
        selected_shapes = cmds.ls(selected_descendants,shapes=True)
        for selected_shape in selected_shapes :
            shapes.append(selected_shape)      
        print(shapes)
        for shape in shapes :
            cmds.setAttr("{}.rman_subdivScheme".format(shape), 1)
    def rmanUnSubdiv(self,*args):
        selMeshes = cmds.ls(type='mesh', dag=1, ni=1)

        for selMesh in selMeshes:
                cmds.setAttr("%s.rman_subdivScheme" % selMesh, 0)       
    def discoDisplace(self,*args):
        selections = cmds.ls(sl=True)
        for selection in selections :
            shapes = cmds.listRelatives(selection,c=True,ad=True,type='shape')
            print(shapes)
            for shape in shapes :
                materials = cmds.listConnections(shape,type='shadingEngine')
                print(materials)
                for material in materials :
                    disps = cmds.listConnections(material,type="PxrDisplace")
                    print(disps)
                    if disps == None :
                        return
                    else :
                        for disp in disps :		
                            breakConnections = cmds.disconnectAttr(disp+".outColor",material+".rman__displacement")
                            self.shrekonoPrint()
    #---------------------------------------------Functions for Light Baking---------------------------------------------#
    def locator_to_light_baker(self,*args):
        #__get the selected geo and the selected light seperated
        select = cmds.ls(sl=True)
        select_clean = cmds.listRelatives(select,c=True)
        select_shapes = cmds.ls(select_clean,shapes=True)
        select_geos = []
        select_lights = []
        for select_shape in select_shapes :
            if "ABCReady" in select_shape :
                select_geos.append(select_shape)
            if "light" in select_shape:
                select_lights.append(select_shape)
                
        if select_geos == [] : 
            print("STP selectionne un ABC !")
        if select_lights == [] : 
            print("STP selectionne une Light !")
        else :
            # select first vertex of the mesh 
            for select_geo in select_geos :
                loc = cmds.spaceLocator(name="loc_"+select_geo+"_info_to_lights")
                vertex_geo_sel = cmds.select(select_geo+".vtx[0]")
                vertex_geo = cmds.ls(sl=True,fl=True)
                cmds.pointOnPolyConstraint(vertex_geo,loc)
                for select_light in select_lights : 
                    lr_light = cmds.listRelatives(select_light,p=True)
                    light_transform = cmds.ls(lr_light,fl=True)
                    cmds.parentConstraint(loc,light_transform,mo=True)
            cmds.select(clear=True)
            #__bake locator mvmt
            start_frame = cmds.playbackOptions(q=True,minTime=True)
            end_frame = cmds.playbackOptions(q=True,maxTime=True)
            cmds.bakeResults(loc,t=(start_frame,end_frame))
            cmds.delete(loc[0] + '*Constraint*')
    #---------------------------------------------Functions for Fixing---------------------------------------------#
    def accumulateOpacity(self,*args,textN=""):
        print(textN)
        cmds.setAttr("PxrPathTracer.accumOpacity",1)
    def accumulateOpacity(self,*args,textN=""):
        print(textN)
        cmds.setAttr("PxrPathTracer.accumOpacity",1)
        change_color(textN=textN)
        cmds.inViewMessage(amg="Accumulate Opacity -- ON --",pos="midCenter",f=True)
    def bucket_spacefill(self,*arg,textN=""):
        cmds.setAttr("rmanGlobals.opt_bucket_order","spacefill",type="string")
        change_color(textN=textN)
        cmds.inViewMessage(amg="Bucket Type -- spacefill --",pos="midCenter",f=True)
    def spool_tractor(self,*arg,textN=""):
        cmds.optionVar(sv=('rfmRenderBatchQueue','Tractor'))
        change_color(textN=textN)
        cmds.inViewMessage(amg="Spool -- tractor --",pos="midCenter",f=True)
    def frame_per_sever(self,*arg,textN=""):
        cmds.optionVar(iv=('rfmRenderBatchFrameChunk',1))
        change_color(textN=textN)
        cmds.inViewMessage(amg="Frame Per Server -- 1 --",pos="midCenter",f=True)
    def project_setter(self,*arg,textN=""):
        cmds.optionVar(sv=("rfmTractorProjects","paperplane"))
        change_color(textN=textN)
        cmds.inViewMessage(amg="Project Set -- paperplane --",pos="midCenter",f=True)
    def crypto_creator(self,*arg,textN=""):
        crypto_path_name = "path"
        crypto_mat_name = "mat"
        crypto_name_list = [crypto_path_name,crypto_mat_name]
        rmanG = "rmanGlobals"
        for crypto_name in crypto_name_list :
            i = crypto_name_list.index(crypto_name)
            crypto_node = cmds.createNode('PxrCryptomatte')
            if i ==0 :
                layer_valid = cmds.setAttr(crypto_node+".layer","identifier:name",type="string")
                print(layer_valid)
            if i == 1 :
                layer_valid = cmds.setAttr(crypto_node+".layer","user:__materialid",type="string")
                print(layer_valid)
            cmds.setAttr(crypto_node+".filename","<imagedir>/cryptomatte_"+crypto_name+".<layer>.<f4>.exr",type="string")
            cmds.connectAttr(crypto_node+".message",rmanG+".sampleFilters["+str(i)+"]")
            change_color(textN=textN)
            cmds.inViewMessage(amg="Cryptomattes in sample filters -- ON --",pos="midCenter",f=True)
    def incremental(self,*arg,textN=""):
        cmds.setAttr("rmanGlobals.hider_incremental",0)
        change_color(textN=textN)
        cmds.inViewMessage(amg="Incremental Samples -- OFF --",pos="midCenter",f=True)
    def camera_depth(self,*arg,textN=""):
        cameras = cmds.ls(type="camera")
        for camera in cameras :
            if "renderCam" in camera :
                cmds.setAttr(camera+".depth", 1)
                change_color(textN=textN)
                cmds.inViewMessage(amg="Z Depth Renderable -- ON --",pos="midCenter",f=True)
                return
            else:
                cmds.inViewMessage(amg="Il faut selectionner une camera renderable.",pos="midCenter",f=True)
    def camera_dof(self,*arg,textN=""):
        cameras = cmds.ls(type="camera")
        for camera in cameras :
            if "renderCam" in camera :
                cmds.setAttr(camera+".depthOfField", 1)
                change_color(textN=textN)
                cmds.inViewMessage(amg="DOF Renderable -- ON --",pos="midCenter",f=True)
                return 
            else:
                cmds.inViewMessage(amg="Il faut selectionner une camera renderable.",pos="midCenter",f=True)   
    def bokehs(self,*arg,textN=""):
        cameras = cmds.ls(type='camera')
        for camera in cameras :
            isRenderable = cmds.getAttr(camera+'.renderable')
            if isRenderable == 1 :
                cmds.setAttr(camera+".rman_apertureSides",9)
                cmds.setAttr(camera+".rman_apertureRoundness",1)
                cmds.setAttr(camera+".rman_apertureDensity",0.6)
                cmds.setAttr(camera+".rman_dofaspect",0.6)
                change_color(textN=textN)
                cmds.inViewMessage(amg="Bokeh -- ON --",pos="midCenter",f=True)
                return
            else :
                cmds.inViewMessage(amg="Il faut selectionner une camera renderable.",pos="midCenter",f=True)
    def pxr_visualizer(self,*arg):
        pxr_viz = "PxrVisualizer"
        in_connect_list = cmds.listConnections("rmanGlobals.ri_integrator")
        for in_connect in in_connect_list :
            cmds.disconnectAttr(in_connect +".msg","rmanGlobals.ri_integrator")
        cmds.connectAttr(pxr_viz+".msg","rmanGlobals.ri_integrator")
        cmds.setAttr(pxr_viz+".style","shaded",type="string")
        cmds.setAttr(pxr_viz+".wireframe", True)
        cmds.setAttr(pxr_viz+".wireframeColor", 1,0,0)
        cmds.setAttr(pxr_viz+".wireframeOpacity", 1)
        cmds.setAttr(pxr_viz+".wireframeWidth", 0.5)
    def motion_blur(self,*arg,textN=""):
        rmanG = "rmanGlobals"
        cmds.setAttr(rmanG+".hider_minSamples",32)
        cmds.setAttr(rmanG+".hider_maxSamples",64)
        cmds.setAttr(rmanG+".ri_pixelVariance",0.15)
        cmds.setAttr(rmanG+".motionBlur",1)
        cmds.setAttr(rmanG+".cameraBlur",1)
        cmds.setAttr(rmanG+".shutterTiming",2)
    def visualizer_mode(self,*arg):
        self.pxr_visualizer()
        self.motion_blur()
        self.bucket_spacefill(textN="StatutBucket")
        cmds.optionVar(sv=('rfmRenderBatchQueue','Local Queue'))
        cmds.optionVar(iv=('rfmRenderBatchFrameChunk',500))
        cmds.optionVar(sv=("rfmTractorProjects",""))
        self.camera_dof(textN="StatutCDOF")
        self.incremental(textN="StatutIncremental")
        cmds.inViewMessage(amg="VISUALIZER MODE -- ON ",f=True)
    #---------------------------------------------Update the renderer---------------------------------------------#
    def UpdateRenderer(*args):
        cmds.setAttr("defaultRenderGlobals.currentRenderer", "renderman", type="string")
    def UpdateInnerSettings(*args):
        cmds.setAttr("defaultRenderGlobals.animation", 1)

        cmds.setAttr("defaultResolution.width", 2048)
        cmds.setAttr("defaultResolution.height", 858)
        cmds.setAttr("defaultResolution.deviceAspectRatio" , (2048 / 858))
        cmds.setAttr("defaultResolution.lockDeviceAspectRatio", 0)
        cmds.setAttr("defaultResolution.pixelAspect", 1.0)
        #attrInte = cmds.setAttr("defaultRenderGlobals.ri_integrator","PxrPathTracer.message")
        #print (attrInte)
    #---------------------------------------------Functions to print---------------------------------------------#
    def peepoPrint (self,*args):
        a="\n⣿⣿⣿⣿⣿⣿⠿⢋⣥⣴⣶⣶⣶⣬⣙⠻⠟⣋⣭⣭⣭⣭⡙⠻⣿⣿⣿⣿⣿"
        b="\n⣿⣿⣿⣿⡿⢋⣴⣿⣿⠿⢟⣛⣛⣛⠿⢷⡹⣿⣿⣿⣿⣿⣿⣆⠹⣿⣿⣿⣿"
        c="\n⣿⣿⣿⡿⢁⣾⣿⣿⣴⣿⣿⣿⣿⠿⠿⠷⠥⠱⣶⣶⣶⣶⡶⠮⠤⣌⡙⢿⣿"
        d="\n⣿⡿⢛⡁⣾⣿⣿⣿⡿⢟⡫⢕⣪⡭⠥⢭⣭⣉⡂⣉⡒⣤⡭⡉⠩⣥⣰⠂⠹"
        e="\n⡟⢠⣿⣱⣿⣿⣿⣏⣛⢲⣾⣿⠃⠄⠐⠈⣿⣿⣿⣿⣿⣿⠄⠁⠃⢸⣿⣿⡧"
        f="\n⢠⣿⣿⣿⣿⣿⣿⣿⣿⣇⣊⠙⠳⠤⠤⠾⣟⠛⠍⣹⣛⣛⣢⣀⣠⣛⡯⢉⣰"
        g="\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡶⠶⢒⣠⣼⣿⣿⣛⠻⠛⢛⣛⠉⣴⣿⣿"
        h="\n⣿⣿⣿⣿⣿⣿⣿⡿⢛⡛⢿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡈⢿⣿"
        i="\n⣿⣿⣿⣿⣿⣿⣿⠸⣿⡻⢷⣍⣛⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢇⡘⣿"
        j="\n⣿⣿⣿⣿⣿⣿⣿⣷⣝⠻⠶⣬⣍⣛⣛⠓⠶⠶⠶⠤⠬⠭⠤⠶⠶⠞⠛⣡⣿"
        k="\n⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣬⣭⣍⣙⣛⣛⣛⠛⠛⠛⠿⠿⠿⠛⣠⣿⣿"
        l="\n⣦⣈⠉⢛⠻⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⣁⣴⣾⣿⣿⣿⣿"
        m="\n⣿⣿⣿⣶⣮⣭⣁⣒⣒⣒⠂⠠⠬⠭⠭⠭⢀⣀⣠⣄⡘⠿⣿⣿⣿⣿⣿⣿⣿"
        n="\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡈⢿⣿⣿⣿⣿⣿"
        o="\n         LA DISPLACE EST DECO           "
        cmds.inViewMessage(amg=a+b+c+d+e+f+g+h+i+j+k+l+m+n+o,f=True)  
    def shrekonoPrint(self,*args):
        a="\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"
        b="\n⣿⠟⠫⢻⣿⣿⣿⣿⢟⣩⡍⣙⠛⢛⣿⣿⣿⠛⠛⠛⠛⠻⣿⣿⣿⣿⣿⡿⢿⣿"
        c="\n⣿⠤⠄⠄⠙⢿⣿⣿⣿⡿⠿⠛⠛⢛⣧⣿⠇⠄⠂⠄⠄⠄⠘⣿⣿⣿⣿⠁⠄⢻"
        d="\n⣿⣿⣿⣿⣶⣄⣾⣿⢟⣼⠒⢲⡔⣺⣿⣧⠄⠄⣠⠤⢤⡀⠄⠟⠉⣠⣤⣤⣤⣾"
        e="\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣀⣬⣵⣿⣿⣿⣶⡤⠙⠄⠘⠃⠄⣴⣾⣿⣿⣿⣿⣿"
        f="\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢻⠿⢿⣿⣿⠿⠋⠁⠄⠂⠉⠒⢘⣿⣿⣿⣿⣿⣿⣿"
        g="\n⣿⣿⣿⣿⣿⣿⣿⣿⡿⣡⣷⣶⣤⣤⣀⡀⠄⠄⠄⠄⠄⠄⠄⣾⣿⣿⣿⣿⣿⣿"
        h="\n⣿⣿⣿⣿⣿⣿⣿⡿⣸⣿⣿⣿⣿⣿⣿⣿⣷⣦⣰⠄⠄⠄⠄⢾⠿⢿⣿⣿⣿⣿"
        i="\n⣿⡿⠋⣡⣾⣿⣿⣿⡟⠉⠉⠈⠉⠉⠉⠉⠉⠄⠄⠄⠑⠄⠄⠐⡇⠄⠈⠙⠛⠋"
        j="\n⠋⠄⣾⣿⣿⣿⣿⡿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢠⡇⠄⠄⠄⠄⠄"
        k="\n⠄⢸⣿⣿⣿⣿⣿⣯⠄⢠⡀⠄⠄⠄⠄⠄⠄⠄⠄⣀⠄⠄⠄⠄⠁⠄⠄⠄⠄⠄"
        l="\n⠁⢸⣿⣿⣿⣿⣿⣯⣧⣬⣿⣤⣐⣂⣄⣀⣠⡴⠖⠈⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄"
        m="\n⠈⠈⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣽⣉⡉⠉⠈⠁⠄⠁⠄⠄⠄⠄⡂⠄⠄⠄⠄⠄"
        n="\n⠄⠄⠙⣿⣿⠿⣿⣿⣿⣿⣷⡤⠈⠉⠉⠁⠄⠄⠄⠄⠄⠄⠄⠠⠔⠄⠄⠄⠄⠄"
        o="\n⠄⠄⠄⡈⢿⣷⣿⣿⢿⣿⣿⣷⡦⢤⡀⠄⠄⠄⠄⠄⠄⢐⣠⡿⠁⠄⠄⠄⠄⠄"
        p="\n    LE DISPLACE EST DECO MON GAAAH !!!  "
        cmds.inViewMessage(amg=a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p,f=True)  
    #---------------------------------------------Launch Initial Functions---------------------------------------------#
    UpdateRenderer()
    #UpdateInnerSettings()
        
      
#---------------------------------------------Launch Window---------------------------------------------#
LD_Launcher = LD_Window()
#---------------------------------------------Functions Global---------------------------------------------#
def change_color(*args,textN=""):
    current_color = cmds.text(textN, q=True, bgc=True)
    if current_color == [1, 0, 0]:
        cmds.text(textN, e=True, bgc=[0, 1, 0])
    else:
        cmds.inViewMessage(amg="Le statut de cette tâche est déjà validé.",pos="midCenter",f=True)
def task_checker(*args):
    accum_opacity_value = cmds.getAttr("PxrPathTracer.accumOpacity")
    print(accum_opacity_value)
    if accum_opacity_value == True :
        cmds.text("SatutAcc",e=True,bgc=[0, 1, 0])
    bucket_order = cmds.getAttr("rmanGlobals.opt_bucket_order")
    if bucket_order == "spacefill" :
        cmds.text("StatutBucket",e=True,bgc=[0, 1, 0])
    spool_value = cmds.optionVar(q="rfmRenderBatchQueue")
    if spool_value == "Tractor" :
        cmds.text("StatutTractor",e=True,bgc=[0, 1, 0])
    fps_value = cmds.optionVar(q='rfmRenderBatchFrameChunk')
    if fps_value == 1 :
        cmds.text("StatutFPS",e=True,bgc=[0, 1, 0])
    project_value = cmds.optionVar(q='rfmTractorProjects')
    if project_value == "paperplane" :
        cmds.text("statutProject",e=True,bgc=[0, 1, 0])
    crypto_value = cmds.listConnections("rmanGlobals.sampleFilters[0]",d=True)
    if crypto_value != None :
        cmds.text("StatutCrypto",e=True,bgc=[0, 1, 0])
    incremental_value = cmds.getAttr("rmanGlobals.hider_incremental")
    if incremental_value == 0 :
        cmds.text("StatutIncremental",e=True,bgc=[0, 1, 0])
    motion_blur = cmds.getAttr("rmanGlobals.motionBlur")
    if motion_blur == 1 :
        cmds.text("StatutMB",e=True,bgc=[0, 1, 0])        
    cameras = cmds.ls(type='camera')
    for camera in cameras :
        if "renderCam" in camera :
            isRenderable = cmds.getAttr(camera+'.renderable')
            if isRenderable == 1 :
                hasDepth = cmds.getAttr(camera+'.depth')
                if hasDepth == 1 :
                    print(camera)
                    cmds.text("StatutCZDepth",e=True,bgc=[0, 1, 0])
                hasDOF = cmds.getAttr(camera+".depthOfField")
                if hasDOF == 1 : 
                    cmds.text("StatutCDOF",e=True,bgc=[0, 1, 0])   
                if cmds.getAttr(camera+".rman_apertureSides") == 9 :
                    cmds.text("StatutBokeh",e=True,bgc=[0, 1, 0])                    
#---------------------------------------------Launch Sub-Tasks---------------------------------------------#
task_checker()

