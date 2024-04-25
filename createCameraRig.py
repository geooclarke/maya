import maya.cmds as cmds

class createWindow(object):
    
    # constructor
    def __init__(self):
        
        self.cameraWindow = "Camera Window"
        self.title = "Camera Creator"
        self.size = (300, 200)
       
        #closing the old window
        if cmds.window(myWindow, exists=True):
            cmds.deleteUI(myWindow, window=True)
            
        #create new window
        self.myWindow = cmds.window(self.cameraWindow, title=self.title, widthHeight=self.size)
                

        #define layout
        cmds.columnLayout(adjustableColumn=True)
        
        #adding UI
        cmds.text(self.title)
        cmds.separator(height=20)
        
        self.camName = cmds.textFieldGrp(label="Camera Name:")
        self.createCamBtn = cmds.button("Create Camera", command=self.createCamera)
        
        #display new window
        cmds.showWindow()
        

        
    # main camera method
    def createCamera(self, *args):
        self.camName = cmds.textFieldGrp(self.camName, query=True, text=True)
        
        def create_camera():
            self.name = self.camName
            self.create_rendercam = cmds.camera(n=self.camName)
            self.camera_list = self.create_rendercam
            self.camera_attrs = ['translate', 'rotate']
            self.camera_axis = ['X', 'Y']
            self.obj = cmds.ls(sl=True)
            
            
            # nested for loop to run through each attribute and lock accordingly
            for axis in self.camera_axis:
                for attr in self.camera_attrs:
                    cmds.setAttr(f"{self.obj[0]}.{attr}{axis}", lock=1)
            return self.camera_list
        
        # define the function that will lock the attributes on the tilt group
        def lock_tilt_attrs(name):
            tilt_axis = ["X", "Y", "Z"]
            tilt_attrs = ["translate", "rotate", "scale"]
            obj = cmds.ls(sl=True)[0]
            
            # nested for loop, same as the for loop above, but running through a couple if statements to skip the rotate x attribute
            for axis in tilt_axis:
                if axis != "X":
                    for attr in tilt_attrs:
                        cmds.setAttr(f"{obj}.{attr}{axis}", lock=1)
                else:
                    for attr in tilt_attrs:
                        if attr != "rotate":
                            cmds.setAttr(f"{obj}.{attr}{axis}", lock=1)
            return
            
        # define the function that will lock the the attributes on the crane group
        def lock_crane_attrs(name):
                tilt_axis = ["X",]
                tilt_attrs = ["rotate"]
                obj = cmds.ls(sl=True)[0]
                
                for axis in tilt_axis:
                    for attr in tilt_attrs:
                        cmds.setAttr(f"{obj}.{attr}{axis}", lock=1)
                return
        
        # define the group creation
        def create_grp(name):
            cmds.group(name=name) # indexing is so that it only selects the transform node
            return name
        
        # define locator
        def createLocator(name):
            name = name
            cmds.spaceLocator(n=name)
            return name
        
        self.cam = create_camera()
        self.camMain = self.cam[0]
        self.tilt_grp = create_grp(f"{self.camMain}_tilt")
        lock_tilt_attrs((cmds.ls(sl=True)[0]))
        self.crane_grp = create_grp(f"{self.camMain}_crane")
        lock_crane_attrs((cmds.ls(sl=True)[0]))
        
        # creation of the locators and distance object
        self.loc_1 = createLocator(f"{self.camMain}_DoF_loc_1")
        self.loc_2 = createLocator(f"{self.camMain}_DoF_loc_2")
        
        cmds.move(0, 1, 0, self.loc_1)
        self.startPoint = cmds.getAttr(f"{self.loc_1}.translate")
        self.endPoint = cmds.getAttr(f"{self.loc_2}.translate")
        self.create_dist = cmds.distanceDimension(sp=self.startPoint[0], ep=self.endPoint[0])
        cmds.move(0, 0, 0, self.loc_1)
        self.distDimParent = cmds.listRelatives(self.create_dist, p=True)
        cmds.select(clear=True)
        self.distDimParent = cmds.rename(self.distDimParent, f"{self.camMain}_DoF")
        
        # parenting to the main group
        cmds.parent(self.loc_2, self.camMain)
        cmds.parent(self.loc_1, self.crane_grp)
        cmds.parent(self.distDimParent, self.crane_grp)
        cmds.select(clear=True)
        
        
        cmds.expression(o=self.camMain, s=(f"{self.camMain}.focusDistance = {self.distDimParent}.distance"))
        
        cmds.deleteUI(myWindow, window=True)
        
        return
        
GC_cameraWindow = createWindow()
