from __future__ import generators
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__credits__ = 'GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, Skip Montanaro'
import string, re
from token import *
import token
__all__ = [ x for x in dir(token) if x[0] != '_' ] + ['COMMENT', 'tokenize', 'NL']
del token
COMMENT = N_TOKENS
tok_name[COMMENT] = 'COMMENT'
NL = N_TOKENS + 1
tok_name[NL] = 'NL'
N_TOKENS += 2

def group(*choices):
    return '(' + ('|').join(choices) + ')'


def any(*choices):
    return apply(group, choices) + '*'


def maybe(*choices):
    return apply(group, choices) + '?'


Whitespace = '[ \\f\\t]*'
Comment = '#[^\\r\\n]*'
Ignore = Whitespace + any('\\\\\\r?\\n' + Whitespace) + maybe(Comment)
Name = '[a-zA-Z_]\\w*'
Hexnumber = '0[xX][\\da-fA-F]*[lL]?'
Octnumber = '0[0-7]*[lL]?'
Decnumber = '[1-9]\\d*[lL]?'
Intnumber = group(Hexnumber, Octnumber, Decnumber)
Exponent = '[eE][-+]?\\d+'
Pointfloat = group('\\d+\\.\\d*', '\\.\\d+') + maybe(Exponent)
Expfloat = '\\d+' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group('\\d+[jJ]', Floatnumber + '[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)
Single = "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
Double = '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
Single3 = "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
Double3 = '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
Triple = group("[uU]?[rR]?'''", '[uU]?[rR]?"""')
String = group("[uU]?[rR]?'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*'", '[uU]?[rR]?"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*"')
Operator = group('\\*\\*=?', '>>=?', '<<=?', '<>', '!=', '//=?', '[+\\-*/%&|^=<>]=?', '~')
Bracket = '[][(){}]'
Special = group('\\r?\\n', '[:;.,`]')
Funny = group(Operator, Bracket, Special)
PlainToken = group(Number, Funny, String, Name)
Token = Ignore + PlainToken
ContStr = group("[uU]?[rR]?'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*" + group("'", '\\\\\\r?\\n'), '[uU]?[rR]?"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*' + group('"', '\\\\\\r?\\n'))
PseudoExtras = group('\\\\\\r?\\n', Comment, Triple)
PseudoToken = Whitespace + group(PseudoExtras, Number, Funny, ContStr, Name)
tokenprog, pseudoprog, single3prog, double3prog = map(re.compile, (Token, PseudoToken, Single3, Double3))
endprogs = {"'": re.compile(Single), '"': re.compile(Double), "'''": single3prog, '"""': double3prog, "r'''": single3prog, 'r"""': double3prog, "u'''": single3prog, 'u"""': double3prog, "ur'''": single3prog, 'ur"""': double3prog, "R'''": single3prog, 'R"""': double3prog, "U'''": single3prog, 'U"""': double3prog, "uR'''": single3prog, 'uR"""': double3prog, "Ur'''": single3prog, 'Ur"""': double3prog, "UR'''": single3prog, 'UR"""': double3prog, 'r': None, 'R': None, 'u': None, 'U': None}
tabsize = 8

class TokenError(Exception):
    __module__ = __name__


class StopTokenizing(Exception):
    __module__ = __name__


def printtoken(type, token, (srow, scol), (erow, ecol), line):
    print '%d,%d-%d,%d:\t%s\t%s' % (srow, scol, erow, ecol, tok_name[type], repr(token))


def tokenize(readline, tokeneater=printtoken):
    try:
        tokenize_loop(readline, tokeneater)
    except StopTokenizing:
        pass


def tokenize_loop(readline, tokeneater):
    for token_info in generate_tokens(readline):
        apply(tokeneater, token_info)


def generate_tokens(readline):
    lnum = parenlev = continued = 0
    namechars, numchars = (string.ascii_letters + '_', '0123456789')
    contstr, needcont = ('', 0)
    contline = None
    indents = [0]
    while 1:
        line = readline()
        lnum = lnum + 1
        pos, max = (0, len(line))
        if contstr:
            if not line:
                raise TokenError, ('EOF in multi-line string', strstart)
            endmatch = endprog.match(line)
            if endmatch:
                pos = end = endmatch.end(0)
                yield (STRING, contstr + line[:end], strstart, (lnum, end), contline + line)
                contstr, needcont = (
                 '', 0)
                contline = None
            else:
                if needcont and line[-2:] != '\\\n' and line[-3:] != '\\\r\n':
                    yield (
                     ERRORTOKEN, contstr + line, strstart, (lnum, len(line)), contline)
                    contstr = ''
                    contline = None
                    continue
                else:
                    contstr = contstr + line
                    contline = contline + line
                    continue
        else:
            if parenlev == 0 and not continued:
                if not line:
                    break
                column = 0
                while pos < max:
                    if line[pos] == ' ':
                        column = column + 1
                    else:
                        if line[pos] == '\t':
                            column = (column / tabsize + 1) * tabsize
                        else:
                            if line[pos] == '\x0c':
                                column = 0
                            else:
                                break
                    pos = pos + 1

                if pos == max:
                    break
                if line[pos] in '#\r\n':
                    yield (
                     (
                      NL, COMMENT)[line[pos] == '#'], line[pos:], (lnum, pos), (lnum, len(line)), line)
                    continue
                if column > indents[-1]:
                    indents.append(column)
                    yield (INDENT, line[:pos], (lnum, 0), (lnum, pos), line)
                while column < indents[-1]:
                    indents = indents[:-1]
                    yield (DEDENT, '', (lnum, pos), (lnum, pos), line)

            else:
                if not line:
                    raise TokenError, ('EOF in multi-line statement', (lnum, 0))
                continued = 0
        while pos < max:
            pseudomatch = pseudoprog.match(line, pos)
            if pseudomatch:
                start, end = pseudomatch.span(1)
                spos, epos, pos = ((lnum, start), (lnum, end), end)
                token, initial = (line[start:end], line[start])
                if initial in numchars or initial == '.' and token != '.':
                    yield (NUMBER, token, spos, epos, line)
                else:
                    if initial in '\r\n':
                        yield (
                         parenlev > 0 and NL or NEWLINE, token, spos, epos, line)
                    else:
                        if initial == '#':
                            yield (
                             COMMENT, token, spos, epos, line)
                        else:
                            if token in ("'''", '"""', "r'''", 'r"""', "R'''", 'R"""', "u'''", 'u"""', "U'''", 'U"""', "ur'''", 'ur"""', "Ur'''", 'Ur"""', "uR'''", 'uR"""', "UR'''", 'UR"""'):
                                endprog = endprogs[token]
                                endmatch = endprog.match(line, pos)
                                if endmatch:
                                    pos = endmatch.end(0)
                                    token = line[start:pos]
                                    yield (STRING, token, spos, (lnum, pos), line)
                                else:
                                    strstart = (
                                     lnum, start)
                                    contstr = line[start:]
                                    contline = line
                                    break
                            else:
                                if initial in ("'", '"') or token[:2] in ("r'", 'r"', "R'", 'R"', "u'", 'u"', "U'", 'U"') or token[:3] in ("ur'", 'ur"', "Ur'", 'Ur"', "uR'", 'uR"', "UR'", 'UR"'):
                                    if token[-1] == '\n':
                                        strstart = (
                                         lnum, start)
                                        endprog = endprogs[initial] or endprogs[token[1]] or endprogs[token[2]]
                                        contstr, needcont = (
                                         line[start:], 1)
                                        contline = line
                                        break
                                    else:
                                        yield (
                                         STRING, token, spos, epos, line)
                                else:
                                    if initial in namechars:
                                        yield (
                                         NAME, token, spos, epos, line)
                                    else:
                                        if initial == '\\':
                                            continued = 1
                                        else:
                                            if initial in '([{':
                                                parenlev = parenlev + 1
                                            else:
                                                if initial in ')]}':
                                                    parenlev = parenlev - 1
                                            yield (
                                             OP, token, spos, epos, line)
            else:
                yield (
                 ERRORTOKEN, line[pos], (lnum, pos), (lnum, pos + 1), line)
                pos = pos + 1

    for indent in indents[1:]:
        yield (
         DEDENT, '', (lnum, 0), (lnum, 0), '')

    yield (
     ENDMARKER, '', (lnum, 0), (lnum, 0), '')
    return


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        tokenize(open(sys.argv[1]).readline)
    else:
        tokenize(sys.stdin.readline)