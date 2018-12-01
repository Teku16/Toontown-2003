# File: P (Python 2.2)

import ihooks
import zlib
import marshal
f = open('Phase3.pyz', 'rb')
exec marshal.loads(zlib.decompress(f.read(904)))
boot('Phase3', f, 1647964)
exec 'import ToontownStart'
