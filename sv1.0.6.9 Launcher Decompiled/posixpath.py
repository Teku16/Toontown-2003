# File: p (Python 2.2)

global _varprog
import os
import stat
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
    'ismount',
    'walk',
    'expanduser',
    'expandvars',
    'normpath',
    'abspath',
    'samefile',
    'sameopenfile',
    'samestat']

def normcase(s):
    return s


def isabs(s):
    return s[:1] == '/'


def join(a, *p):
    path = a
    for b in p:
        if b[:1] == '/':
            path = b
        elif path == '' or path[-1:] == '/':
            path = path + b
        else:
            path = path + '/' + b
    
    return path


def split(p):
    i = p.rfind('/') + 1
    (head, tail) = (p[:i], p[i:])
    if head and head != '/' * len(head):
        while head[-1] == '/':
            head = head[:-1]
    
    return (head, tail)


def splitext(p):
    (root, ext) = ('', '')
    for c in p:
        if c == '/':
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


def basename(p):
    return split(p)[1]


def dirname(p):
    return split(p)[0]


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


def getsize(filename):
    st = os.stat(filename)
    return st[stat.ST_SIZE]


def getmtime(filename):
    st = os.stat(filename)
    return st[stat.ST_MTIME]


def getatime(filename):
    st = os.stat(filename)
    return st[stat.ST_ATIME]


def islink(path):
    
    try:
        st = os.lstat(path)
    except (os.error, AttributeError):
        return 0

    return stat.S_ISLNK(st[stat.ST_MODE])


def exists(path):
    
    try:
        st = os.stat(path)
    except os.error:
        return 0

    return 1


def isdir(path):
    
    try:
        st = os.stat(path)
    except os.error:
        return 0

    return stat.S_ISDIR(st[stat.ST_MODE])


def isfile(path):
    
    try:
        st = os.stat(path)
    except os.error:
        return 0

    return stat.S_ISREG(st[stat.ST_MODE])


def samefile(f1, f2):
    s1 = os.stat(f1)
    s2 = os.stat(f2)
    return samestat(s1, s2)


def sameopenfile(fp1, fp2):
    s1 = os.fstat(fp1)
    s2 = os.fstat(fp2)
    return samestat(s1, s2)


def samestat(s1, s2):
    if s1[stat.ST_INO] == s2[stat.ST_INO]:
        pass
    return s1[stat.ST_DEV] == s2[stat.ST_DEV]


def ismount(path):
    
    try:
        s1 = os.stat(path)
        s2 = os.stat(join(path, '..'))
    except os.error:
        return 0

    dev1 = s1[stat.ST_DEV]
    dev2 = s2[stat.ST_DEV]
    if dev1 != dev2:
        return 1
    
    ino1 = s1[stat.ST_INO]
    ino2 = s2[stat.ST_INO]
    if ino1 == ino2:
        return 1
    
    return 0


def walk(top, func, arg):
    
    try:
        names = os.listdir(top)
    except os.error:
        return None

    func(arg, top, names)
    for name in names:
        name = join(top, name)
        
        try:
            st = os.lstat(name)
        except os.error:
            continue

        if stat.S_ISDIR(st[stat.ST_MODE]):
            walk(name, func, arg)
        
    


def expanduser(path):
    if path[:1] != '~':
        return path
    
    (i, n) = (1, len(path))
    while i < n and path[i] != '/':
        i = i + 1
    if i == 1:
        if not os.environ.has_key('HOME'):
            import pwd
            userhome = pwd.getpwuid(os.getuid())[5]
        else:
            userhome = os.environ['HOME']
    else:
        import pwd
        
        try:
            pwent = pwd.getpwnam(path[1:i])
        except KeyError:
            return path

        userhome = pwent[5]
    if userhome[-1:] == '/':
        i = i + 1
    
    return userhome + path[i:]

_varprog = None

def expandvars(path):
    global _varprog
    if '$' not in path:
        return path
    
    if not _varprog:
        import re
        _varprog = re.compile('\\$(\\w+|\\{[^}]*\\})')
    
    i = 0
    while 1:
        m = _varprog.search(path, i)
        if not m:
            break
        
        (i, j) = m.span(0)
        name = m.group(1)
        if name[:1] == '{' and name[-1:] == '}':
            name = name[1:-1]
        
        if os.environ.has_key(name):
            tail = path[j:]
            path = path[:i] + os.environ[name]
            i = len(path)
            path = path + tail
        else:
            i = j
    return path


def normpath(path):
    if path == '':
        return '.'
    
    initial_slashes = path.startswith('/')
    if initial_slashes and path.startswith('//') and not path.startswith('///'):
        initial_slashes = 2
    
    comps = path.split('/')
    new_comps = []
    for comp in comps:
        if comp in ('', '.'):
            continue
        
        if not comp != '..':
            if not initial_slashes and not new_comps and new_comps and new_comps[-1] == '..':
                new_comps.append(comp)
            elif new_comps:
                new_comps.pop()
            
    
    comps = new_comps
    path = '/'.join(comps)
    if initial_slashes:
        path = '/' * initial_slashes + path
    
    if not path:
        pass
    return '.'


def abspath(path):
    if not isabs(path):
        path = join(os.getcwd(), path)
    
    return normpath(path)


def realpath(filename):
    filename = abspath(filename)
    bits = [
        '/'] + filename.split('/')[1:]
    for i in range(2, len(bits) + 1):
        component = join(*bits[0:i])
        if islink(component):
            resolved = os.readlink(component)
            (dir, file) = split(component)
            resolved = normpath(join(dir, resolved))
            newpath = join(*[
                resolved] + bits[i:])
            return realpath(newpath)
        
    
    return filename

