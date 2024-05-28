try:
    # Qt5
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from PySide2 import QtGui
    from shiboken2 import wrapInstance
except:
    # Qt6
    from PySide6 import QtCore
    from PySide6 import QtWidgets
    from PySide6 import QtGui
    from shiboken6 import wrapInstance
    
import sys
import maya.OpenMayaUI as omui
    
    
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    
class MainToolWindow(QtWidgets.QDialog):
    
    FILE_FILTERS = " All Files (*.*);; tif (*.tif *.tiff);; png (*.png);; \
    jpeg (*.jpeg *.jpg *.jp2);; exr (*.exr);; hdr (*.hdr);; tga (*.tga)"
    
    selected_filter = "Images ( )"
    
    def __init__(self, parent=maya_main_window()):
        super().__init__(parent)
        
        self.setWindowTitle("Redshift Material Creation")
        self.setMinimumSize(500, 400)
        
        # On macOS make the window a Tool to keep it on top of Maya
        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)
            
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
            
    def create_widgets(self):
        self.material_name_le = QtWidgets.QLineEdit()
        
        self.base_colour_fp = QtWidgets.QLineEdit()
        self.base_colour_btn = QtWidgets.QPushButton()
        self.base_colour_btn.setToolTip("Select File")
        self.base_colour_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
                
                
        self.metallic_fp = QtWidgets.QLineEdit()
        self.metallic_btn = QtWidgets.QPushButton()
        self.metallic_btn.setToolTip("Select File")
        self.metallic_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        
        self.roughness_fp = QtWidgets.QLineEdit()
        self.roughness_btn = QtWidgets.QPushButton()
        self.roughness_btn.setToolTip("Select File")
        self.roughness_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        
        self.normal_fp = QtWidgets.QLineEdit()
        self.normal_btn = QtWidgets.QPushButton()
        self.normal_btn.setToolTip("Select File")
        self.normal_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        
        self.displacement_fp = QtWidgets.QLineEdit()
        self.displacement_btn = QtWidgets.QPushButton()
        self.displacement_btn.setToolTip("Select File")
        self.displacement_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        
        self.create_and_close_btn = QtWidgets.QPushButton("Create And Close")
        self.create_material_btn = QtWidgets.QPushButton("Create Material")
        self.close_btn = QtWidgets.QPushButton("Close")
        
    def create_layouts(self):
        material_layout = QtWidgets.QFormLayout()
        material_layout.addRow(self.material_name_le)
        
        base_colour_layout = QtWidgets.QHBoxLayout()
        base_colour_layout.addWidget(self.base_colour_fp)
        base_colour_layout.addWidget(self.base_colour_btn)
        
        metallic_layout = QtWidgets.QHBoxLayout()
        metallic_layout.addWidget(self.metallic_fp)
        metallic_layout.addWidget(self.metallic_btn)
        
        roughness_layout = QtWidgets.QHBoxLayout()
        roughness_layout.addWidget(self.roughness_fp)
        roughness_layout.addWidget(self.roughness_btn)
        
        normal_layout = QtWidgets.QHBoxLayout()
        normal_layout.addWidget(self.normal_fp)
        normal_layout.addWidget(self.normal_btn)
        
        displacement_layout = QtWidgets.QHBoxLayout()
        displacement_layout.addWidget(self.displacement_fp)
        displacement_layout.addWidget(self.displacement_btn)
        
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        button_layout.addWidget(self.create_and_close_btn)
        button_layout.addWidget(self.create_material_btn)
        button_layout.addWidget(self.close_btn)
        
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Material Name: ", material_layout)
        form_layout.addRow("Base Colour:", base_colour_layout)
        form_layout.addRow("Metallic: ", metallic_layout)
        form_layout.addRow("Roughness: ", roughness_layout)
        form_layout.addRow("Normal: ", normal_layout)
        form_layout.addRow("Displacement: ", displacement_layout)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        
        
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        
    def create_connections(self):
        # file paths
        self.base_colour_btn.clicked.connect(self.show_file_select_dialog)
        self.metallic_btn.clicked.connect(self.show_file_select_metallic)
        self.roughness_btn.clicked.connect(self.show_file_select_roughness)
        self.normal_btn.clicked.connect(self.show_file_select_normal)
        self.displacement_btn.clicked.connect(self.show_file_select_displacement)
        
        # lower buttons
        self.create_and_close_btn.clicked.connect(self.creatingMateralAndClose)
        self.create_material_btn.clicked.connect(self.creatingMaterial)
        self.close_btn.clicked.connect(self.close)

# methods for the file opening boxes for each map type. I'm sure this can be done in 1 method...
        
        
    def show_file_select_dialog(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(
        self, "Select File", "", self.FILE_FILTERS, self.selected_filter)
        
        # below makes sure code is run just in case user closed dialog box
        if file_path:
            # adding the returned file path to the line edit
            self.base_colour_fp.setText(file_path)
            
    def show_file_select_metallic(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(
        self, "Select File", "", self.FILE_FILTERS, self.selected_filter)
        
        if file_path:
            self.metallic_fp.setText(file_path)
            
    def show_file_select_roughness(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(
        self, "Select File", "", self.FILE_FILTERS, self.selected_filter)
        
        if file_path:
            self.roughness_fp.setText(file_path)
            
    def show_file_select_normal(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(
        self, "Select File", "", self.FILE_FILTERS, self.selected_filter)
        
        if file_path:
            self.normal_fp.setText(file_path)
            
    def show_file_select_displacement(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(
        self, "Select File", "", self.FILE_FILTERS, self.selected_filter)
        
        if file_path:
            self.displacement_fp.setText(file_path)
            
    # retrieving the material name text
    def get_name(self):
        return(self.material_name_le.text())
        
    # retrieving the selected file names ready to be input into the file nodes 
    
    def base_colour_file_path(self):
        return(self.base_colour_fp.text())
        
    def metallic_file_path(self):
        return(self.metallic_fp.text())
        
    def roughness_file_path(self):
        return(self.roughness_fp.text())
        
    def normal_file_path(self):
        return(self.normal_fp.text())
        
    def displacement_file_path(self):
        return(self.displacement_fp.text())
         
    ####################################
    # MATERIAL HEIRARCHY CREATION
    def createMaterial(self):
        
        self.selectedObjects = cmds.ls(sl=True)
        self.materialCustomName = self.get_name()
        
        # creating variabvles for each file path
        self.base_colour_file = self.base_colour_file_path()
        self.metallic_file = self.metallic_file_path()
        self.roughness_file = self.roughness_file_path()
        self.normal_file = self.normal_file_path()
        self.displacement_file = self.displacement_file_path()
        
        # creating the standard material node
        def createStandardMaterial(self, name, *args):
            self.name = name
            self.materialList = []
            self.materialCreation = cmds.shadingNode('RedshiftStandardMaterial', asShader=True, name=self.name)
            self.shadingGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{self.name}SG')
            cmds.connectAttr(f"{self.materialCreation}.outColor", f"{self.shadingGroup}.surfaceShader")
            self.materialList.append(self.materialCreation)
            self.materialList.append(self.shadingGroup)
            
            return self.materialList
            
        def createTextureFile(self, mapType, raw=False):
            
            def createFileNode(self):
                self.mapType = mapType
                self.fileName = self.materialCustomName
                self.fileNode = cmds.shadingNode('file', asTexture=True, name=f"{self.materialCustomName}_{self.mapType}_#")
                cmds.setAttr(f"{self.fileNode}.filterType", False)
                return self.fileNode
        
            def create_place2dNode(self):
                self.place2dNode = cmds.shadingNode('place2dTexture', asUtility=True)
                return self.place2dNode
   
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
                
            self.create2dNode = create_place2dNode(self)
            self.createFile = createFileNode(self)
            
            attachFileNodeToPlace2d(self, self.create2dNode, self.createFile)
            
            return self.createFile
            
            
        def normalNode(self):
            self.bumpNode = cmds.shadingNode("RedshiftBumpMap", asTexture=True)
            cmds.setAttr(f"{self.bumpNode}.inputType", 1)
            cmds.setAttr(f"{self.bumpNode}.scale", 1)
            
            return self.bumpNode
            
            
        # creating main node structure. This will have to change when introducing toggle checkboxes
        self.materialNode = createStandardMaterial(self, name=self.materialCustomName)
        self.baseColourFile = createTextureFile(self, "base_colour")
        self.metallicFile = createTextureFile(self, "metallic")
        self.roughnessFile = createTextureFile(self, "roughness", raw=True)
        self.normalFile = createTextureFile(self, "normal", raw=True)
        self.displacementFile = createTextureFile(self, "displacement", raw=True)
        
        # setting the file path to each individual 
        cmds.setAttr(f"{self.baseColourFile}.fileTextureName", f"{self.base_colour_file}", type="string")
        cmds.setAttr(f"{self.metallicFile}.fileTextureName", f"{self.metallic_file}", type="string")
        cmds.setAttr(f"{self.roughnessFile}.fileTextureName", f"{self.roughness_file}", type="string")
        cmds.setAttr(f"{self.normalFile}.fileTextureName", f"{self.normal_file}", type="string")
        cmds.setAttr(f"{self.displacementFile}.fileTextureName", f"{self.displacement_file}", type="string")
        
        
        self.bumpNode = normalNode(self)
        self.displacementNode = cmds.shadingNode("RedshiftDisplacement", asShader=True)
        # connecting the bump and displacements to the file nodes
        cmds.connectAttr(f"{self.displacementFile}.outColor", f"{self.displacementNode}.texMap")
        cmds.connectAttr(f"{self.normalFile}.outColor", f"{self.bumpNode}.input")
        # connecting the file nodes to the correct inputs
        cmds.connectAttr(f"{self.baseColourFile}.outColor", f"{self.materialNode[0]}.base_color")
        cmds.connectAttr(f"{self.metallicFile}.outAlpha", f"{self.materialNode[0]}.metalness")
        cmds.connectAttr(f"{self.roughnessFile}.outAlpha", f"{self.materialNode[0]}.refl_roughness")
        cmds.connectAttr(f"{self.bumpNode}.out", f"{self.materialNode[0]}.bump_input")
        cmds.connectAttr(f"{self.displacementNode}.out", f"{self.materialNode[1]}.displacementShader")
        
        
    def creatingMaterial(self):
        self.redshiftMaterial = self.createMaterial()
        
    def creatingMateralAndClose(self):
        self.redshiftMaterial = self.createMaterial()
        self.close()
   
        
if __name__ == "__main__":
    try:
        win.close()        # pylint: disable=E0601
        win.deleteLater()
    except:
        pass
        
    win = MainToolWindow()
    win.show()
