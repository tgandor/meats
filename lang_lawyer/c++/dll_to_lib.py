# Windows, MSVS Tools in path, only...

import os
import struct
import sys

def arch_of(dll_file):
    with open(dll_file, 'rb') as f:
        doshdr = f.read(64)
        magic, padding, offset = struct.unpack('2s58si', doshdr)
        # print magic, offset
        if magic != 'MZ':
            return None
        f.seek(offset, os.SEEK_SET)
        pehdr = f.read(6)
        # careful! H == unsigned short, x64 is negative with signed
        magic, padding, machine = struct.unpack('2s2sH', pehdr)
        # print magic, hex(machine)
        if magic != 'PE':
            return None
        if machine == 0x014c:
            return 'i386'
        if machine == 0x0200:
            return 'IA64'
        if machine == 0x8664:
            return 'x64'
        return 'unknown'


class DumbPinReader:
    def __init__(self):
        self.funcs_expected = 0
        self.funcs_found = 0
        self.phase = self.find_number
        self.functions = []

    def process(self, line):
        self.phase(line)

    def find_number(self, line):
        if 'number of functions' in line:
            self.funcs_expected = int(line.split()[0])
            self.phase = self.wait_for_list

    def wait_for_list(self, line):
        if line.split() == 'ordinal hint RVA      name'.split():
            self.phase = self.scan_symbols

    def scan_symbols(self, line):
        if line.strip() == 'Summary':
            self.phase = self.idle
            return
        ordinal, hint, rva, name = line.split()[:4]
        print('Function {} @{}'.format(name, ordinal))
        self.functions.append((name, ordinal))
        self.funcs_found += 1

    def idle(self, line):
        pass


def generate_def(functions, dll_file):
    def_file = dll_file.lower().replace('.dll', '.def')
    with open(def_file, 'w') as f:
        f.write('LIBRARY {}\nEXPORTS\n'.format(dll_file))
        for name, ordinal in functions:
            f.write('\t{} @{}\n'.format(name, ordinal))
    return def_file

# this should crash when missing Visual Studio
vs_tools = os.environ[max([f for f in os.environ if f.startswith('VS')])]
lib_cmd = '""{}..\\..\\VC\\bin\\lib.exe""'.format(vs_tools)
dumpbin_cmd = '""{}..\\..\\VC\\bin\\dumpbin.exe""'.format(vs_tools)

dll_file = sys.argv[1]
arch = arch_of(dll_file)

if not arch:
    print('Not a DLL file. Exiting.')
    exit()

exports = os.popen('{} /nologo /exports {}'.format(dumpbin_cmd, dll_file)).readlines()

processor = DumbPinReader()

for line in exports:
    if line.strip() == '':
        continue
    processor.process(line)


if processor.funcs_found != processor.funcs_expected:
    print('Warning: expected {} functions, found {}'.format(processor.funcs_expected, processor.funcs_found))

def_file = generate_def(processor.functions, dll_file)

command = '%s /machine:%s /def:%s' % (lib_cmd, arch, def_file)
print(command)
if os.system(command) != 0:
    print('LIB failed')


