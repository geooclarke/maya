# things to add
#    check box for if you want to assign the material to the selected object
#    tick box for each file node to create, with all defaulting to on, apart from the displacement
#    prefix for material naming convention
#    better organised button layout
#    ability to select specific maps and a UDIM tickbox
#    ability to select multiple maps at once and a whole folder auto fill into correct boxes
#    folder selection with auto detect map types
#    error messages, such as if there isn't a material name, or missing map type

import maya.cmds as cmds

class createMaterialWindow(object):
    
    # constructor
    def __init__(self):

        self.materialWindow = "MaterialCreation"
        self.title = "Basic Redshift Material Creation"
        self.size = [300, 200]
        
        # closing the old window
        if cmds.window(self.materialWindow, exists=True):
            cmds.deleteUI(self.materialWindow, window=True)
            
        # create new window
        self.myWindow = cmds.window(self.materialWindow, title=self.title, widthHeight=self.size, resizeToFitChildren=True)
                
        #define layout
        cmds.columnLayout(adjustableColumn=True)
        
        # adding UI
        cmds.text(self.title)
        cmds.separator(height=20)
        
        self.materialName = cmds.textFieldGrp(label="Material Name:")
        self.buttonRow = cmds.rowLayout(numberOfColumns=3, columnWidth=((1, 100), (2, 100), (3, 800)))
        self.createMatBtnAndClose = cmds.button("Create and Close", parent=self.buttonRow, command=self.materialAndClose)
        self.createCamBtn = cmds.button("Create Material", command=self.materialCreation, parent=self.buttonRow)
        self.createCloseBtn = cmds.button("Close", parent=self.buttonRow, command=self.closeWindow)
        
        # display new window
        cmds.showWindow()
        
    def closeWindow(self, *args):
        cmds.deleteUI(self.materialWindow, window=True)
        return
        
    def materialCreation(self, *args):
        
        self.selectedObjects = cmds.ls(sl=True)
        self.materialCustomName = cmds.textFieldGrp(self.materialName, query=True, text=True) # remember this, querying the text field input data

        # define the creation of the standard material
        def createStandardMaterial(self, name, *args):
            self.materialList = []
            self.materialCreation = cmds.shadingNode('RedshiftStandardMaterial', asShader=True, name=self.materialCustomName)
            self.shadingGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{self.materialCreation}SG')
            cmds.connectAttr(f"{self.materialCreation}.outColor", f"{self.shadingGroup}.surfaceShader")
            self.materialList.append(self.materialCreation)
            self.materialList.append(self.shadingGroup)
            
            return self.materialList

        # define function to create the file node and place2dTexture node, connect the attributes together, and then output the file node as a string
        def createTextureFile(self, fileName, raw=False):
        
            def createFileNode(self):
                self.fileNode = cmds.shadingNode('file', asTexture=True, name=fileName)
                cmds.setAttr(f"{self.fileNode}.filterType", False)
                return self.fileNode
        
            def create_place2dNode(self):
                self.place2dNode = cmds.shadingNode('place2dTexture', asUtility=True)
                return self.place2dNode
    
            self.create2dNode = create_place2dNode(self)
            self.createFile = createFileNode(self)
    
            def attachFileNodeToPlace2d(self, place2dNode, fileNode):
                cmds.connectAttr(f'{self.place2dNode}.coverage', f'{self.fileNode}.coverage')
                cmds.connectAttr(f'{self.place2dNode}.translateFrame', f'{self.fileNode}.translateFrame')
                cmds.connectAttr(f'{self.place2dNode}.rotateFrame', f'{self.fileNode}.rotateFrame')
                cmds.connectAttr(f'{self.place2dNode}.mirrorU', f'{self.fileNode}.mirrorU')
                cmds.connectAttr(f'{self.place2dNode}.mirrorV', f'{self.fileNode}.mirrorV')
                cmds.connectAttr(f'{self.place2dNode}.stagger', f'{self.fileNode}.stagger')
                cmds.connectAttr(f'{self.place2dNode}.wrapU', f'{self.fileNode}.wrapU')
                cmds.connectAttr(f'{self.place2dNode}.wrapV', f'{self.fileNode}.wrapV')
                cmds.connectAttr(f'{self.place2dNode}.repeatUV', f'{self.fileNode}.repeatUV')
                cmds.connectAttr(f'{self.place2dNode}.offset', f'{self.fileNode}.offset')
                cmds.connectAttr(f'{self.place2dNode}.rotateUV', f'{self.fileNode}.rotateUV')
                cmds.connectAttr(f'{self.place2dNode}.noiseUV', f'{self.fileNode}.noiseUV')
                cmds.connectAttr(f'{self.place2dNode}.vertexUvOne', f'{self.fileNode}.vertexUvOne')
                cmds.connectAttr(f'{self.place2dNode}.vertexUvTwo', f'{self.fileNode}.vertexUvTwo')
                cmds.connectAttr(f'{self.place2dNode}.vertexUvThree', f'{self.fileNode}.vertexUvThree')
                cmds.connectAttr(f'{self.place2dNode}.vertexCameraOne', f'{self.fileNode}.vertexCameraOne')
                cmds.connectAttr(f'{self.place2dNode}.outUV', f'{self.fileNode}.uv')
                cmds.connectAttr(f'{self.place2dNode}.outUvFilterSize', f'{self.fileNode}.uvFilterSize')
            
            if raw:
                cmds.setAttr(f"{self.createFile}.ignoreColorSpaceFileRules", 1)
                cmds.setAttr(f"{self.createFile}.colorSpace", "Raw", type="string")
                cmds.setAttr(f"{self.createFile}.alphaIsLuminance", 1)
            
            attachFileNodeToPlace2d(self, self.create2dNode, self.createFile)
            
            return self.createFile
            
        def normalNode(self):
            self.bumpNode = cmds.shadingNode("RedshiftBumpMap", asTexture=True)
            cmds.setAttr(f"{self.bumpNode}.inputType", 1)
            cmds.setAttr(f"{self.bumpNode}.scale", 1)
            
            return self.bumpNode
    
        # creating the material node
        self.materialNode = createStandardMaterial(self, name=self.materialCustomName)
        # creation of the file texture nodes
        self.baseColourFile = createTextureFile(self, f"{self.materialCustomName}_baseColour#")
        self.roughnessFile = createTextureFile(self, f"{self.materialCustomName}_roughness#", raw=True)
        self.normalFile = createTextureFile(self, f"{self.materialCustomName}_normal#", raw=True)
        self.displacementFile = createTextureFile(self, f"{self.materialCustomName}_displacement#", raw=True)
        
        # creating bump and displacement nodes
        self.bumpNode = normalNode(self)
        self.displacementNode = cmds.shadingNode("RedshiftDisplacement", asShader=True)
        
        # connecting the bump and displacements to the file nodes
        cmds.connectAttr(f"{self.displacementFile}.outColor", f"{self.displacementNode}.texMap")
        cmds.connectAttr(f"{self.normalFile}.outColor", f"{self.bumpNode}.input")
        
        # connecting the file nodes to the correct inputs
        cmds.connectAttr(f"{self.baseColourFile}.outColor", f"{self.materialNode[0]}.base_color")
        cmds.connectAttr(f"{self.roughnessFile}.outAlpha", f"{self.materialNode[0]}.refl_roughness")
        cmds.connectAttr(f"{self.bumpNode}.out", f"{self.materialNode[0]}.bump_input")
        cmds.connectAttr(f"{self.displacementNode}.out", f"{self.materialNode[1]}.displacementShader")
        
        if len(self.selectedObjects) > 0:
            for object in self.selectedObjects:
                cmds.select(object)
                cmds.hyperShade(assign=self.materialNode[0])
                
    def materialAndClose(self, *args):
        self.materialCreation()
        self.closeWindow()
        
GC_materialWindow = createMaterialWindow()
