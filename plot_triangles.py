import os
#to get the current working directory
import matplotlib.pyplot as plt
import numpy as np
directory = os.getcwd()

exp_name = "A.1"
poly_file = directory + "/%s.node" % exp_name

f = open(poly_file, 'r')
first_line = f.readline().strip()
num_vertices = int(first_line.split(" ")[0])
print(num_vertices)
fig, ax = plt.subplots()

x_coords = []
y_coords = []
for i in range(num_vertices):
    line = f.readline().strip()
    temp = line.split()
    x_coord = float(temp[1])
    y_coord = float(temp[2])
    x_coords.append(x_coord)
    y_coords.append(y_coord)
    print_str = "%f %f\n" % (x_coord, y_coord)
    print(print_str)    


ele_file = directory + "/%s.ele" % exp_name

f = open(ele_file, 'r')
first_line = f.readline().strip()
num_elements = int(first_line.split()[0])
print('num_elements: %d' % num_elements)

#line = f.readline().strip()
# num_edges = int(line.split(" ")[0])
# print('num_edges: ', num_edges)

triangles = []
for i in range(num_elements):
    line = f.readline().strip()
    temp = line.split()    
    triangle = [int(temp[1])-1, int(temp[2])-1, int(temp[3])-1]
    triangles.append(triangle)
    print(triangle)
    #print("triangle: %d %d %d" % (int(temp[0]), int(temp[1]), int(temp[2])))

import matplotlib.tri as mtri

triang = mtri.Triangulation(x_coords, y_coords, triangles)
plt.title("triangular grid")
plt.triplot(triang, 'ko-')
plt.show()

# # plt.xlim([0, 1.0])
# # plt.ylim([0, 1.0])
# plt.show()