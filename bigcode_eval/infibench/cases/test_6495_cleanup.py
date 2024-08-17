import os
for file in ['tmp.png']:
    if os.path.exists(file):
        os.remove(file)