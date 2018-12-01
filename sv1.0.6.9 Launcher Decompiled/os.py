# File: o (Python 2.2)

import sys
_names = sys.builtin_module_names
altsep = None
__all__ = [
    'altsep',
    'curdir',
    'pardir',
    'sep',
    'pathsep',
    'linesep',
    'defpath',
    'name']

def _get_exports_list(module):
    
    try:
        return list(module.__all__)
    except AttributeError:
        continue
        return []


if 'posix' in _names:
    name = 'posix'
    linesep = '\n'
    curdir = '.'
    pardir = '..'
    sep = '/'
    pathsep = ':'
    defpath = ':/bin:/usr/bin'
    from posix import *
    
    try:
        from posix import _exit
    except ImportError:
        pass

    import posixpath
    path = posixpath
    del posixpath
    import posix
    __all__.extend(_get_exports_list(posix))
    del posix
elif 'nt' in _names:
    name = 'nt'
    linesep = '\r\n'
    curdir = '.'
    pardir = '..'
    sep = '\\'
    pathsep = ';'
    defpath = '.;C:\\bin'
    from nt import *
    for i in [
        '_exit']:
        
        try:
            exec 'from nt import ' + i
        except ImportError:
            pass

    
    import ntpath
    path = ntpath
    del ntpath
    import nt
    __all__.extend(_get_exports_list(nt))
    del nt
elif 'dos' in _names:
    name = 'dos'
    linesep = '\r\n'
    curdir = '.'
    pardir = '..'
    sep = '\\'
    pathsep = ';'
    defpath = '.;C:\\bin'
    from dos import *
    
    try:
        from dos import _exit
    except ImportError:
        pass

    import dospath
    path = dospath
    del dospath
    import dos
    __all__.extend(_get_exports_list(dos))
    del dos
elif 'os2' in _names:
    name = 'os2'
    linesep = '\r\n'
    curdir = '.'
    pardir = '..'
    sep = '\\'
    pathsep = ';'
    defpath = '.;C:\\bin'
    from os2 import *
    
    try:
        from os2 import _exit
    except ImportError:
        pass

    import ntpath
    path = ntpath
    del ntpath
    import os2
    __all__.extend(_get_exports_list(os2))
    del os2
elif 'mac' in _names:
    name = 'mac'
    linesep = '\r'
    curdir = ':'
    pardir = '::'
    sep = ':'
    pathsep = '\n'
    defpath = ':'
    from mac import *
    
    try:
        from mac import _exit
    except ImportError:
        pass

    import macpath
    path = macpath
    del macpath
    import mac
    __all__.extend(_get_exports_list(mac))
    del mac
elif 'ce' in _names:
    name = 'ce'
    linesep = '\r\n'
    curdir = '.'
    pardir = '..'
    sep = '\\'
    pathsep = ';'
    defpath = '\\Windows'
    from ce import *
    for i in [
        '_exit']:
        
        try:
            exec 'from ce import ' + i
        except ImportError:
            pass

    
    import ntpath
    path = ntpath
    del ntpath
    import ce
    __all__.extend(_get_exports_list(ce))
    del ce
elif 'riscos' in _names:
    name = 'riscos'
    linesep = '\n'
    curdir = '@'
    pardir = '^'
    sep = '.'
    pathsep = ','
    defpath = '<Run$Dir>'
    from riscos import *
    
    try:
        from riscos import _exit
    except ImportError:
        pass

    import riscospath
    path = riscospath
    del riscospath
    import riscos
    __all__.extend(_get_exports_list(riscos))
    del riscos
else:
    raise ImportError, 'no os specific module found'
if sep == '.':
    extsep = '/'
else:
    extsep = '.'
__all__.append('path')
del _names
sys.modules['os.path'] = path

def makedirs(name, mode = 511):
    (head, tail) = path.split(name)
    if not tail:
        (head, tail) = path.split(head)
    
    if head and tail and not path.exists(head):
        makedirs(head, mode)
    
    mkdir(name, mode)


def removedirs(name):
    rmdir(name)
    (head, tail) = path.split(name)
    if not tail:
        (head, tail) = path.split(head)
    
    while head and tail:
        
        try:
            rmdir(head)
        except error:
            break

        (head, tail) = path.split(head)


def renames(old, new):
    (head, tail) = path.split(new)
    if head and tail and not path.exists(head):
        makedirs(head)
    
    rename(old, new)
    (head, tail) = path.split(old)
    if head and tail:
        
        try:
            removedirs(head)
        except error:
            pass

    

__all__.extend([
    'makedirs',
    'removedirs',
    'renames'])

try:
    pass
except NameError:
    environ = { }


def execl(file, *args):
    execv(file, args)


def execle(file, *args):
    env = args[-1]
    execve(file, args[:-1], env)


def execlp(file, *args):
    execvp(file, args)


def execlpe(file, *args):
    env = args[-1]
    execvpe(file, args[:-1], env)


def execvp(file, args):
    _execvpe(file, args)


def execvpe(file, args, env):
    _execvpe(file, args, env)

__all__.extend([
    'execl',
    'execle',
    'execlp',
    'execlpe',
    'execvp',
    'execvpe'])

def _execvpe(file, args, env = None):
    ENOENT = ENOENT
    ENOTDIR = ENOTDIR
    import errno
    if env is not None:
        func = execve
        argrest = (args, env)
    else:
        func = execv
        argrest = (args,)
        env = environ
    (head, tail) = path.split(file)
    if head:
        apply(func, (file,) + argrest)
        return None
    
    if env.has_key('PATH'):
        envpath = env['PATH']
    else:
        envpath = defpath
    PATH = envpath.split(pathsep)
    saved_exc = None
    saved_tb = None
    for dir in PATH:
        fullname = path.join(dir, file)
        
        try:
            apply(func, (fullname,) + argrest)
        except error:
            e = None
            tb = sys.exc_info()[2]
            if e.errno != ENOENT and e.errno != ENOTDIR and saved_exc is None:
                saved_exc = e
                saved_tb = tb
            
        except:
            saved_exc is None

    
    if saved_exc:
        raise error, saved_exc, saved_tb
    
    raise error, e, tb


try:
    pass
except NameError:
    pass

import UserDict
if name in ('os2', 'nt', 'dos'):
    
    def unsetenv(key):
        putenv(key, '')


if name == 'riscos':
    from riscosenviron import _Environ
elif name in ('os2', 'nt', 'dos'):
    
    class _Environ(UserDict.IterableUserDict):
        
        def __init__(self, environ):
            UserDict.UserDict.__init__(self)
            data = self.data
            for (k, v) in environ.items():
                data[k.upper()] = v
            

        
        def __setitem__(self, key, item):
            putenv(key, item)
            self.data[key.upper()] = item

        
        def __getitem__(self, key):
            return self.data[key.upper()]

        
        try:
            pass
        except NameError:
            
            def __delitem__(self, key):
                del self.data[key.upper()]


        
        def __delitem__(self, key):
            unsetenv(key)
            del self.data[key.upper()]

        
        def has_key(self, key):
            return self.data.has_key(key.upper())

        
        def get(self, key, failobj = None):
            return self.data.get(key.upper(), failobj)

        
        def update(self, dict):
            for (k, v) in dict.items():
                self[k] = v
            


else:
    
    class _Environ(UserDict.IterableUserDict):
        
        def __init__(self, environ):
            UserDict.UserDict.__init__(self)
            self.data = environ

        
        def __setitem__(self, key, item):
            putenv(key, item)
            self.data[key] = item

        
        def update(self, dict):
            for (k, v) in dict.items():
                self[k] = v
            

        
        try:
            pass
        except NameError:
            pass

        
        def __delitem__(self, key):
            unsetenv(key)
            del self.data[key]


environ = _Environ(environ)

def getenv(key, default = None):
    return environ.get(key, default)

__all__.append('getenv')

def _exists(name):
    
    try:
        eval(name)
        return 1
    except NameError:
        return 0


if _exists('fork') and not _exists('spawnv') and _exists('execv'):
    P_WAIT = 0
    P_NOWAIT = 1
    P_NOWAITO = 1
    
    def _spawnvef(mode, file, args, env, func):
        pid = fork()
        if not pid:
            
            try:
                if env is None:
                    func(file, args)
                else:
                    func(file, args, env)
            except:
                _exit(127)

        elif mode == P_NOWAIT:
            return pid
        
        while 1:
            (wpid, sts) = waitpid(pid, 0)
            if WIFSTOPPED(sts):
                continue
            elif WIFSIGNALED(sts):
                return -WTERMSIG(sts)
            elif WIFEXITED(sts):
                return WEXITSTATUS(sts)
            else:
                raise error, 'Not stopped, signaled or exited???'

    
    def spawnv(mode, file, args):
        return _spawnvef(mode, file, args, None, execv)

    
    def spawnve(mode, file, args, env):
        return _spawnvef(mode, file, args, env, execve)

    
    def spawnvp(mode, file, args):
        return _spawnvef(mode, file, args, None, execvp)

    
    def spawnvpe(mode, file, args, env):
        return _spawnvef(mode, file, args, env, execvpe)


if _exists('spawnv'):
    
    def spawnl(mode, file, *args):
        return spawnv(mode, file, args)

    
    def spawnle(mode, file, *args):
        env = args[-1]
        return spawnve(mode, file, args[:-1], env)


if _exists('spawnvp'):
    
    def spawnlp(mode, file, *args):
        return spawnvp(mode, file, args)

    
    def spawnlpe(mode, file, *args):
        env = args[-1]
        return spawnvpe(mode, file, args[:-1], env)

    __all__.extend([
        'spawnlp',
        'spawnlpe',
        'spawnv',
        'spawnve',
        'spawnvp',
        'spawnvpe',
        'spawnl',
        'spawnle'])

if _exists('fork'):
    if not _exists('popen2'):
        
        def popen2(cmd, mode = 't', bufsize = -1):
            import popen2
            (stdout, stdin) = popen2.popen2(cmd, bufsize)
            return (stdin, stdout)

        __all__.append('popen2')
    
    if not _exists('popen3'):
        
        def popen3(cmd, mode = 't', bufsize = -1):
            import popen2
            (stdout, stdin, stderr) = popen2.popen3(cmd, bufsize)
            return (stdin, stdout, stderr)

        __all__.append('popen3')
    
    if not _exists('popen4'):
        
        def popen4(cmd, mode = 't', bufsize = -1):
            import popen2
            (stdout, stdin) = popen2.popen4(cmd, bufsize)
            return (stdin, stdout)

        __all__.append('popen4')
    

import copy_reg as _copy_reg

def _make_stat_result(tup, dict):
    return stat_result(tup, dict)


def _pickle_stat_result(sr):
    (type, args) = sr.__reduce__()
    return (_make_stat_result, args)


try:
    _copy_reg.pickle(stat_result, _pickle_stat_result, _make_stat_result)
except NameError:
    pass


def _make_statvfs_result(tup, dict):
    return statvfs_result(tup, dict)


def _pickle_statvfs_result(sr):
    (type, args) = sr.__reduce__()
    return (_make_statvfs_result, args)


try:
    _copy_reg.pickle(statvfs_result, _pickle_statvfs_result, _make_statvfs_result)
except NameError:
    pass

