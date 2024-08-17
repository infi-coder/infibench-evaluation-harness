# Check: train_loader and validation_loader has no overlap (1 point)

embed_idx = []
size = 0

for data in train_loader:
    img_x = data[0][:,0,0,0,0]
    img_y = data[0][:,0,0,1,0]
    embed_idx.extend((img_x * 200 + img_y).tolist())
    size += len(data[0])

for data in validation_loader:
    img_x = data[0][:,0,0,0,0]
    img_y = data[0][:,0,0,1,0]
    embed_idx.extend((img_x * 200 + img_y).tolist())
    size += len(data[0])

embed_idx = len(set(embed_idx))
assert embed_idx == size
