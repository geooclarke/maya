import maya.cmds as cmds

#define camera creation function
def create_camera(name):
    create_rendercam = cmds.camera(name=name)
    camera_attrs = ['translate', 'rotate']
    camera_axis = ['X', 'Y']
    obj = cmds.ls(sl=True)[0]
    
    
    # nested for loop to run through each attribute and lock accordingly
    for axis in camera_axis:
        for attr in camera_attrs:
            cmds.setAttr(obj+'.'+attr+axis, lock=1)
    return name

# define the function that will lock the attributes on the tilt group
def lock_tilt_attrs(name):
        tilt_axis = ["X", "Y", "Z"]
        tilt_attrs = ["translate", "rotate", "scale"]
        obj = cmds.ls(sl=True)[0]
        
        # nested for loop, same as the for loop above, but running through a couple if statements to skip the rotate x attribute
        for axis in tilt_axis:
            if axis != "X":
                for attr in tilt_attrs:
                    cmds.setAttr(obj+"."+attr+axis, lock=1)
            else:
                for attr in tilt_attrs:
                    if attr != "rotate":
                        cmds.setAttr(obj+"."+attr+axis, lock=1)
        return

# define the function that will lock the the attributes on the crane group
def lock_crane_attrs(name):
        tilt_axis = ["X",]
        tilt_attrs = ["rotate"]
        obj = cmds.ls(sl=True)[0]
        
        for axis in tilt_axis:
            for attr in tilt_attrs:
                cmds.setAttr(obj+"."+attr+axis, lock=1)
        return

#define the group creation
def create_grp(name):
    cmds.group(name=name) # indexing is so that it only selects the transform node
    return name

# creation of camera and groups, as well as locking values
cam = create_camera("camera_1")
cam = cmds.ls(sl=True)[0]
tilt_grp = create_grp(f"{cam}_tilt")
lock_tilt_attrs((cmds.ls(sl=True)[0]))
crane_grp = create_grp(f"{cam}_crane")
lock_crane_attrs((cmds.ls(sl=True)[0]))

# new creation of the locators and distance object

def createLocator(name):
    name = name
    cmds.spaceLocator(n=name)
    return name

loc_1 = createLocator(f"{cam}_DoF_loc_1")
loc_2 = createLocator(f"{cam}_DoF_loc_2")

cmds.move(0, 1, 0, loc_1)
startPoint = cmds.getAttr(f"{loc_1}.translate")
endPoint = cmds.getAttr(f"{loc_2}.translate")

create_dist = cmds.distanceDimension(sp=startPoint[0], ep=endPoint[0])
cmds.move(0, 0, 0, loc_1)
distDimParent = cmds.listRelatives(create_dist, p=True)
cmds.select(clear=True)
distDimParent = cmds.rename(distDimParent, f"{cam}_DoF")
# parenting to the main group
cmds.parent(loc_2, cam)
cmds.parent(loc_1, crane_grp)
cmds.parent(distDimParent, crane_grp)

cmds.expression(o = cam, s = (cam+".focusDistance = "+distDimParent+".distance"))
