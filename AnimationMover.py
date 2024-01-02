################################################################
# This code will currently copy any keyed translation and rotation data from one object to another.
# Select the animated object first and then the target object.
################################################################

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

# Update 0.5
       # set to work in local space so will work when objects and bones are in a heirarchy.
       # also now select the animated object first and then the target object
# Update 0.6
       # Added conditional to determine if 2 objects have been selected
       # Added multiple items to have keyframes assigned
# TODO: 
#       make a UI for this so the user can set whether to be done in world or local space
#       add in the checker of whether there has been a range set or not
#       probably will never be required but to do as practice, add the ability to set keys on every frame
#       is there a way of factoring in animation curves?

# select target keyframed object first, and then target object
selected_bones = cmds.ls(sl=True)
#getting the initial playback range
def get_playback_range():
    range_start = cmds.playbackOptions(q=True, minTime=True)
    range_end = cmds.playbackOptions(q=True, maxTime=True)
    return [range_start, range_end]
    
# determining if a keyframe exists
def keyframe_exists(keyframe_time):
    keyframe_count = cmds.keyframe(q=True, keyframeCount=True, time=(keyframe_time,))
    return keyframe_count > 0

# getting the keyframe times by making a range out of the playback min and max
# then filtering this out by running through the range and appending any frames where more than 1 key exists
def get_keyframe_times(skip_existing=True):
    keyframe_range = get_playback_range()
    range_start = keyframe_range[0]
    range_end = keyframe_range[1]
    
    keyframe_list = list(range(int(range_start), int((range_end + 1))))
    
    if skip_existing:
        filtered_list = []
        for keyframe_time in keyframe_list:
            if keyframe_exists(keyframe_time):
                filtered_list.append(keyframe_time)
    return filtered_list
# _____________________________________________________________________

def moveToKeyframe(joint_list):
    new_list = joint_list[1:]
    # getting the translate data 
    joint_translate = []
    joint_rotate = []
    # getting translate information out of tuple
    keyframed_bone_translate = cmds.getAttr(f"{joint_list[0]}.translate")
    for transform in keyframed_bone_translate[0]:
        joint_translate.append(transform)

    # getting rotate information out of tuple
    keyframed_bone_rotate = cmds.getAttr(f"{joint_list[0]}.rotate")
    for rotate in keyframed_bone_rotate[0]:
        joint_rotate.append(rotate)

    # moving the joint from target joint to keyframed joint for each item after the first
    for item in new_list:
        cmds.move(joint_translate[0], joint_translate[1], joint_translate[2], item, localSpace=True)
        cmds.rotate(joint_rotate[0], joint_rotate[1], joint_rotate[2], item, objectSpace=True)

    return
# _____________________________________________________________________
    
   
def setKeys(keys, joints):
    new_list = joints[1:]
    for item in new_list:
        for key in keys:
            cmds.currentTime(key)
            moveToKeyframe(joints)
            cmds.setKeyframe(item)


if __name__ == "__main__":
    if len(selected_bones) >= 2:
        keyframe_times = get_keyframe_times()
        setKeys(keyframe_times, selected_bones)
    else:
        om.MGlobal.displayError("Please select 2 or more objects, animated object first")
