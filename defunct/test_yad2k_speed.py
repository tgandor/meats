import re
import subprocess
from itertools import count
import csv

sizes = count(1)  # [1, 5, 25]
fakeing = ['--fake-batch', '']

input_video = '-i f3-s1-test1.mp4'
out_of_memory = False

with open('results.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['batch', 'fake', 'real'])
    for size in sizes:
        if out_of_memory:
            print('Memory limit reached')
            break
        row = [size]
        for fake in fakeing:
            print('batch size', size, fake)
            process = subprocess.Popen('python test_yolo_webcam.py --batch-size {} {} --limit {} --test {}'.format(
                size, fake, 5 if fake else 5 * size, input_video
            ), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            results, errors = [x.decode() for x in process.communicate()]

            last_line = results.strip().split('\n')[-1]
            avg = float(re.findall(r'avg=(\d+.\d+)', last_line)[0])
            row.append(avg)
            print(last_line)

            if 'ran out of memory trying to allocate' in errors:
                out_of_memory = True

        writer.writerow(row)
