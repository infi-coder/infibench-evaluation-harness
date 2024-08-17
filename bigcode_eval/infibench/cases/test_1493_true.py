import shutil

file_list = ['a.txt', 'c.txt', 'b.txt', 'zzz.txt']
dest_folder = 'my_dest'

import os
if os.path.exists(dest_folder):
    shutil.rmtree(dest_folder)
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

for f in file_list:
    with open(f, 'w') as ff:
        pass

copy_from_file_list([[item, '1'] for item in file_list], dest_folder)

for file in os.listdir(dest_folder):
    assert file in file_list
assert len(os.listdir(dest_folder)) == len(file_list)