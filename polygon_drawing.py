import matplotlib.pyplot as plt
from matplotlib.widgets import PolygonSelector
import numpy as np

fig2, ax2 = plt.subplots()
fig2.show()

selector2 = PolygonSelector(ax2, lambda *args: None)

print("Click on the figure to create a polygon.")
print("Press the 'esc' key to start a new polygon.")
print("Try holding the 'shift' key to move all of the vertices.")
print("Try holding the 'ctrl' key to move a single vertex.")

plt.show()

with open('test.txt', 'w') as f:
    for vert in selector2.verts:
        line = "%f %f" % (vert[0], vert[1])
        f.write(line)        
        print(line)
        
    
# verts = np.array(selector2.verts)
# with open('verts.poly', 'wb') as zf:
#     np.save(f, verts, allow_pickle=False)
# print(verts)