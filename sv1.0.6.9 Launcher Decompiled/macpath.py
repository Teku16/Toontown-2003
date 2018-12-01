# File: m (Python 2.2)

import os
from stat import *
__all__ = [
    'normcase',
    'isabs',
    'join',
    'splitdrive',
    'split',
    'splitext',
    'basename',
    'dirname',
    'commonprefix',
    'getsize',
    'getmtime',
    'getatime',
    'islink',
    'exists',
    'isdir',
    'isfile',
    'walk',
    'expanduser',
    'expandvars',
    'normpath',
    'abspath']

def normcase(path):
    return path.lower()


def isabs(s):
    if ':' in s:
        pass
    return s[0] != ':'


def join(s, *p):
    path = s
    for t in p:
        if not s or isabs(t):
            path = t
            continue
        
        if t[:1] == ':':
            t = t[1:]
        
        if ':' not in path:
            path = ':' + path
        
        if path[-1:] != ':':
            path = path + ':'
        
        path = path + t
    
    return path


def split(s):
    if ':' not in s:
        return ('', s)
    
    colon = 0
    for i in range(len(s)):
        if s[i] == ':':
            colon = i + 1
        
    
    (path, file) = (s[:colon - 1], s[colon:])
    if path and not (':' in path):
        path = path + ':'
    
    return (path, file)


def splitext(p):
    (root, ext) = ('', '')
    for c in p:
        if c == ':':
            (root, ext) = (root + ext + c, '')
        elif c == '.':
            if ext:
                (root, ext) = (root + ext, c)
            else:
                ext = c
        elif ext:
            ext = ext + c
        else:
            root = root + c
    
    return (root, ext)


def splitdrive(p):
    return ('', p)


def dirname(s):
    return split(s)[0]


def basename(s):
    return split(s)[1]


def isdir(s):
    
    try:
        st = os.stat(s)
    except os.error:
        return 0

    return S_ISDIR(st[ST_MODE])


def getsize(filename):
    st = os.stat(filename)
    return st[ST_SIZE]


def getmtime(filename):
    st = os.stat(filename)
    return st[ST_MTIME]


def getatime(filename):
    st = os.stat(filename)
    return st[ST_ATIME]


def islink(s):
    return 0


def isfile(s):
    
    try:
        st = os.stat(s)
    except os.error:
        return 0

    return S_ISREG(st[ST_MODE])


def exists(s):
    
    try:
        st = os.stat(s)
    except os.error:
        return 0

    return 1


def commonprefix(m):
    if not m:
        return ''
    
    prefix = m[0]
    for item in m:
        for i in range(len(prefix)):
            if prefix[:i + 1] != item[:i + 1]:
                prefix = prefix[:i]
                if i == 0:
                    return ''
                
                break
            
        
    
    return prefix


def expandvars(path):
    return path


def expanduser(path):
    return path

norm_error = 'macpath.norm_error: path cannot be normalized'

def normpath(s):
    if ':' not in s:
        return ':' + s
    
    comps = s.split(':')
    i = 1
    while i < len(comps) - 1:
        if comps[i] == '' and comps[i - 1] != '':
            if i > 1:
                del comps[i - 1:i + 1]
                i = i - 1
            else:
                raise norm_error, 'Cannot use :: immediately after volume name'
        else:
            i = i + 1
    s = ':'.join(comps)
    if s[-1] == ':' and len(comps) > 2 and s != ':' * len(s):
        s = s[:-1]
    
    return s


def walk(top, func, arg):
    
    try:
        names = os.listdir(top)
    except os.error:
        return None

    func(arg, top, names)
    for name in names:
        name = join(top, name)
        if isdir(name):
            walk(name, func, arg)
        
    


def abspath(path):
    if not isabs(path):
        path = join(os.getcwd(), path)
    
    return normpath(path)

realpath = abspath
