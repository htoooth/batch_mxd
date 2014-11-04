
import os
import arcpy

input_path = arcpy.GetParameterAsText(0)
output_path = arcpy.GetParameterAsText(1)
resolution = int(arcpy.GetParameterAsText(2))

f = []
for (path,dirs,files) in os.walk(input_path):
    f = [ (path,i) for i in files if os.path.splitext(i)[1].lower() == ".mxd"]


def export_mxd(input,output,res):
    mxd = arcpy.mapping.MapDocument(input)
    arcpy.mapping.ExportToJPEG(mxd,output,resolution=res)

for (path,fi) in f:
    i = os.path.join(path,fi)
    o = os.path.join(output_path,fi)
    export_mxd(i,o,resolution)
