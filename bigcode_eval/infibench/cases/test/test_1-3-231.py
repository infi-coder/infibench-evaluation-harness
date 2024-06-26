def f(tensor):
    return [t.size() for t in tensor]
import torch
t = [torch.tensor([1, 2, 3,1]), torch.tensor([4, 5, 6]),
      torch.tensor([7, 8, 9,1,1,1]), torch.tensor([10, 11]),
      torch.tensor([13, 14, 15, 0])]

import torch
'''
def getSize(t):
    sizes = [tensor.size() for tensor in t]
    return sizes
'''
# Example usage:
tensors_list = [torch.tensor([1, 2, 3]), torch.tensor([4, 5])]
sizes = getSize(tensors_list)
print(sizes)

assert getSize(t) == f(t)
