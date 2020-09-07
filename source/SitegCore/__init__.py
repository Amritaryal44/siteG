from SitegCore.app import create_app
import os, shutil

def copier(dst):
    try:
        packageDir = os.path.dirname(os.path.abspath(__file__))
        currentDir = os.getcwd()
        shutil.copytree(os.path.join(packageDir, 'site_files'), os.path.join(currentDir,dst))
        return 1
    except OSError:
        return 0

def readSite():
    packageDir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(packageDir, "tree.set"), "r") as f:
        setFormed = set(f.read()[1:-1].replace("'","").split(", "))
    setFormed = set(map(lambda x: os.path.normpath(x), setFormed))
    return setFormed
