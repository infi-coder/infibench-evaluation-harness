import os
for file in ['figure.pdf']:
    if os.path.exists(file):
        os.remove(file)
