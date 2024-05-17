import maya.cmds as cmds

class createMaterialWindow(object):
    
    #constructor
    def __init__(self):
        
        self.materialWindow = "Material Creation"
        self.title = "Basic Redshift Material Creation"
        self.size = (300, 50)
       
        #closing the old window
        if cmds.window(self.materialWindow, exists=True):
            cmds.deleteUI(self.materialWindow, window=True)
            
        #create new window
        self.myWindow = cmds.window(self.materialWindow, title=self.title, widthHeight=self.size)
                
        #define layout
        cmds.columnLayout(adjustableColumn=True)
        
        #adding UI
        cmds.text(self.title)
        cmds.separator(height=20)
        
        self.materialName = cmds.textFieldGrp(label="Material Name:")
        self.createCamBtn = cmds.button("Create Material", command=self.materialCreation)
        
        #display new window
        cmds.showWindow()
        
        
    def materialCreation(self, *args):
        
        self.selectedObjects = cmds.ls(sl=True)
        self.materialCustomName = cmds.textFieldGrp(self.materialName, query=True, text=True) # remember this, querying the text field input data

        # define the creation of the standard material
        def createStandardMaterial(self, name, *args):
            self.materialList = []
            self.materialCreation = cmds.shadingNode('RedshiftStandardMaterial', asShader=True, n=self.materialCustomName)
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
        
        
        if len(selectedObjects) > 0:
            for object in selectedObjects:
                cmds.select(object)
                cmds.hyperShade(assign=materialNode[0])
                    
GC_materialWindow = createMaterialWindow()
