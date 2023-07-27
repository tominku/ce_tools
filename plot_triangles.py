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

def circumcenter(p1, p2, p3):    
    ax = p1[0]
    ay = p1[1]
    bx = p2[0]
    by = p2[1]
    cx = p3[0]
    cy = p3[1]
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return (ux, uy)

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
    #print(print_str)    

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
vertIdxToEdges = {}
for i in range(num_elements):
    line = f.readline().strip()
    temp = line.split()    
    vert_idx1 = int(temp[1])-1
    vert_idx2 = int(temp[2])-1
    vert_idx3 = int(temp[3])-1
    triangle = [vert_idx1, vert_idx2, vert_idx3]
    cc = circumcenter((x_coords[vert_idx1], y_coords[vert_idx1]),
                       (x_coords[vert_idx2], y_coords[vert_idx2]),
                        (x_coords[vert_idx3], y_coords[vert_idx3]))
    triangles.append(triangle)
    vert_indices = [vert_idx1, vert_idx2, vert_idx3]
    for vert_index in vert_indices:
        if vert_index not in vertIdxToEdges:
            vertIdxToEdges[vert_index] = {}
        for vert_neigh_index in vert_indices:
            if vert_neigh_index == vert_index:
                continue
            else:
                edge = [vert_index, vert_neigh_index]
                edgeID = "%d, %d" % (vert_index, vert_neigh_index)
                if edgeID not in vertIdxToEdges[vert_index]: 
                    vertIdxToEdges[vert_index][edgeID] = []
                #vertIdxToEdges[vert_index][edgeID].append(triangle)
                vertIdxToEdges[vert_index][edgeID].append(cc)
    
    #print(triangle)
    #print("triangle: %d %d %d" % (int(temp[0]), int(temp[1]), int(temp[2])))

#print(vertIdxToEdges)

for vert_index in vertIdxToEdges.keys():
    edgeIdToCCs = vertIdxToEdges[vert_index]
    #print(len(edgeIdToCCs.keys()))
    for edgeID in edgeIdToCCs.keys():
        ccs_for_the_edge = edgeIdToCCs[edgeID]
        #print(len(ccs_for_the_edge))
        xs_of_ccs = []
        ys_of_ccs = []
        for cc in ccs_for_the_edge:
            xs_of_ccs.append(cc[0])
            ys_of_ccs.append(cc[1])
            #ax.scatter(cc[0], cc[1], c='green', zorder=11, s=2)            
        ax.scatter(xs_of_ccs, ys_of_ccs, c='green', zorder=11, s=2)            
        ax.plot(xs_of_ccs, ys_of_ccs, c='blue', zorder=12)            

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

#triangle -peqD a0.001 hand_drawing.poly