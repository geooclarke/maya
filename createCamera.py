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
    return

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
    return

# creation of camera and groups, as well as locking values
create_camera("rendercam")
create_grp("tilt")
lock_tilt_attrs((cmds.ls(sl=True)[0]))
create_grp("crane")
lock_crane_attrs((cmds.ls(sl=True)[0]))

# creating the distance dimensions
cmds.distanceDimension( sp=(0, 0, 0), ep=(0, 0, 2) )
cmds.move(0, 0, 0, "locator2")
cmds.parent("locator1", "crane")
cmds.parent("locator2", "rendercam1")
cmds.rename("distanceDimension1", "DoF")
cmds.expression(o = "rendercam1", s = "rendercamShape1.focusDistance = DoFShape.distance")
cmds.parent("DoF", "crane")
