#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, random, time, logging, StringIO, shutil
from PyInstaller.main import run as pyinstallerrun

def log(c):
    time.sleep(1)
    logger = logging.getLogger("PyInstaller")
    sio = StringIO.StringIO()
    logger.addHandler( logging.StreamHandler(sio) )
    
    old_len = 0
    while not (c.error or c.finished):
        entrys = sio.getvalue().split("\n")
        
        if len(entrys) != old_len:
            for entry in entrys[(old_len-1):-1]:
                c.LOG(entry)
            old_len = len(entrys)
        
        time.sleep(0.1)
                

def build(c):
    try:
        oldcwd = os.getcwd()
        project = c.project
        
        if not check_empty(project):
            c.ERROR("Please enter: 'name', 'executable file', 'output path' and 'temporary path'!")
            return
        if not check_str(project):
            c.ERROR("You are only allowed to use ASCII-characters!")
            return
        
        tmp, dist, spec, work = get_paths(project)
        create_paths(project.temppath, tmp, dist, spec, work)
        
        args = create_args(project, dist, spec, work)
        
        c.LOG("created arguments: {}".format(args))
        
        
        os.chdir(dist)
        c.LOG(u"Changing working-dir: " + unicode(os.getcwd()))
    
        #############################################################################################################
        pyinstallerrun(pyi_args=args)
        time.sleep(5) #!!
        
        c.LOG("building successful! :)")
        
        if project.saveasfile: #copy file
            ld = os.listdir(dist)
            c.LOG(u"copy files to '{0}'".format(os.path.join(project.outpath, ld[0])))
            shutil.copy(os.path.join(dist, ld[0]), os.path.join(project.outpath, ld[0]))
        else: #copy dir
            c.LOG(u"copy dir to '{0}'".format(os.path.join(project.outpath, project.name)))
            shutil.copytree(os.path.join(dist, project.name), os.path.join(project.outpath, project.name))
        
        shutil.rmtree(tmp)
        
        c.FINISH()
    except Exception as FM:
        c.ERROR(FM)
    finally:
        os.chdir(oldcwd)
        c.LOG(u"Changing working-dir: " + unicode(os.getcwd()))
        c.LOG("Exit building-progress...")
    

def get_paths(project):
    tmp = os.path.join(project.temppath, "ps{0}".format(hex(random.randint(0x111111111111, 0xffffffffffff))[2:]))
    dist = os.path.join(tmp, "dist")
    spec = os.path.join(tmp, "spec")
    work = os.path.join(tmp, "work")
    return tmp, dist, spec, work
def create_paths(*args):
    for p in args:
        if not os.path.exists(p):
            os.mkdir(p)

def create_args(project, dist, spec, work):
        args = []
        
        args.append("-n")
        args.append(project.name)
    
        if len(project.icon) > 0: args.append(u'--icon={0}'.format(project.icon))
    
        args.append(u'--distpath={0}'.format(dist))
        
        args.append("--clean")
        
        if project.saveasfile:              args.append("-F")
        else:                               args.append("-D")
    
        if project.console:                 args.append("-c")
        else:                               args.append("-w")
        
        if project.debug:                   args.append("-d")
        
        for p in project.pathstosearchin:   args.append('--paths="{}"'.format(p))
        for hi in project.hiddenmodules:    args.append('--hidden-import="{}"'.format(hi))
        
        if not project.unicode:         args.append("-a")
        
        args.append("-y")
        
        args.append('--specpath={}'.format(spec))
        args.append('--workpath={}'.format(work))
        
        args.append('{}'.format(project.execfile))
        
        return args

def check_str(project):
    try:
        str(project.name) + str(project.icon) + str(project.execfile) + str(project.outpath) + str(project.temppath)
        return True
    except:
        return False
def check_empty(project):
    for key in ["name", "execfile", "outpath", "temppath"]:
        if len(eval("project.{}".format(key))) == 0: return False
    return True
