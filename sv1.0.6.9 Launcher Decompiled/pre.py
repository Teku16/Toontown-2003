# File: p (Python 2.2)

import sys
from pcre import *
__all__ = [
    'match',
    'search',
    'sub',
    'subn',
    'split',
    'findall',
    'escape',
    'compile',
    'I',
    'L',
    'M',
    'S',
    'X',
    'IGNORECASE',
    'LOCALE',
    'MULTILINE',
    'DOTALL',
    'VERBOSE',
    'error']
I = IGNORECASE
L = LOCALE
M = MULTILINE
S = DOTALL
X = VERBOSE
_cache = { }
_MAXCACHE = 20

def _cachecompile(pattern, flags = 0):
    key = (pattern, flags)
    
    try:
        return _cache[key]
    except KeyError:
        pass

    value = compile(pattern, flags)
    if len(_cache) >= _MAXCACHE:
        _cache.clear()
    
    _cache[key] = value
    return value


def match(pattern, string, flags = 0):
    return _cachecompile(pattern, flags).match(string)


def search(pattern, string, flags = 0):
    return _cachecompile(pattern, flags).search(string)


def sub(pattern, repl, string, count = 0):
    if type(pattern) == type(''):
        pattern = _cachecompile(pattern)
    
    return pattern.sub(repl, string, count)


def subn(pattern, repl, string, count = 0):
    if type(pattern) == type(''):
        pattern = _cachecompile(pattern)
    
    return pattern.subn(repl, string, count)


def split(pattern, string, maxsplit = 0):
    if type(pattern) == type(''):
        pattern = _cachecompile(pattern)
    
    return pattern.split(string, maxsplit)


def findall(pattern, string):
    if type(pattern) == type(''):
        pattern = _cachecompile(pattern)
    
    return pattern.findall(string)


def escape(pattern):
    result = list(pattern)
    for i in range(len(pattern)):
        char = pattern[i]
        if not char.isalnum():
            if char == '\x0':
                result[i] = '\\000'
            else:
                result[i] = '\\' + char
        
    
    return ''.join(result)


def compile(pattern, flags = 0):
    groupindex = { }
    code = pcre_compile(pattern, flags, groupindex)
    return RegexObject(pattern, flags, code, groupindex)


class RegexObject:
    
    def __init__(self, pattern, flags, code, groupindex):
        self.code = code
        self.flags = flags
        self.pattern = pattern
        self.groupindex = groupindex

    
    def search(self, string, pos = 0, endpos = None):
        if endpos is None or endpos > len(string):
            endpos = len(string)
        
        if endpos < pos:
            endpos = pos
        
        regs = self.code.match(string, pos, endpos, 0)
        if regs is None:
            return None
        
        self._num_regs = len(regs)
        return MatchObject(self, string, pos, endpos, regs)

    
    def match(self, string, pos = 0, endpos = None):
        if endpos is None or endpos > len(string):
            endpos = len(string)
        
        if endpos < pos:
            endpos = pos
        
        regs = self.code.match(string, pos, endpos, ANCHORED)
        if regs is None:
            return None
        
        self._num_regs = len(regs)
        return MatchObject(self, string, pos, endpos, regs)

    
    def sub(self, repl, string, count = 0):
        return self.subn(repl, string, count)[0]

    
    def subn(self, repl, source, count = 0):
        if count < 0:
            raise error, 'negative substitution count'
        
        if count == 0:
            count = sys.maxint
        
        n = 0
        pos = 0
        lastmatch = -1
        results = []
        end = len(source)
        if type(repl) is type(''):
            
            try:
                repl = pcre_expand(_Dummy, repl)
            except (error, TypeError):
                m = MatchObject(self, source, 0, end, [])
                
                repl = lambda m, repl = repl, expand = pcre_expand: expand(m, repl)

            m = None
        else:
            m = MatchObject(self, source, 0, end, [])
        match = self.code.match
        append = results.append
        while n < count and pos <= end:
            regs = match(source, pos, end, 0)
            if not regs:
                break
            
            self._num_regs = len(regs)
            (i, j) = regs[0]
            if i == j:
                pass
            j == lastmatch
            if 1:
                pos = pos + 1
                append(source[lastmatch:pos])
                continue
            
            if pos < i:
                append(source[pos:i])
            
            if m:
                m.pos = pos
                m.regs = regs
                append(repl(m))
            else:
                append(repl)
            pos = j
            lastmatch = j
            if i == j:
                pos = pos + 1
                append(source[lastmatch:pos])
            
            n = n + 1
        append(source[pos:])
        return (''.join(results), n)

    
    def split(self, source, maxsplit = 0):
        if maxsplit < 0:
            raise error, 'negative split count'
        
        if maxsplit == 0:
            maxsplit = sys.maxint
        
        n = 0
        pos = 0
        lastmatch = 0
        results = []
        end = len(source)
        match = self.code.match
        append = results.append
        while n < maxsplit:
            regs = match(source, pos, end, 0)
            if not regs:
                break
            
            (i, j) = regs[0]
            if i == j:
                if pos >= end:
                    break
                
                pos = pos + 1
                continue
            
            append(source[lastmatch:i])
            rest = regs[1:]
            if rest:
                for (a, b) in rest:
                    if a == -1 or b == -1:
                        group = None
                    else:
                        group = source[a:b]
                    append(group)
                
            
            pos = j
            lastmatch = j
            n = n + 1
        append(source[lastmatch:])
        return results

    
    def findall(self, source):
        pos = 0
        end = len(source)
        results = []
        match = self.code.match
        append = results.append
        while pos <= end:
            regs = match(source, pos, end, 0)
            if not regs:
                break
            
            (i, j) = regs[0]
            rest = regs[1:]
            if not rest:
                gr = source[i:j]
            elif len(rest) == 1:
                (a, b) = rest[0]
                gr = source[a:b]
            else:
                gr = []
                for (a, b) in rest:
                    gr.append(source[a:b])
                
                gr = tuple(gr)
            append(gr)
            pos = max(j, pos + 1)
        return results

    
    def __getinitargs__(self):
        return (None, None, None, None)

    
    def __getstate__(self):
        return (self.pattern, self.flags, self.groupindex)

    
    def __setstate__(self, statetuple):
        self.pattern = statetuple[0]
        self.flags = statetuple[1]
        self.groupindex = statetuple[2]
        self.code = apply(pcre_compile, statetuple)



class _Dummy:
    group = None


class MatchObject:
    
    def __init__(self, re, string, pos, endpos, regs):
        self.re = re
        self.string = string
        self.pos = pos
        self.endpos = endpos
        self.regs = regs

    
    def start(self, g = 0):
        if type(g) == type(''):
            
            try:
                g = self.re.groupindex[g]
            except (KeyError, TypeError):
                raise IndexError, 'group %s is undefined' % `g`

        
        return self.regs[g][0]

    
    def end(self, g = 0):
        if type(g) == type(''):
            
            try:
                g = self.re.groupindex[g]
            except (KeyError, TypeError):
                raise IndexError, 'group %s is undefined' % `g`

        
        return self.regs[g][1]

    
    def span(self, g = 0):
        if type(g) == type(''):
            
            try:
                g = self.re.groupindex[g]
            except (KeyError, TypeError):
                raise IndexError, 'group %s is undefined' % `g`

        
        return self.regs[g]

    
    def groups(self, default = None):
        result = []
        for g in range(1, self.re._num_regs):
            (a, b) = self.regs[g]
            if a == -1 or b == -1:
                result.append(default)
            else:
                result.append(self.string[a:b])
        
        return tuple(result)

    
    def group(self, *groups):
        if len(groups) == 0:
            groups = (0,)
        
        result = []
        for g in groups:
            if type(g) == type(''):
                
                try:
                    g = self.re.groupindex[g]
                except (KeyError, TypeError):
                    raise IndexError, 'group %s is undefined' % `g`

            
            if g >= len(self.regs):
                raise IndexError, 'group %s is undefined' % `g`
            
            (a, b) = self.regs[g]
            if a == -1 or b == -1:
                result.append(None)
            else:
                result.append(self.string[a:b])
        
        if len(result) > 1:
            return tuple(result)
        elif len(result) == 1:
            return result[0]
        else:
            return ()

    
    def groupdict(self, default = None):
        dict = { }
        for (name, index) in self.re.groupindex.items():
            (a, b) = self.regs[index]
            if a == -1 or b == -1:
                dict[name] = default
            else:
                dict[name] = self.string[a:b]
        
        return dict


