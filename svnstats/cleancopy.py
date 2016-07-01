#!/usr/bin/env python

import os, shutil, stat
import sys, traceback

g_quiet = False
g_logfile = False
g_delete = True
g_verbose = False

g_verboten_files = set([
    '.git',
    '.settings',
    '_debug',
])

console = []

# Adds string with new line for further writing to file.
def log(msg):
    if not g_quiet and not g_logfile:
        print(msg)
    if g_logfile:
        console.append(msg + "\n")


def remove_readonly(fn, path, excinfo):
    try:
        os.chmod(path, stat.S_IWRITE)
        fn(path)
    except Exception as exc:
        log("Skipped " + path + " because: \n\t" + str(exc))


#
# Use SVN ST command to get files
#
def get_alien_files__pipe():

    log("using pipes\n")

    for line in os.popen('svn st --no-ignore'):
        if not line.strip():
            continue
        st, filename = line.split(None, 1)
        filename = filename.strip()
        if st in 'I?' and filename not in g_verboten_files:
            yield filename


#
# Parse SVN directory to get info about files
#
def get_alien_files__entries(top='.'):
    log("using entries\n")

    from os.path import join, isdir, exists, islink
    entries_file = join(top, '.svn/entries')
    if not exists(entries_file):
        # print 'Not exists:', entries_file
        return
    # print 'Entering', top
    entries = open(entries_file).read().split('\x0c\n')
    versioned = set(entry.split('\n', 1)[0] for entry in entries[1:-1])
    present = set(os.listdir(top)) - set(['.svn'])
    if top == '.':
        top = ''
    for non_versioned in present - versioned:
        candidate = join(top, non_versioned)
        if isdir(candidate) and not islink(candidate) and exists(join(candidate, '.svn')):
            # caveat: this is an external working copy
            continue
        yield candidate
    for entry in versioned:
        maybe_subdir = join(top, entry)
        if isdir(maybe_subdir):
            for alien in get_alien_files__entries(maybe_subdir):
                yield alien


def main():
    svn = os.popen('svn st')

    for line in svn:
        if g_verbose:
            log (line)

    status = svn.close()

    if status == None:
        files_generator = get_alien_files__pipe()
    else: 
        files_generator = get_alien_files__entries() 

    for filename in files_generator:

        if filename.lower() == "cleancopy.log":
            continue

        try:
            if os.path.islink(filename):
                log(filename+' (SYMLINK)')
            elif os.path.isdir(filename):
                if g_delete:
                    shutil.rmtree(filename, onerror=remove_readonly)
                log(filename+' (DIR)')
            else:
                if g_delete:
                    os.chmod(filename, stat.S_IWRITE)
                    os.unlink(filename)
                log(filename)
        except WindowsError as e:
                log("Exception:")
                log("\t"+str(e))

if __name__ == '__main__':
    args = set(sys.argv[1:])
    if set(['-t', '-n', '--dry-run']) & args:
        g_delete = False
    if set(['-v', '--verbose']) & args:
        g_verbose = True
    if set(['-q', '--quiet']) & args:
        g_quiet = True
    if set(['-l', '--log']) & args:
        g_logfile = True

    if not g_delete:
        log('Simulation only.')

    try:
        main()
    except Exception as e:
        print "Some problems occurred:\n---------\n%s\n----------\n" % traceback.format_exc()
        log("Exception:")
        log(traceback.format_exc())

    if g_logfile:
        with open("cleancopy.log", "w") as logfile:
            logfile.writelines(console)



