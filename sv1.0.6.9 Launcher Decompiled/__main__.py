#[TTSQUEEZE] Phase2
import ihooks,zlib,marshal
f=open("Phase2.pyz","rb")
exec marshal.loads(zlib.decompress(f.read(904)))
boot("Phase2",f,408211)
exec "import Launcher"
