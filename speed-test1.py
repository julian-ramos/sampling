
import statsmodels.api as sm
import numpy as np
import timeit

def new():
    a=np.array([1,1,1,1,1,2,2,2,2,2])
    b=np.array([1,1,1,2,2,2,3,4,2,2])
    d=np.zeros(len(a))
    c=np.where(a==b)
    d[c]+=1
    return d
    
def prev():
    a=np.array([1,1,1,1,1,2,2,2,2,2])
    b=np.array([1,1,1,2,2,2,3,4,2,2])
    d=np.zeros(len(a))
    c=np.equal(a,b)
    for i in range(len(c)):
        if c[i]:
            d[i]=d[i]+1
    return d
        

# print(new())
# print(prev())

r1=timeit.timeit("new()",number=100000,setup="import numpy as np;from __main__ import new")
r2=timeit.timeit("prev()",number=100000,setup="import numpy as np;from __main__ import prev")
print("New \t\t %f \nprevious \t %f \nimprovement \t %f"%(r1,r2,100*(r2-r1)/r2))  

    
   




