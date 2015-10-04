#import scipy.misc.imshow as imshow
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread

img = imread("map.png")
bb = [ -6.3504, -6.2189, 53.3206, 53.3761]
#ar = (bb[1]-bb[0])/(bb[3]-bb[2])
ar = 1265.0/893.0   # run cmd: $file map.png

stations = 10
xx = [np.random.uniform(bb[0],bb[1]) for x in range(stations)]
yy = [np.random.uniform(bb[2],bb[3]) for x in range(stations)]
print xx
print yy
plt.imshow(img,zorder=0, extent=bb, aspect = ar)
plt.plot(xx, yy, 'bo')
plt.show()
