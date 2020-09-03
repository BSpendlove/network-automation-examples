import os

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