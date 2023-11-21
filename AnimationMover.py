import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

# select target joint first, and then keyframed joint
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
    # getting the translate data 
    joint_translate = []
    joint_rotate = []
    # getting translate information out of tuple
    keyframed_bone_translate = cmds.getAttr(f"{joint_list[1]}.translate")
    for transform in keyframed_bone_translate[0]:
        joint_translate.append(transform)

    # getting rotate information out of tuple
    keyframed_bone_rotate = cmds.getAttr(f"{joint_list[1]}.rotate")
    for rotate in keyframed_bone_rotate[0]:
        joint_rotate.append(rotate)

    # moving the joint from target joint to keyframed joint
    cmds.move(joint_translate[0], joint_translate[1], joint_translate[2], joint_list[0])
    cmds.rotate(joint_rotate[0], joint_rotate[1], joint_rotate[2], joint_list[0])

    return
# _____________________________________________________________________
    
def setKeys(keys, joints):
    for key in keys:
        cmds.currentTime(key)
        moveToKeyframe(joints)
        cmds.setKeyframe(joints[0])
        

if __name__ == "__main__":
    keyframe_times = get_keyframe_times()
    setKeys(keyframe_times, selected_bones)

