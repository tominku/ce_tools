import os
#to get the current working directory
import matplotlib.pyplot as plt
import numpy as np
directory = os.getcwd()

poly_file = directory + "/A.poly"

f = open(poly_file, 'r')
first_line = f.readline().strip()
num_vertices = int(first_line.split(" ")[0])
print(num_vertices)
fig, ax = plt.subplots()

x_coords = []
y_coords = []
for i in range(num_vertices):
    line = f.readline().strip()
    temp = line.split(" ")
    x_coord = float(temp[1])
    y_coord = float(temp[2])
    x_coords.append(x_coord)
    y_coords.append(y_coord)
    print_str = "%f %f\n" % (x_coord, y_coord)
    print(print_str)    
# print(first_line)
# while True:
#     line = f.readline().strip()
#     if not line: break
#     print(line)
# f.close()

line = f.readline().strip()
num_edges = int(line.split(" ")[0])
print('num_edges: ', num_edges)

for i in range(num_vertices):
    line = f.readline().strip()
    temp = line.split(" ")    
    vertex1_index = int(temp[1]) - 1
    vertex2_index = int(temp[2]) - 1

    print_str = "%d %d\n" % (vertex1_index, vertex2_index)
    print(print_str)    

    vertex1 = (x_coords[vertex1_index], y_coords[vertex1_index])
    vertex2 = (x_coords[vertex2_index], y_coords[vertex2_index])
    #x_coords.append(x_coord)
    #y_coords.append(y_coord)
    ax.plot([vertex1[0], vertex2[0]], [vertex1[1], vertex2[1]])



# plt.xlim([0, 1.0])
# plt.ylim([0, 1.0])
plt.show()