# integer overflow 

import numpy as np 

a_0 = np.array([2147483647], dtype="int32")

print(a_0-1)

print(a_0+5)

print(2147483647+1)
