import maya.cmds as cmds

materialName = input("Assign a material name:")
selectedObjects = cmds.ls(sl=True)


# define the creation of the standard material
def createStandardMaterial(name):
    materialList = []
    materialCreation = cmds.shadingNode('RedshiftStandardMaterial', asShader=True, n=name)
    shadingGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{materialCreation}SG')
    cmds.connectAttr(f"{materialCreation}.outColor", f"{shadingGroup}.surfaceShader")
    materialList.append(materialCreation)
    materialList.append(shadingGroup)
    
    return materialList

# define function to create the file node and place2dTexture node, connect the attributes together, and then output the file node as a string
def createTextureFile(fileName, raw=False):

    def createFileNode():
        fileNode = cmds.shadingNode('file', asTexture=True, name=fileName)
        cmds.setAttr(f"{fileNode}.filterType", False)
        return fileNode

    def create_place2dNode():
        place2dNode = cmds.shadingNode('place2dTexture', asUtility=True)
        return place2dNode

    create2dNode = create_place2dNode()
    createFile = createFileNode()

    def attachFileNodeToPlace2d(place2dNode, fileNode):
        cmds.connectAttr(f'{place2dNode}.coverage', f'{fileNode}.coverage')
        cmds.connectAttr(f'{place2dNode}.translateFrame', f'{fileNode}.translateFrame')
        cmds.connectAttr(f'{place2dNode}.rotateFrame', f'{fileNode}.rotateFrame')
        cmds.connectAttr(f'{place2dNode}.mirrorU', f'{fileNode}.mirrorU')
        cmds.connectAttr(f'{place2dNode}.mirrorV', f'{fileNode}.mirrorV')
        cmds.connectAttr(f'{place2dNode}.stagger', f'{fileNode}.stagger')
        cmds.connectAttr(f'{place2dNode}.wrapU', f'{fileNode}.wrapU')
        cmds.connectAttr(f'{place2dNode}.wrapV', f'{fileNode}.wrapV')
        cmds.connectAttr(f'{place2dNode}.repeatUV', f'{fileNode}.repeatUV')
        cmds.connectAttr(f'{place2dNode}.offset', f'{fileNode}.offset')
        cmds.connectAttr(f'{place2dNode}.rotateUV', f'{fileNode}.rotateUV')
        cmds.connectAttr(f'{place2dNode}.noiseUV', f'{fileNode}.noiseUV')
        cmds.connectAttr(f'{place2dNode}.vertexUvOne', f'{fileNode}.vertexUvOne')
        cmds.connectAttr(f'{place2dNode}.vertexUvTwo', f'{fileNode}.vertexUvTwo')
        cmds.connectAttr(f'{place2dNode}.vertexUvThree', f'{fileNode}.vertexUvThree')
        cmds.connectAttr(f'{place2dNode}.vertexCameraOne', f'{fileNode}.vertexCameraOne')
        cmds.connectAttr(f'{place2dNode}.outUV', f'{fileNode}.uv')
        cmds.connectAttr(f'{place2dNode}.outUvFilterSize', f'{fileNode}.uvFilterSize')
    
    if raw:
        cmds.setAttr(f"{createFile}.ignoreColorSpaceFileRules", 1)
        cmds.setAttr(f"{createFile}.colorSpace", "Raw", type="string")
        cmds.setAttr(f"{createFile}.alphaIsLuminance", 1)
    
    attachFileNodeToPlace2d(create2dNode, createFile)
    
    return createFile
    
def normalNode():
    bumpNode = cmds.shadingNode("RedshiftBumpMap", asTexture=True)
    cmds.setAttr(f"{bumpNode}.inputType", 1)
    cmds.setAttr(f"{bumpNode}.scale", 1)
    
    return bumpNode
    
# creating the material node
materialNode = createStandardMaterial(materialName)

# creation of the file texture nodes
baseColourFile = createTextureFile(f"{materialName}_baseColour#")
roughnessFile = createTextureFile(f"{materialName}_roughness#", raw=True)
normalFile = createTextureFile(f"{materialName}_normal#", raw=True)
displacementFile = createTextureFile(f"{materialName}_displacement#", raw=True)
# creating bump and displacement nodes
bumpNode = normalNode()
displacementNode = cmds.shadingNode("RedshiftDisplacement", asShader=True)
# connecting the bump and displacements to the file nodes
cmds.connectAttr(f"{displacementFile}.outColor", f"{displacementNode}.texMap")
cmds.connectAttr(f"{normalFile}.outColor", f"{bumpNode}.input")
# connecting the file nodes to the correct inputs
print(materialNode[0])
cmds.connectAttr(f"{baseColourFile}.outColor", f"{materialNode[0]}.base_color")
cmds.connectAttr(f"{roughnessFile}.outAlpha", f"{materialNode[0]}.refl_roughness")
cmds.connectAttr(f"{bumpNode}.out", f"{materialNode[0]}.bump_input")
cmds.connectAttr(f"{displacementNode}.out", f"{materialNode[1]}.displacementShader")

for object in selectedObjects:
    cmds.select(object)
    cmds.hyperShade(assign=materialNode[0])
