# This file is for live testing during development...
"""
from app import db
from functions import dbfunctions

device = dbfunctions.get_device("CSW01")
print(device.vlans)
"""

import os
import json

rootDir = "backups"

folder_structure = {}
"""
for dirName, subdirList, fileList in os.walk(rootDir):
    print(dirName)
    for fname in fileList:
        folder_structure[dirName] = fname
        print('\t%s' % fname)

print(json.dumps(folder_structure, indent=4))
"""
def dir_to_list(dirname, path=os.path.pathsep):
    data = []
    for name in os.listdir(dirname):
        dct = {}
        dct['name'] = name
        dct['path'] = path + name

        full_path = os.path.join(dirname, name)
        if os.path.isfile(full_path):
            dct['type'] = 'file'
        elif os.path.isdir(full_path):
            dct['type'] = 'folder'
            dct['children'] = dir_to_list(full_path, path=path + name + os.path.pathsep)
        data.append(dct)
    return data

print(json.dumps(dir_to_list(rootDir), indent=4))