#!/usr/bin/env python

import os
import sys
import time

def ensure_command(command, package):
	check_command = 'which' if sys.platform.startswith('linux') else 'where'
	command_line = '{0} {1}'.format(check_command, command)
	if os.system(command_line) == 0:
		return
	if sys.platform.startswith('linux'):
		sys.stderr.write(
			"'{0}' command missing. Trying to install '{1}' package...\n"
			.format(command, package)
		)
		os.system('sudo apt-get install {0}'.format(package))
		if os.system(command_line) == 0:
			return
	sys.stderr.write('{0}: command not found.\n'.format(command))
	exit(1)

if len(sys.argv) < 2:
    sys.stderr.write('Usage: {0} URL\n'.format(sys.argv[0]))
    exit(1)

ensure_command('svn', 'subversion')

url_parts = sys.argv[1].split('/')

if url_parts[-1] == '':
    url_parts.pop()

folder_name = ''

if url_parts[-1] == 'trunk':
    folder_name = url_parts[-2]

if url_parts[-2] == 'branches':
    folder_name = '{0}_{1}'.format(url_parts[-3], url_parts[-1])

command = 'svn co {0} {1}'.format(sys.argv[1], folder_name)
sys.stderr.write('{0}\n'.format(command))
start_time = time.time()
os.system(command)
elapsed = time.time() - start_time
sys.stderr.write('Done. {0:.1f}s elapsed ({1:02}:{2:.1f}).'.format(
	elapsed, int(elapsed/60), elapsed % 60))
