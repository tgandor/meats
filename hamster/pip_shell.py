#qpy:console
import os
import os.path
import sys
#sys.dont_write_bytecode = True


class CmdCache:
    last_cmd = ''


def history_expand(cmd):
    if '!$' in cmd and last_cmd.strip():
        cmd = cmd.replace('!$', CmdCache.last_cmd.split()[-1])
    if '!!' in cmd:
        cmd = cmd.replace('!$', CmdCache.last_cmd)
    if '!yt' in cmd:
        cmd = cmd.replace('!yt', 'youtube_dl')
    CmdCache.last_cmd = cmd
    return cmd


def modcmd(arg):
    arg = 'pip ' + history_expand(arg)
    cmd = sys.executable + " " + sys.prefix + "/bin/" + arg
    print(cmd)
    os.system(cmd)


if not(os.path.exists(sys.prefix+"/bin/pip")):
    print("You need to install pip first.")
    exit()

print("Input pip commands, ie: pip install {module}")

shorthands = {
    'i': 'install',
    'u': 'install --upgrade',
    'f': 'freeze',
    's': 'search --index https://pypi.python.org/pypi',
    'd': 'uninstall',
    'h': 'help'
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
    if cmd.strip() == '?':
        print("Shorthands:")
        for k in shorthands:
            print("{}: {}".format(k, shorthands[k]))
        continue
    modcmd(expand(cmd))
