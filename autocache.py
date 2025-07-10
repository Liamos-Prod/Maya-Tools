def autoCache(*arg, mode=""):
    # ___VARIABLES___ #
        # __QUERY CHECKBOXES
            # __get character checkboxes
    characters = ["charaLewis","charaKarl","charaJohn","charaDolphi"]
            # __set character lists
    setNames = []
    correctNames =[]
            # __get caches checkboxes
    cacheVar = ["Render","CFX","Int","Helices"]
    cacheCharaPrefix = "cacheChara"
    LODs = ["LOD01","LOD03"]
    cacheCharaRenderLOD1 = [cacheCharaPrefix+cacheVar[0]+"Lewis"+LODs[0],cacheCharaPrefix+cacheVar[0]+"John"+LODs[0],cacheCharaPrefix+cacheVar[0]+"Karl"+LODs[0],cacheCharaPrefix+cacheVar[0]+"Dolphi"+LODs[0]]
    cacheCharaRenderLOD3 = [cacheCharaPrefix+cacheVar[0]+"Lewis"+LODs[1],cacheCharaPrefix+cacheVar[0]+"John"+LODs[1],cacheCharaPrefix+cacheVar[0]+"Karl"+LODs[1],cacheCharaPrefix+cacheVar[0]+"Dolphi"+LODs[1]]
    cacheCharaCFX = [cacheCharaPrefix+cacheVar[1]+"Lewis",cacheCharaPrefix+cacheVar[1]+"John",cacheCharaPrefix+cacheVar[1]+"Karl",cacheCharaPrefix+cacheVar[1]+"Dolphi"]
    cacheCharaChildPrefix = "cacheCharaChild"
    cacheCharaChild = [cacheCharaChildPrefix+"Lewis",cacheCharaChildPrefix+"Karl"]
    cachePlanePrefix ="cachePlane"
    cachePlaneRender = [cachePlanePrefix+cacheVar[0]+"Lewis",cachePlanePrefix+cacheVar[0]+"John",cachePlanePrefix+cacheVar[0]+"Karl",cachePlanePrefix+cacheVar[0]+"Dolphi"]
    cachePlaneInt = [cachePlanePrefix+cacheVar[2]+"Lewis",cachePlanePrefix+cacheVar[2]+"John",cachePlanePrefix+cacheVar[2]+"Karl",cachePlanePrefix+cacheVar[2]+"Dolphi"]
    cachePlaneHelices = [cachePlanePrefix+cacheVar[3]+"Lewis",cachePlanePrefix+cacheVar[3]+"John",cachePlanePrefix+cacheVar[3]+"Karl",cachePlanePrefix+cacheVar[3]+"Dolphi"]
    cachePaperPlanePrefix ="cachePaperPlane"
    cachePaperPlane = [cachePaperPlanePrefix+"Lewis",cachePaperPlanePrefix+"Karl"]
            # __set cache list
    checkboxList = [cacheCharaRenderLOD1,cacheCharaRenderLOD3,cacheCharaCFX,cacheCharaChild,cachePlaneRender,cachePlaneInt,cachePlaneHelices,cachePaperPlane]
            # __get ABC infos
    if cmds.checkBox("uvWrite", query=True, value=True)==1:
        ABCuv = " -uvWrite"
    else:
        ABCuv = ""
    if cmds.checkBox("visibilityWrite", query=True, value=True)==1:
        ABCwv = " -writeVisibility"
    else:
        ABCwv = ""
    if cmds.checkBox("worldSpace", query=True, value=True)==1:
        ABCws = " -worldSpace"
    else:
        ABCws = ""

    ABCef = ""
            # __get time infos
    ABCstartTime = cmds.playbackOptions(q=True, min=True)
    ABCendTime = cmds.playbackOptions(q=True, max=True)
        # __SET VARIABLES FOR NAMES
            # __extension , setGeo and default variables
    setGeoCache = "setGeoCache_"
    ud = "_"
    lookdevs = ["_P_lookdev:","_P_Lookdev:"]
    rig = "_P_rig:"
    extension = ".abc"
    endAndExtension = "_P"+extension

            # __planes
    planeBritish = "spitfire_"
    planeGerman = "messerschmitt_"
    planes= [planeBritish,planeGerman]
                # __plane setGeo extensions
    planeRender = "_general_render"
    planeInt = "_int_render"
    planeIntMesserschmitt = "_int"
    planeHelices = "_helice_group"
    paperPlane = "_paperplane"
            # __characters
    adult = "_adult"
    child = "_child"
                # __charas setGeo extensions
    adultRender = "_adult_render"
    renderSuffixe = "_render"
    flatSuffixe = "_flat"
    adultCFX = "_adult_"
    CFXending = ["render", "flat"]
            # __cameras
    renderCam = "renderCam"
        # __GET AND CREATE PATH IF NONE EXISTENT
            # __query checkboxes
    path = cmds.textField( "FolderPath",q=True, text=True)
    folder = cmds.optionMenu("Folder" , q=True,v=True)
    name = cmds.textScrollList("assetName", q=True, si=True)
            # __define paths
    setProj = "/maya/cache/alembic/"
    try :
        fullPath = path+"/"+folder+"/"+name[0]+setProj
    except :
        unluckyErrorPrint()
            # __importCam variables to get the scene name
    scenePath = cmds.file(q=True,sn=True)
    sceneShotName = name[0]
    goodTerm = "renderCam_P.abc"
            # __cache folders variables
    cacheFolders = ["01_final/","02_cfx/","03_mush/"]
            # __create paths
    for cacheFolder in cacheFolders :
        childs=os.listdir(fullPath)
        if not cacheFolder in childs:
            try :
                os.mkdir(fullPath+cacheFolder)
                print (" file created ")
            except FileExistsError:
                pass
    finalPath = fullPath + cacheFolders[0]
    cfxPath = fullPath + cacheFolders[1]
            # __store path in clear variables
    savePlaceFinal = finalPath
    savePlaceCFX = cfxPath

    # ___FUNCTIONS___ #
        # __runAutoCache : gets all the needed informations from the selection, adds them to a list ready for export / import
    def runAutocache(mode=""):
        # __camera
        if cmds.checkBox("cacheCamera",q=True,v=True) == True :
            setProj = "/camera/"
            camPath = path+"/"+folder+"/"+sceneShotName+setProj
            savePath = camPath
            if mode == "export":
                backupCheckCam(path=savePath)
                exportCam(savePath)
            if mode == "import":
                importCam(savePath)


        # __loop in characters to get the ones checked ad add them to list
        for character in characters :
            if cmds.checkBox(character,q=True,v=True) == True :
                setNames.append(character)
        # __loop for the names checked and only gets the 'Name' without 'chara'
        for setName in setNames :
            goodNames = setName.split("chara")[-1]
            correctNames.append(goodNames)
        # __loop to check which checkbox associated with the 'Name' is checked
        for correctName in correctNames :
            print(correctName)
            for checkbox in checkboxList :
                for checkboxTrue in checkbox :
                    if cmds.checkBox(checkboxTrue,q=True,v=True) == True :
                        # __get a lower case name
                        lowerCaseName = str.lower(correctName)
                        # __check if the cache is for a plane part
                        if (cachePlanePrefix) in checkboxTrue :

                            # __define planes for charas
                            for plane in planes :
                                if ("Lewis" ) in correctName:
                                    plane = planeBritish
                                if ("John" ) in correctName:
                                    plane = planeBritish
                                if ("Karl") in correctName:
                                    plane = planeGerman
                                if ("Dolphi") in correctName:
                                    plane = planeGerman
                            # __get suffixe from mode
                            if mode == "export":
                                suffixe = rig
                            if mode == "import":
                                suffixe = lookdevs[0]
                            namespacePlane= plane + lowerCaseName + suffixe
                            if "Dolphi" in correctName :
                                if mode == "export" :
                                    namespacePlane= plane.capitalize() + lowerCaseName + suffixe
                            if "Karl" in correctName :
                                if mode == "export" :
                                    namespacePlane= plane.capitalize() + lowerCaseName + suffixe
                        # __check if the cache is for a character
                        if (cacheCharaPrefix) in checkboxTrue :
                            # __get suffixe from mode
                            if mode == "export":
                                suffixe = rig
                            if mode == "import":
                                suffixe = lookdevs[1]
                                if ("John") in correctName :
                                    suffixe = lookdevs[0]
                            # __apply proper namespaces for each chara
                            if ("Lewis" ) in correctName:
                                namespaceChara= lowerCaseName + adult + suffixe
                            if ("John" ) in correctName:
                                namespaceChara= lowerCaseName + suffixe
                            if ("Karl") in correctName:
                                namespaceChara= lowerCaseName + adult + suffixe
                            if ("Dolphi") in correctName:
                                namespaceChara= lowerCaseName + suffixe
                        # __get the LOD of the chara
                        for LOD in LODs :
                            if cmds.checkBox("cacheCharaRender"+correctName + LODs[0],q=True,v=True)==True :
                                LOD = LODs[0]
                            else :
                                LOD = LODs[1]


                        if (cacheCharaChildPrefix) in checkboxTrue :
                            if mode == "export":
                                suffixe = rig
                            if mode == "import":
                                suffixe = lookdevs[0]
                            namespaceCharaChild= lowerCaseName + child + suffixe
                        if (cachePaperPlanePrefix) in checkboxTrue :
                            if mode == "export":
                                suffixe = rig
                            if mode == "import":
                                suffixe = lookdevs[0]
                            namespacePaperPlane= lowerCaseName + str.lower(paperPlane) + suffixe

                        if checkboxTrue == "cacheCharaRender"+correctName + LOD:
                            if mode == "export":
                                cmds.optionMenu("charaAnimSel", e=True, v=correctName)
                                if cmds.checkBox("cacheCharaMaskLewis",q=True,v=True) == 1 :
                                    cmds.checkBox("OxygenMask",e=True, v=True)
                                else :
                                    cmds.checkBox("OxygenMask",e=True, v=False)
                                if correctName == "John" :
                                    cmds.checkBox("OxygenMask",e=True, v=True)
                                if correctName == "Karl" :
                                    LOD = LODs[1]
                                cmds.optionMenu("ExportAnimMode", e=True, v="render"+LOD)
                                SetParametreExport()
                            print(cmds.optionMenu("ExportAnimMode", q=True, v=True))
                            saveName = name[0] + ud + correctName + adultRender + endAndExtension
                            savePath =savePlaceFinal
                            savedCache = savePath+saveName
                            if cmds.namespace(exists=namespaceChara) :
                                cacheCharaRender = cmds.ls(namespaceChara + setGeoCache + lowerCaseName + adultRender + ud + LOD,an=True,l=True,type="objectSet")
                                if correctName == "John" :
                                    if LOD == LODs[0]:
                                        cacheCharaRender = cmds.ls(namespaceChara + setGeoCache + lowerCaseName + adultRender + ud + LOD,an=True,l=True,type="objectSet")
                                    else :
                                        cacheCharaRender = cmds.ls(namespaceChara + setGeoCache + lowerCaseName + renderSuffixe + ud + LOD,an=True,l=True,type="objectSet")
                                if correctName == "Karl" :
                                    cacheCharaRender = cmds.ls(namespaceChara + setGeoCache + lowerCaseName + adultRender,an=True,l=True,type="objectSet")
                            else:
                                cacheCharaRender = cmds.ls(setGeoCache + lowerCaseName + adultRender + ud + LOD,an=True,l=True,type="objectSet")
                                if correctName == "John" :
                                    if LOD == LODs[0]:
                                        print(LOD)
                                        cacheCharaRender = cmds.ls(setGeoCache + lowerCaseName + adultRender + ud + LOD,an=True,l=True,type="objectSet")
                                        print(setGeoCache + lowerCaseName + adultRender + ud + LOD)
                                    else :
                                        cacheCharaRender = cmds.ls(setGeoCache + lowerCaseName + renderSuffixe + ud + LOD,an=True,l=True,type="objectSet")
                                if correctName == "Karl" :
                                    cacheCharaRender = cmds.ls(setGeoCache + lowerCaseName + adultRender,an=True,l=True,type="objectSet")
                            cmds.select(cacheCharaRender)
                            print(LOD)
                            print(cacheCharaRender)
                            switchImportExport(saveName,savedCache,savePath,ABCef,selection=cacheCharaRender,mode=mode)

                        if checkboxTrue == "cacheCharaCFX"+correctName:
                            if mode == "export":
                                cmds.optionMenu("charaAnimSel", e=True, v=correctName)
                                if cmds.checkBox("cacheCharaMaskLewis",q=True,v=True) == 1 :
                                    cmds.checkBox("OxygenMask",e=True, v=True)
                                else :
                                    cmds.checkBox("OxygenMask",e=True, v=False)
                                if correctName == "John" :
                                    cmds.checkBox("OxygenMask",e=True, v=True)
                                    cmds.optionMenu("ExportAnimMode", e=True, v="render"+LODs[1])
                                if correctName == "Karl" :
                                    LOD = LODs[1]
                                cmds.optionMenu("ExportAnimMode", e=True, v="render"+LOD)
                                SetParametreExport()
                            saveName = name[0] + ud + correctName + adultCFX + CFXending[0] + endAndExtension
                            savePath = savePlaceCFX
                            print(savePath)
                            savedCache = savePath+saveName
                            if cmds.namespace(exists=namespaceChara) :
                                cacheCharaCFX = cmds.ls(namespaceChara + setGeoCache + lowerCaseName + adultCFX + CFXending[0] + ud + LODs[1],an=True,l=True,type="objectSet")
                                if correctName == "John" :
                                    cacheCharaCFX = cmds.ls(namespaceChara + setGeoCache + lowerCaseName + renderSuffixe +  ud + LODs[1],an=True,l=True,type="objectSet")
                                if correctName == "Karl" :
                                    cacheCharaCFX = cmds.ls(namespaceChara + setGeoCache + lowerCaseName + adultCFX + CFXending[0],an=True,l=True,type="objectSet")
                            else:
                                cacheCharaCFX = cmds.ls(setGeoCache + lowerCaseName + adultCFX + CFXending[0] + ud + LODs[1],an=True,l=True,type="objectSet")
                                if correctName == "John" :
                                    cacheCharaCFX = cmds.ls( setGeoCache + lowerCaseName + renderSuffixe + ud + LODs[1],an=True,l=True,type="objectSet")
                                if correctName == "Karl" :
                                    cacheCharaCFX = cmds.ls(setGeoCache + lowerCaseName + adultCFX + CFXending[0] ,an=True,l=True,type="objectSet")
                            cmds.select(cacheCharaCFX)
                            print(cacheCharaCFX)
                            switchImportExport(saveName,savedCache,savePath,ABCef,selection=cacheCharaCFX,mode=mode)
                            if mode == "export":
                                cmds.optionMenu("charaAnimSel", e=True, v=correctName)
                                if cmds.checkBox("cacheCharaMaskLewis",q=True,v=True) :
                                    cmds.checkBox("OxygenMask",e=True, v=True)
                                else :
                                    cmds.checkBox("OxygenMask",e=True, v=False)
                                if correctName == "John" :
                                    cmds.checkBox("OxygenMask",e=True, v=True)
                                cmds.optionMenu("ExportAnimMode", e=True, v="flat")
                                SetParametreExport()
                            saveName = name[0] + ud + correctName + adultCFX + CFXending[1] + endAndExtension
                            savePath = savePlaceCFX
                            savedCache = savePath+saveName
                            if cmds.namespace(exists=namespaceChara) :
                                cacheCharaCFX = cmds.ls(namespaceChara + setGeoCache + lowerCaseName + adultCFX + CFXending[1],an=True,l=True,type="objectSet")
                                if correctName == "John" :
                                    cacheCharaCFX = cmds.ls(namespaceChara + setGeoCache + lowerCaseName + flatSuffixe,an=True,l=True,type="objectSet")
                                if correctName == "Karl" :
                                    cacheCharaCFX = cmds.ls(namespaceChara + setGeoCache + lowerCaseName + adultCFX + CFXending[1],an=True,l=True,type="objectSet")
                            else:
                                cacheCharaCFX = cmds.ls(setGeoCache + lowerCaseName + adultCFX + CFXending[1] ,an=True,l=True,type="objectSet")
                                if correctName == "John" :
                                    cacheCharaCFX = cmds.ls(setGeoCache + lowerCaseName + flatSuffixe,an=True,l=True,type="objectSet")
                                if correctName == "Karl" :
                                    cacheCharaCFX = cmds.ls(setGeoCache + lowerCaseName + adultCFX + CFXending[1],an=True,l=True,type="objectSet")
                            cmds.select(cacheCharaCFX)
                            print(cacheCharaCFX)
                            switchImportExport(saveName,savedCache,savePath,ABCef,selection=cacheCharaCFX,mode=mode)

                        if checkboxTrue == "cacheCharaChild"+correctName:
                            saveName = name[0] + ud + correctName + child + endAndExtension
                            savePath =savePlaceFinal
                            savedCache = savePath+saveName
                            print(savedCache)
                            if cmds.namespace(exists=namespaceCharaChild) :
                                cacheCharaChild = cmds.ls(namespaceCharaChild + setGeoCache + lowerCaseName + child,an=True,l=True,type="objectSet")
                            else:
                                cacheCharaChild = cmds.ls(setGeoCache + lowerCaseName + child,an=True,l=True,type="objectSet")
                            cmds.select(cacheCharaChild)
                            switchImportExport(saveName,savedCache,savePath,ABCef,selection=cacheCharaChild,mode=mode)

                        if checkboxTrue == "cachePlaneRender"+correctName:
                            saveName = name[0] + ud + plane + correctName + planeRender + endAndExtension
                            print(plane)
                            savePath = savePlaceFinal
                            savedCache = savePath+saveName
                            print(namespacePlane)
                            if cmds.namespace(exists=namespacePlane) :
                                cachePlaneRender = cmds.ls(namespacePlane + setGeoCache + plane + lowerCaseName + planeRender,an=True,l=True,type="objectSet")
                            else :
                                cachePlaneRender = cmds.ls(setGeoCache + plane + lowerCaseName + planeRender,an=True,l=True,type="objectSet")
                            cmds.select(cachePlaneRender)
                            print(cachePlaneRender)
                            switchImportExport(saveName,savedCache,savePath,ABCef,selection=cachePlaneRender,mode=mode)

                        if checkboxTrue == "cachePlaneInt"+correctName:
                            saveName = name[0] + ud + plane + correctName + planeInt + endAndExtension
                            print(plane)
                            savePath = savePlaceFinal
                            savedCache = savePath+saveName
                            if cmds.namespace(exists=namespacePlane) :
                                cachePlaneInt = cmds.ls(namespacePlane + setGeoCache + plane + lowerCaseName + planeInt,an=True,l=True,type="objectSet")
                            else :
                                cachePlaneInt = cmds.ls(setGeoCache + plane + lowerCaseName + planeInt,an=True,l=True,type="objectSet")
                            cmds.select(cachePlaneInt)
                            print(cachePlaneInt)
                            switchImportExport(saveName,savedCache,savePath,ABCef,selection=cachePlaneInt,mode=mode)

                        if checkboxTrue == "cachePlaneHelices"+correctName:
                            if cmds.checkBox("eulerFilter", query=True, value=True)==1:
                                ABCefHelices = " -eulerFilter"
                            saveName = name[0] + ud + plane + correctName + planeHelices + endAndExtension
                            print(plane)
                            savePath = savePlaceFinal
                            savedCache = savePath+saveName
                            if cmds.namespace(exists=namespacePlane) :
                                cachePlaneHelices = cmds.ls(namespacePlane + setGeoCache + plane + lowerCaseName + planeHelices,an=True,l=True,type="objectSet")
                            else :
                                cachePlaneHelices = cmds.ls(setGeoCache + plane + lowerCaseName + planeHelices,an=True,l=True,type="objectSet")
                            cmds.select(cachePlaneHelices)
                            print(cachePlaneHelices)
                            switchImportExport(saveName,savedCache,savePath,ABCef = ABCefHelices,selection=cachePlaneHelices,mode=mode)

                        if checkboxTrue == "cachePaperPlane"+correctName:
                            saveName = name[0] + ud + correctName + paperPlane + endAndExtension
                            savePath =savePlaceFinal
                            savedCache = savePath+saveName
                            print(savedCache)
                            if cmds.namespace(exists=namespacePaperPlane) :
                                cachePaperPlane = cmds.ls(namespacePaperPlane + setGeoCache + lowerCaseName + paperPlane,an=True,l=True,type="objectSet")
                            else:
                                cachePaperPlane = cmds.ls(setGeoCache + lowerCaseName + paperPlane,an=True,l=True,type="objectSet")
                            cmds.select(cachePaperPlane)
                            switchImportExport(saveName,savedCache,savePath,ABCef,selection=cachePaperPlane,mode=mode)
        # __exportCam : exportCameraSelection
    def exportCam(savePath=""):
        allCameras = cmds.ls(type=('camera'), l=True)
        startup_cameras = [cameraShape for cameraShape in allCameras if cmds.camera(cmds.listRelatives(cameraShape, parent=True, s=False)[0], startupCamera=True, q=True)]
        non_startup_cameras = list(set(allCameras) - set(startup_cameras))
        for cameraShape in non_startup_cameras:
            cam_name = cameraShape
            if "renderCam" in cam_name :
                print(cam_name)
                camExports = cmds.listRelatives(cam_name,p=True)
                print(camExports)
                for camExport in camExports:
                    cmds.select(camExport)
                    savedName = cam_name.rpartition("|")[-1].replace(":","_").rpartition("_Shape")[0]+"_P.abc"
                    savedCache = savePath + savedName
                    print(savedCache)
                    ABCsel = ""
                    selection = cmds.ls(sl=True,l=True)
                    for element in selection:
                        ABCsel=ABCsel+" -root "+element
                        print(ABCsel)
                    cmds.AbcExport(j="-frameRange " + str(ABCstartTime) + " " + str(ABCendTime) + ABCws + ABCsel + " -ef " +" -file "+ savedCache )
        peepoPrint()
        # __importCam : importCameraSelection
    def importCam(savePath):
        result = []
        for root, dir, files in os.walk(savePath):
            for filename in files :
                if filename.endswith(goodTerm):
                    result.append(os.path.join(root, filename))
            print(result)
            for goodCam in result :
                print(goodCam)
                cmds.AbcImport(goodCam,m="import")
                camera_withoutext = goodCam.split(".abc")[0]
                camera_namealmostgood = camera_withoutext.split("/")[-1]
                camera_newname = camera_namealmostgood.split("_P")[0]
                print(camera_newname)
                camera_node = cmds.ls("renderCam_")
                print(camera_node)
                cmds.rename(camera_node,camera_newname)
            if not filename in files:
                shrekonoPrint()
            return
        # __backupCheckCam : creates a backup of your precedent camera abc if it exists
    def backupCheckCam(path,*args):
        childs=os.listdir(path+"/")
        print(path)
        if not "backup" in childs:
            os.mkdir(path+"/backup")
        for child in childs:
            if "_P" in child:
                print(child)
                index= len(os.listdir(path+"/"+"backup/"))+1
                baseSimp = child.split(".")[0]
                if index<10:
                    shutil.move(path+child, path+"backup/"+baseSimp+"_00"+str(index)+".abc")
                else:
                    shutil.move(path+child, path+"backup/"+baseSimp+"_0"+str(index)+".abc")
        # __launchCache : exports selection
    def launchCache(saveName,ABCef,savePlace):
        ABCsel = ""
        selection = cmds.ls(sl=True,sn=True)
        print(selection)
        if selection != [] :
            for element in selection:
                element = element.split( "|" )[-1]
                ABCsel=ABCsel+" -root "+element
            print(ABCsel)
            command = "-frameRange " + str(ABCstartTime) + " " + str(ABCendTime) + ABCuv + ABCws + ABCef + ABCsel + ABCwv + " -autoSubd -writeUVSets -file " + savePlace + saveName
            print(command)
            cmds.AbcExport(j= command)
            cmds.select(cl=True)
        else :
            cmds.inViewMessage(amg="Pas d'ABC correspondant, check le noms des setGeos, ou demande à Liam",f=True)
        # __importCache : import selection
    def importCache(savePath,saveName):
        selection = cmds.ls(sl=True)
        print(selection)
        selection = " ".join(selection)
        print(selection)
        print(savePath+saveName)
        cmds.AbcImport(savePath+saveName,m="import",ct=selection,sts=True)
        cmds.select(cl=True)
        shrekosPrint()
        # __switchImportExport : switches to the 'mode' associated
    def switchImportExport(saveName,savedCache,savePath,ABCef,selection,mode=""):
        if mode == "export":
            backupCheck(saveName,Path=savedCache,path=savePath)
            launchCache(saveName,ABCef,savePlace=savePath)
        if  mode == "import":
            importCache(savePlaceFinal,saveName)
        # __backupCheck : creates a backup of your precedent abc if it exists
    def backupCheck(saveName,Path,path,*args):
        childs=os.listdir(path+"/")
        print(Path)
        if not "backup" in childs:
            os.mkdir(path+"/backup")
        for child in childs:
            if saveName in child:
                if "_P" in child:
                    index= len(os.listdir(path+"/"+"backup/"))+1
                    baseSimp = child.split(".")[0]
                    if index<10:
                        shutil.move(Path, path+"backup/"+baseSimp+"_00"+str(index)+".abc")
                    else:
                        shutil.move(Path, path+"backup/"+baseSimp+"_0"+str(index)+".abc")
    runAutocache(mode=mode)