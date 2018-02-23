import math
import numpy as np

z3 = np.zeros(3)
pi = math.pi
U = 32768

def a3(V): 
    try : a = np.array([V.X,V.Y,V.Z])
    except : 
        try :a = np.array([V.Pitch,V.Yaw,V.Roll])
        except : a = np.array([V[0],V[1],V[2]])
    return a

def a2(V): 
    return np.array([V[0],V[1]])

def sign(x):
    if x>0 : return 1
    else : return -1

def d3(A,B=[0,0,0]):
    return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2)

def d2(A,B=[0,0]):
    return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)

def Range(v,r):
    if abs(v)>r:
        v = math.copysign(r,v)
    return v

def Range180(x,pi):
    x = x - abs(x)//(2*pi) * (2*pi) * sign(x)
    x = x - int(abs(x)>pi) * (2*pi) * sign(x)
    return x

def ang_dif(a1,a2,pi):
    return abs(Range180(a1-a2,pi))

def mid_ang(a1,a2,pi=pi):
    return Range180(Range180(a1-a2,pi)/2 + a2,pi)
 
def pos(v):
    if v<0:
        v = 0
    return v

def rotate2D(x,y,ang):
    x2 = x*math.cos(ang) - y*math.sin(ang)
    y2 = y*math.cos(ang) + x*math.sin(ang)
    return x2,y2

def local(tL,oL,oR,Urot=True):
    L = tL-oL
    if Urot :
        pitch = oR[0]*pi/U
        yaw = Range180(oR[1]-U/2,U)*pi/U
        roll = oR[2]*pi/U
        R = -np.array([pitch,yaw,roll])
    else :
        R = -oR
    x,y = rotate2D(L[0],L[1],R[1])
    y,z = rotate2D(y,L[2],R[0])
    x,z = rotate2D(x,z,R[2])
    return x,y,z

def spherical(x,y,z,Urot=True):
    d = math.sqrt(x*x+y*y+z*z)
    if d!=0 : i = math.acos(z/d)
    else: i=0
    a = math.atan2(y,x)
    if Urot : return d, Range180(a/pi-.5,1), Range180(i/pi-.5,1)
    else : return d,a,i
    # https://en.wikipedia.org/wiki/Spherical_coordinate_system

def cartesian(d,a,i):
    x = d * math.sin(i) * math.cos(a)
    y = d * math.sin(i) * math.sin(a)
    z = d * math.cos(i)
    return x,y,z

def regress(a):
    cond = abs(a)>.08
    return cond*sign(a) + (1-cond)*12.5*a

def line_intersect(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0 : div = 1
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
