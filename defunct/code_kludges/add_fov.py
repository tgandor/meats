
import sys
import glob


def skip_cons_empty(data):
    result = data[:1]
    for line in data[1:]:
        if line.strip() == '':
            if result[-1].strip() != '':
                result.append('')
            continue
        result.append(line)
    return result
    

def fix_spaces(line):
    return line.replace('    ', '\t')


def save_with_check(filename, data):
    old_data = open(filename).read()
    if data != old_data:
        print('{} - file changed'.format(filename))
        open(filename, 'w').write(data)
        return True
    
    print('{} - up to date'.format(filename))
    return False
        

for f in glob.glob(sys.argv[1]):
    fov = f.split('.')[0].split('_')[-1]
    fov_line = '\tinclude "../fovs/{}.hrp"'.format(fov)
    
    data = open(f).read().split('\n')[::-1]
    data = list(map(fix_spaces, data))
    data = skip_cons_empty(data)
    
    if fov_line not in data:
        print('fov missing: {}'.format(f))
        idx = data.index('}')
        data.insert(idx+1, fov_line)
    
    content = '\n'.join(data[::-1])
    if not content.endswith('\n'):
        content += '\n'
    if save_with_check(f, content):
        print(content)
    print('-' * 60)

