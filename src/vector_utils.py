
def normalize(v):
    mod = (v[0]**2 + v[1]**2 +v[2]**2)**0.5
    if mod!=0:
        v[0] /= mod
        v[1] /= mod
        v[2] /= mod
        
def scale(v, factor):
    v[0] *= factor
    v[1] *= factor
    v[2] *= factor
    
def add(v1, v2):
    return [v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2]]
        
def sub(v1,v2):
    return [v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]]
  
def mult(v1, v2):
    return [v1[0]*v2[0], v1[1]*v2[1], v1[2]*v2[2]]    
    
def dot_product(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def cross_product(v1, v2):
    return [v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0]]

def modulus(v):
    return (v[0]**2+v[1]**2+v[2]**2)**0.5

def cos(v1, v2):
    if modulus(v1)==0 or modulus(v2)==0:
        return 0
    return dot_product(v1,v2)/(modulus(v1)*modulus(v2))

