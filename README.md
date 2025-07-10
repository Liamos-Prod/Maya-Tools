This is a pack of tools working for maya 2022 made in 2023 for my final year project it contains : 

  
- The LD Launcher
    
        --> A UI maya-based for renderman, done with the maya functions that has a few functions :
          -  setting the ratio format of your renders and choosing a camera for the render
          -  a time range changer for the sequence you need to render
          -  the lookdev tool allows you to select an object, add the selection to an LPE, and check cycles in the shading tab
          -  render tab is made for multiple things : cancelling all catmull and clark subdivs for exports, or applying them, disconnect displaces, and all the basic funtions of renderman in the render tab combined inside one UI, easing the process
          -  a locator to light baker, since some renders where made in maya and some in houdini, we had to export multiple locators that were parented to objects ( such as planes ).

- The VDB finder
  
        --> Is able to find the vdb's done in houdini and import them with the right settings in maya
    
- The autocacher
    
        --> This one was very usefull, since we had multiple abc to export / import during the production, I decided to build a auto-cache exporter.
          It was made with simple checkboxes, that would automatically select the right sets of selection and add them into a queue, that way, on a free computer and since we were using a storage, we could render all the alembics, and make sure they were
          correctly exported. 
          It would export :
            -  The camera
            -  The characters selected : --> one version for the final assembly ( with all the subdivs ) // one flat version of the clothes which allowed the CFX artist working on houdini to have the collider and the clothes // and one high version extruded of the clothes : used to apply the deformations of the flat clothes onto it.
            -  The planes
            The auto-cacher would also manage versionning by always getting the last version of the abc's and creating backups with the old versions just in case /!\/!\/!\/!\ CAN BE VERY HEAVY /!\/!\/!\/!\

- DPK installer
  
          --> While working with a license, and to make sure not only riggers and animators had DPK, I made sure everyone had it by creating a copy of dpk on each computer that had the pipeline, and checking if DPK was installed on every opening of this pipeline.
