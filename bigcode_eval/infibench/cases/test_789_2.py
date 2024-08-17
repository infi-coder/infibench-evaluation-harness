# train_loader and validation_loader has expected sizes (1 point)

train_size = 0
for data in train_loader:
    train_size += len(data[0])

val_size = 0
for data in validation_loader:
    val_size += len(data[0])

assert train_size + val_size == 5000

