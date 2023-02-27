from types import SimpleNamespace 
import time

file1 = {'filepath': 'path/to/logs/file1.log', 'contents': '', 'ctime': time.time() - 1800, 'size': 0}
file2 = {'filepath': 'path/to/logs/file2.log', 'contents': 'hi', 'ctime': time.time() - 900, 'size': 1}
file3 = {'filepath': 'path/to/logs/file3.log', 'contents': '', 'ctime': time.time() - 3600, 'size': 0}

mock_dir = {'path': 'path/to/logs/', "contents": {}}


class MockOS():
    def __init__(self):
        self.path = SimpleNamespace(getsize = self.path_getsize, 
                                    getctime = self.path_getctime,
                                    join = self.path_join,
                                    dirname = self.path_dirname)
        self.filesystem = {}
    

    def path_getsize(self, dir):
        parent_dir = self.path_dirname(dir)
        filename = dir.split('/')[-1].split('.')[0]
        size = self.filesystem[parent_dir]['contents'][filename]['size']
        return size

    def path_getctime(self, dir):
        parent_dir = self.path_dirname(dir)
        filename = dir.split('/')[-1].split('.')[0]
        ctime = self.filesystem[parent_dir]['contents'][filename]['ctime']
        return ctime
    
    def path_join(self, *args):
        return ''.join([arg for arg in args])

    def path_dirname(self, dir):
        return '/'.join(dir.split('/')[:-1]) + '/'

    def listdir(self, dir):
        try:
            parentfolder = self.path_dirname(dir)
            dirlist = [file['filepath'].split('/')[-1] for file in self.filesystem[parentfolder]['contents'].values()]
        except KeyError:
            raise FileNotFoundError(f'"{dir}" does not exist') from OSError
        return dirlist

    def remove(self, dir):
        try:
           parent_dir = self.path_dirname(dir)
           filename = dir.split('/')[-1].split('.')[0]
           del self.filesystem[parent_dir]['contents'][filename]
        except KeyError:
            raise FileNotFoundError(f'"{dir}" does not exist') from OSError
        return 1

    def makedir(self, dir):
        if dir['path'][-1] != '/':
            raise FileNotFoundError(f'"{dir}" is not a directory') from OSError
        try:
           self.filesystem[dir['path']] = dir
        except KeyError:
            raise FileNotFoundError(f'"{dir}" does is exist') from OSError
        return 1
        # self.filesystem[dir['path']] = dir

mock_os = MockOS()
mock_os.makedir(mock_dir)
mock_os.filesystem[mock_dir['path']]['contents']['file1'] = file1
mock_os.filesystem[mock_dir['path']]['contents']['file2'] = file2
mock_os.filesystem[mock_dir['path']]['contents']['file3'] = file3
# print(mock_os.filesystem)

def test():
    joined = mock_os.path.join('test/', 'me/myself/', 'silly.log')
    dirlist = mock_os.listdir(mock_dir['contents']['file1']['filepath'])
    parentfolder = mock_os.path.dirname(file1['filepath'])

    print(f'test: \njoined = {joined}\ndirlist = {dirlist}\nparentfolder = {parentfolder}\n')

def test1():
    parentfolder = mock_os.path.dirname(file1['filepath'])
    logs = [mock_os.path.join(parentfolder, f) for f in mock_os.listdir(parentfolder) if f.endswith('.log')]
    print(f'test 1: \nparent folder = {parentfolder}\nlogs = {logs}\n')

def test2():
    parentfolder = mock_os.path.dirname(file1['filepath'])
    ctimes = [(mock_os.path.join(parentfolder, f), mock_os.path.getctime(mock_os.path.join(parentfolder, f))) for f in mock_os.listdir(parentfolder) if f.endswith('.log')]
    print(f'test 2: \nparent folder = {parentfolder}\nctimes = {ctimes}\n')

def test3():
    print(f'test 3: \n{mock_os.filesystem}')
    mock_os.remove(file2['filepath'])
    print(f'after remove: \n{mock_os.filesystem}\n')

def test4():
    parentfolder = mock_os.path.dirname(file1['filepath'])
    filesize = mock_os.path.getsize(file2['filepath']) # dpesn't exist should thrown not found error
    print(f'test 4: \nparent folder = {parentfolder}\nfilesize = {filesize}\n')
    # filesize = os.path.getsize(self.filepath)

# test()
test1()
test2()
test3()
test4()