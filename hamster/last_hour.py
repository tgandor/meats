import glob
import os
import time


hour_ago = time.strftime('IMG_%Y%m%d_%H%M%S.jpg', time.localtime(time.time() - 3600))
print(hour_ago)

os.chdir('/mnt/sdcard/DCIM/Camera')

for img in glob.glob('IMG_*'):
    print(img)
    if img > hour_ago:
        base, _ = os.path.splitext(img)
        os.rename(img, base + '.bak')
        print('... renamed')

for bak in glob.glob('*.bak'):
    os.rename(bak, '../../documents/'+bak)
    print(bak)

