import os
#to get the current working directory
import matplotlib.pyplot as plt
import numpy as np
directory = os.getcwd()

exp_name = "hand_drawing.1"
poly_file = directory + "/%s.node" % exp_name

f = open(poly_file, 'r')
first_line = f.readline().strip()
num_vertices = int(first_line.split(" ")[0])
print(num_vertices)
fig, ax = plt.subplots()

x_coords = []
y_coords = []
list_is_boundary = []
for i in range(num_vertices):
    line = f.readline().strip()
    temp = line.split()
    x_coord = float(temp[1])
    y_coord = float(temp[2])
    x_coords.append(x_coord)
    y_coords.append(y_coord)
    is_boundary = int(temp[3])
    print_str = "%f %f\n" % (x_coord, y_coord)
    list_is_boundary.append(is_boundary)
    print(print_str)    

    if is_boundary:            
        ax.scatter(x_coord, y_coord, c='red', zorder=2)    


ele_file = directory + "/%s.ele" % exp_name

f = open(ele_file, 'r')
first_line = f.readline().strip()
num_elements = int(first_line.split()[0])
print('num_elements: %d' % num_elements)

#line = f.readline().strip()
# num_edges = int(line.split(" ")[0])
# print('num_edges:  ', num_edges)

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
plt.title("Mesh")
#ax.triplot(triang, 'ko-')
ax.triplot(triang, 'ko-', zorder=1)

plt.xlim([0, 1.0])
plt.ylim([0, 1.0])

# node_file = directory + "/%s.node" % exp_name

# f = open(edge_file, 'r')
# first_line = f.readline().strip()
# num_edges = int(first_line.split()[0])
# print('num_edges: %d' % num_edges)

# for i in range(num_edges):
#     line = f.readline().strip()
#     temp = line.split()    
#     is_boundary = int(temp[3])
#     if is_boundary:
#         vertex1_index = int(temp[1])
#         vertex2_index = int(temp[2])
#         print("is_boundary: %d" % is_boundary)
#         boundary_points_x = [x_coords[vertex1_index], x_coords[vertex2_index]]
#         boundary_points_y = [y_coords[vertex1_index], y_coords[vertex2_index]]
#         ax.scatter(boundary_points_x, boundary_points_y, c='red', zorder=2)
#     #temp[1]
#     #temp[2]
    


plt.show()

# plt.show()