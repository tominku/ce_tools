import os
#to get the current working directory
import matplotlib.pyplot as plt
import numpy as np
directory = os.getcwd()

poly_file = directory + "/A.poly"

f = open(poly_file, 'r')
first_line = line = f.readline().strip()
num_vertices = int(first_line.split(" ")[0])
print(num_vertices)

x_coords = []
y_coords = []
for i in range(num_vertices):
    line = f.readline().strip()
    x_coord = line.split(" ")[1]    
    y_coord = line.split(" ")[2]
    x_coords.append(x_coord)
    y_coords.append(y_coord)
    print(x_coord + ", " + y_coord)
# print(first_line)
# while True:
#     line = f.readline().strip()
#     if not line: break
#     print(line)
# f.close()

fig, ax = plt.subplots()
ax.scatter(x_coords, y_coords)
plt.show()