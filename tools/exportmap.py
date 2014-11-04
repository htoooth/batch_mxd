
import os
import arcpy

input_path  = arcpy.GetParameterAsText(0)
resolution  = arcpy.GetParameterAsText(1)
isexportTree   = arcpy.GetParameterAsText(2)
output_path = arcpy.GetParameterAsText(3)

def export_mxd(inputfile,output,res):
    mxd = arcpy.mapping.MapDocument(inputfile)
    arcpy.mapping.ExportToJPEG(mxd,output,resolution=res)

def ignore_file(path,names):
    return [name for name in names if os.path.isfile(os.path.join(path,name)) and os.path.splitext(name)[1].lower() != ".mxd"]

def export_into_one(src,dst,handle = None,ignore = None):
    names = []
    for (path,dirs,files) in os.walk(src):
        names.extend([ (path,i) for i in files if os.path.splitext(i)[1].lower() == ".mxd"])

    for (path,name) in names:
        i = os.path.join(path,name)
        o = os.path.join(dst,os.path.splitext(name)[0] + ".jpg")
        handle(i,o)

def export_mxd_tree(src,dst,handle = None,ignore = None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src,names)
    else:
        ignored_names = set()

    if handle is None:
        return

    dst = dst.encode('gb2312')
    if os.path.exists(dst):
        pass
    else:
        os.makedirs(dst)

    dst = dst.decode('gb2312')
    
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src,name)
        dstname = os.path.join(dst,name)
        if os.path.isdir(srcname):
            export_mxd_tree(srcname,dstname,handle,ignore)
        else:
            handle(srcname,dstname)

def handle_mxd(res):
    return lambda i,o:export_mxd(i,o,res)

if str(isexportTree) == 'true':
    export_mxd_tree(input_path,output_path,handle_mxd(resolution),ignore_file)
else:
    export_into_one(input_path,output_path,handle_mxd(resolution))
