import maya.cmds as cmds
import os

# this script was created to send out a text file that meets the standard import format for PFTrack. 
# start by selecting a series of locators with locators that are in position of what you're trying to track
# then run the script, this will create a text file in the location of the maya file with all the transform data

# getting the scene name in order to isolate both the scene name and the file path

filepath = cmds.file(q=True, sn=True)
raw_name, extension = os.path.splitext(filename)
filename = os.path.basename(filepath)
filepath = filepath.replace(filename, "")

# getting all the transforms from selected locators

selected_markers = cmds.ls(sl=True)
print(selected_markers)
locator_dimensions_list = []

# writing the information to the text file

default_heading = "# Name		SurveyX			SurveyY			SurveyZ			Uncertainty"
uncertainty_value_default = "3.000000"


lines = ['Readme', 'How to write text files in Python']
file_name_path = f"{filepath}{raw_name}_trackingMarkers.txt"

file_create = open(file_name_path, "w")

file_create.write(f"{default_heading} \n")

for locator in selected_markers:
    locator_transformX = cmds.getAttr(f"{locator}.translateX")
    locator_transformY = cmds.getAttr(f"{locator}.translateY")
    locator_transformZ = cmds.getAttr(f"{locator}.translateZ")
    file_create.write(f"\"{locator}\" \t")
    file_create.write(f"{locator_transformX} \t")
    file_create.write(f"{locator_transformY} \t")
    file_create.write(f"{locator_transformZ} \t")
    file_create.write(uncertainty_value_default)
    
    file_create.write("\n")
    
file_create.close()