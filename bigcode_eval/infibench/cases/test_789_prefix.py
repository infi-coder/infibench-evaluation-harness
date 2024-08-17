

import pandas as pd
import numpy as np
from torch.utils.data.dataset import Dataset


class CustomDatasetFromCSV(Dataset):
    def __init__(self, csv_path, transform=None):
        self.data = pd.read_csv(csv_path)
        try:
            self.labels = pd.get_dummies(self.data['emotion']).as_matrix()
        except Exception:
            self.labels = pd.get_dummies(self.data['emotion']).values
        self.height = 48
        self.width = 48
        self.transform = transform

    def __getitem__(self, index):
        pixels = self.data['pixels'][index]
        faces = []
        face = np.asarray(eval(pixels)).reshape(self.width, self.height)
        faces.append(face.astype('float32'))
        faces = np.asarray(faces)
        faces = np.expand_dims(faces, -1)
        return faces, self.labels[index]

    def __len__(self):
        return len(self.data)

my_path = 'tmp.csv'

d = []
for i in range(5000):
    now_data = {'emotion': i % 50, 'pixels': np.random.randint(0, 255, (48, 48), int)}
    now_data['pixels'][0, 0] = i // 200
    now_data['pixels'][0, 1] = i % 200
    now_data['pixels'] = now_data['pixels'].tolist()
    d.append(now_data)
df = pd.DataFrame(data=d)
df.to_csv(my_path)

dataset = CustomDatasetFromCSV(my_path)

