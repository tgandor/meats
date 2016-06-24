#qpy:console
import os,os.path,sys
#sys.dont_write_bytecode = True

def modcmd(arg):
    arg = 'pip ' + arg
    print(arg)
    os.system(sys.executable+" "+sys.prefix+"/bin/"+arg)

if not(os.path.exists(sys.prefix+"/bin/pip")):
    print("You need to install pip first.")
    exit()

print("Input pip commands, ie: pip install {module}")

shorthands = {
    'i': 'install',
    'f': 'freeze',
    's': 'search'
}

def expand(cmd):
    splat = cmd.split()
    cmd = splat[0]
    args = splat[1:]
    if cmd in shorthands:
        cmd = shorthands[cmd]
    return ' '.join([cmd] + args)

while(True):
    cmd = raw_input("--> ")
    if cmd.strip() == "": 
        break
    modcmd(expand(cmd))

