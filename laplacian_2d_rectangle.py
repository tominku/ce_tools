import os
#to get the current working directory
import matplotlib.pyplot as plt
import numpy as np
directory = os.getcwd()

exp_name = "rect_boundary.1"
poly_file = directory + "/%s.node" % exp_name

f = open(poly_file, 'r')
first_line = f.readline().strip()
num_vertices = int(first_line.split(" ")[0])
print('num_vertices: %d' % num_vertices)

#bc1 = {4: 1.0, 5: 1.0, 105: 1.0, 6: 1.0, 19: 0.0, 154: 0.0, 20: 0.0, "name": "bc1"}
bc1 = {"name": "bc1"}
#bc2 = {4: 0.0, 5: 0.0, 105: 0.0, 6: 0.0, 19: 1.0, 154: 1.0, 20: 1.0, "name": "bc2"}
bc2 = {"name": "bc2"}
bc_sum = {4: 1.0, 5: 1.0, 105: 1.0, 6: 1.0, 19: 1.0, 154: 1.0, 20: 1.0, "name": "bc_sum"}

#bc1 = {}

for i in range(20, 30 + 1):
    bc1[i] = 1.0

for i in range(70, 88 + 1):
    bc1[i] = 0.0    

#20~69
#69~88

#bc = bc2
#bc = bc1 
bc = bc1


fig, ax = plt.subplots(figsize=(8, 8))

def is_diri_conditioned(vert_index):
    return vert_index in bc.keys()

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
    return np.array((ux, uy))

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
    if is_boundary:            
        ax.text(x_coord, y_coord, "%d" % (i+1), color='black', zorder=20)
    print_str = "%f %f\n" % (x_coord, y_coord)
    list_is_boundary.append(is_boundary)
    #list_is_diri.append(False)
    #print(print_str)    

    if is_boundary:        
        color = "red"
        if is_diri_conditioned(i):    
             color = "green"                   
        
        ax.scatter(x_coord, y_coord, c=color, zorder=2)    



ele_file = directory + "/%s.ele" % exp_name

f = open(ele_file, 'r')
first_line = f.readline().strip()
num_elements = int(first_line.split()[0])
print('num_elements: %d' % num_elements)


triangles = []
vertIdxToNeighVertIndexToCCs = {}
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
        if vert_index not in vertIdxToNeighVertIndexToCCs:
            vertIdxToNeighVertIndexToCCs[vert_index] = {}
        for vert_neigh_index in vert_indices:
            if vert_neigh_index == vert_index:
                continue
            else:
                #edge = [vert_index, vert_neigh_index]
                #neighIdx = "%d %d" % (vert_index, vert_neigh_index)
                #neigh_vert_idx = vert_neigh_index
                if vert_neigh_index not in vertIdxToNeighVertIndexToCCs[vert_index]: 
                    vertIdxToNeighVertIndexToCCs[vert_index][vert_neigh_index] = []
                #vertIdxToEdges[vert_index][edgeID].append(triangle)
                vertIdxToNeighVertIndexToCCs[vert_index][vert_neigh_index].append(cc)
    
    #print(triangle)
    #print("triangle: %d %d %d" % (int(temp[0]), int(temp[1]), int(temp[2])))

#print(vertIdxToEdges)

def vertIdxToVert(vertIdx):
    x = x_coords[vertIdx]
    y = y_coords[vertIdx]
    return np.array((x, y))

A = np.zeros(shape=(num_vertices, num_vertices))
b = np.zeros(shape=(num_vertices,))


for vert_index in vertIdxToNeighVertIndexToCCs.keys():
    if is_diri_conditioned(vert_index):
        A[vert_index][vert_index] = 1.0
        b[vert_index] = bc[vert_index]
        continue
    neighVertIdxToCCs = vertIdxToNeighVertIndexToCCs[vert_index]
    #neigh_vert_indices = neighVertIdxToCCs.keys()
    #print(len(edgeIdToCCs.keys()))
    vert = vertIdxToVert(vert_index)
    sum_coeffs = 0.0
    for neigh_idx in neighVertIdxToCCs.keys():
        neigh_vert = vertIdxToVert(neigh_idx)
        l_ij = np.linalg.norm(neigh_vert - vert)
        is_boundary_edge = False
        if list_is_boundary[vert_index] and list_is_boundary[neigh_idx]:
            is_boundary_edge = True
                                
        ccs_for_the_edge = neighVertIdxToCCs[neigh_idx]       
        pt1 = ccs_for_the_edge[0]
        pt2 = []
        if len(ccs_for_the_edge) < 2: # boundary edge
            center_of_two_verts = (vert + neigh_vert) / 2.0
            pt2 = center_of_two_verts            
            continue
        else:
            pt2 = ccs_for_the_edge[1]       

        s_ij = np.linalg.norm(pt1 - pt2)
        coeff_ij = s_ij / l_ij    
        A[vert_index][neigh_idx] = -coeff_ij
        sum_coeffs += coeff_ij             
        
        ax.scatter([pt1[0], pt2[0]], [pt1[1], pt2[1]], c='green', zorder=11, s=2)            
        ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], c='blue', zorder=12)            

        ccs = np.array(ccs_for_the_edge)
        surface_len = np.linalg.norm(ccs[0, :] - ccs[1, :])

    A[vert_index][vert_index] = sum_coeffs

x = np.linalg.solve(A, b)
np.save(f'laplace_2d_sol_bc_{bc["name"]}', x)
np.savetxt(f'laplace_2d_sol_bc_{bc["name"]}', x)

import matplotlib.tri as mtri

ax.axis('equal')

triang = mtri.Triangulation(x_coords, y_coords, triangles)
plt.title("Mesh")
#ax.triplot(triang, 'ko-')
ax.triplot(triang, 'ko-', zorder=1)

plt.xlim([0, 1.0])
plt.ylim([0, 1.0])

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
cmhot = plt.get_cmap("hot")
p = ax.scatter(x_coords, y_coords, x, c=x, cmap=cmhot)
print(x)

fig.colorbar(p)
plt.show()

# plt.show()