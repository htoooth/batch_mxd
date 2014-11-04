
import os
import arcpy

input_path  = arcpy.GetParameterAsText(0)
output_path = arcpy.GetParameterAsText(1)
resolution  = arcpy.GetParameterAsText(2)
ischecked   = arcpy.GetParameterAsText(3)

if str(ischecked) == 'true':
    pass
else:
    pass

f = []
for (path,dirs,files) in os.walk(input_path):
    f.extend([ (path,i) for i in files if os.path.splitext(i)[1].lower() == ".mxd"])

def export_mxd(inputfile,output,res):
    mxd = arcpy.mapping.MapDocument(inputfile)
    arcpy.mapping.ExportToJPEG(mxd,output,resolution=res)

for (path,fi) in f:
    i = os.path.join(path,fi)
    o = os.path.join(output_path,fi)
    export_mxd(i,o,resolution)

def export_into_one(src,dst,handle = None,ignore = None):
    pass

def export_mxd_tree(src,dst,handle = None,ignore = None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src,name)
    else:
        ignored_names = set()

    if handle is None:
        return

    os.makedirs(dst)
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src,name)
        dstname = os.path.join(dst,name)
        if os.path.isdir(srcname):
            export_mxd_tree(srcname,dstname,handle,ignore)
        else:
            handle(srcname,dstname)


