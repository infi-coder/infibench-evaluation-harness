import os
for file in ['tmp0.png', 'tmp.bmp']:
    if os.path.exists(file):
        os.remove(file)