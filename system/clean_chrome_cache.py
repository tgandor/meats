from pathlib import Path
import shutil

LOCATIONS = [
    '~/.config/chromium/Default/Service Worker/CacheStorage/',
    '~/.config/google-chrome/Default/Service Worker/CacheStorage/',
]

def get_size(path: str) -> int:
    return sum(p.stat().st_size for p in Path(path).expanduser().rglob('*'))


total = 0
after = 0

for location in LOCATIONS:
    print(location)
    size = get_size(location)
    total += size
    print("- before: {:,}".format(size))
    p = Path(location).expanduser()
    for subdir in p.glob('*/'):
        shutil.rmtree(subdir)
    size = get_size(location)
    after += size
    print("- after:  {:,}".format(size))

print("Total deleted: {:,}".format(total - after))
