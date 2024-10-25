import maya.cmds as cmds

selectedCurve = cmds.ls(sl=True)

duplicatedCurve = cmds.duplicate(selectedCurve)

cmds.setAttr(f"{duplicatedCurve[0]}.scaleX", -1)

cmds.reverseCurve(f"{duplicatedCurve[0]}", constructionHistory=0)

attachedCurve = cmds.attachCurve(f"{selectedCurve[0]}", f"{duplicatedCurve[0]}", constructionHistory=0, replaceOriginal=0, method=1)

cmds.rename(attachedCurve[0], f"{selectedCurve[0]}mirrored")