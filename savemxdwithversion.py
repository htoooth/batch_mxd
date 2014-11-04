import os
import arcpy


input_path  = arcpy.GetParameterAsText(0)
output_path = arcpy.GetParameterAsText(1)

def ignore_file(path,names):
    return [name for name in names if os.path.isfile(os.path.join(path,name)) and os.path.splitext(name)[1].lower() != ".mxd"]

def save_mxd(inputfile,output,ver="9.3"):
    mxd = arcpy.mapping.MapDocument(inputfile)
    mxd.saveACopy(output,ver)

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


export_mxd_tree(input_path,output_path,save_mxd,ignore_file)