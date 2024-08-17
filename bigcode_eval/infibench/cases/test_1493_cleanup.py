import shutil
import os

file_list = ['a.txt', 'c.txt', 'b.txt', 'zzz.txt']
dest_folder = 'my_dest'

for ff in file_list:
    if os.path.exists(ff):
        os.remove(ff)

if os.path.exists(dest_folder):
    shutil.rmtree(dest_folder)
