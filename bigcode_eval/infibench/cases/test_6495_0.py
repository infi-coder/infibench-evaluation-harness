matrix = [[6000, 476, 789],
          [381, 2856, 93],
          [98, 187, 5384]]

x_labels = ['class A', 'class B', 'class C']
y_labels = ['class 1', 'class 2', 'class 3']

fig = plot_confusion_matrix(matrix, x_labels, y_labels)
fig.write_image("tmp.png")
