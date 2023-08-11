import numpy as np
import matplotlib.pyplot as plt

width = 2.5 * np.pi
height = np.pi

nx = 20 
ny = 10

# nx = 40 
# ny = 20

# nx = 60 
# ny = 30

walls = []

# left_wall
left_wall = np.array([np.zeros(shape=(ny,)), np.linspace(0, height, ny)])
print(left_wall.shape)
#print(left_wall)

# top_wall
top_wall = np.array([np.linspace(0, width, nx), height*np.ones(shape=(nx,))])[:, 1:]
print(top_wall.shape)
#print(top_wall)

# right_wall
right_wall = np.array([width*np.ones(shape=(ny,)), np.linspace(0, height, ny)])
right_wall = np.flip(right_wall, axis=1)[:, 1:]
print(right_wall.shape)

# bottom_wall
bottom_wall = np.array([np.linspace(0, width, nx), np.zeros(shape=(nx,))])
bottom_wall = np.flip(bottom_wall, axis=1)[:, 1:-1]
print(bottom_wall.shape)

walls.append(left_wall)
walls.append(top_wall)
walls.append(right_wall)
walls.append(bottom_wall)

dic_walls = {'left_wall':left_wall, 'top_wall':top_wall, 'right_wall':right_wall, 'bottom_wall':bottom_wall}


num_vertices = 0
verts = []
xs = []
ys = []
fig, ax = plt.subplots(figsize=(8, 8))
top_wall_indices = []
right_wall_indices = []

vert_index = 0
for key, val in dic_walls.items():
    wall = dic_walls[key]
    num_points = wall.shape[1]
    num_vertices += num_points
    for i in range(num_points):
        x = wall[0, i]
        y = wall[1, i]
        vert_index += 1
        if key is 'top_wall':
            top_wall_indices.append(int(vert_index))
        elif key is 'right_wall':            
            right_wall_indices.append(int(vert_index))
        vert = (x, y)
        verts.append(vert)        
        xs.append(x)
        ys.append(y)        

np.savetxt('top_wall_indices.txt', top_wall_indices, '%d')
np.savetxt('right_wall_indices.txt', right_wall_indices, '%d')
# for wall in walls:
#     num_points = wall.shape[1]
#     num_vertices += num_points
#     for i in range(num_points):
#         x = wall[0, i]
#         y = wall[1, i]
#         vert = (x, y)
#         verts.append(vert)
#         xs.append(x)
#         ys.append(y)        

print(num_vertices)
assert(num_vertices == len(verts))

ax.axis('equal')
ax.scatter(xs, ys, s=5, c="blue")

do_add_random_points = True

#save rect boundary
first_line = "%d 2 0 0\n" % num_vertices
i = 1
with open('rect_boundary.poly', 'w') as f:
    
    # vertices
    f.write(first_line)
    for vert in verts:
        line = "%d %f %f\n" % (i, vert[0], vert[1])
        f.write(line)        
        #print(line)
        i += 1

    # if do_add_random_points:
    #     line = "%d %f %f\n" % (i, width * (0.2 + np.random.rand()*0.6), height * (0.2 + np.random.rand()*0.6))
    #     f.write(line)        

    # edges
    num_edges = num_vertices
    first_line = "%d 0\n" % num_edges
    f.write(first_line)
    for i in range(num_edges):
        edge_v1_index = i+1
        edge_v2_index = i+2
        if edge_v2_index > num_edges:
            edge_v2_index = 1
        line = "%d %d %d\n" % (i+1, edge_v1_index, edge_v2_index)
        f.write(line)        
        #print(line)    
        ax.plot([verts[edge_v1_index-1][0], verts[edge_v2_index-1][0]],
                 [verts[edge_v1_index-1][1], verts[edge_v2_index-1][1]], c='green')            
    
    # holes
    f.write("0")



plt.show()

#triangle -peqDY -a0.01 rect_boundary.poly