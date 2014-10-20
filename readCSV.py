#CSV READER

import bpy
from time import time
import os
import json

def clip(val,minVal=0.0, maxVal=1.0):
    """clip(val, minVal=0.0, maxVal=1.0
    Clips 'val' between minVal and maxVal"""
    return min(maxVal, max(minVal, val))

def ranger(val, minVal=0.0, maxVal=1.0):
    """ranger(val, minVal=0.0, maxVal=1.0)
    Shifts and scales val such that any number
    between minVal and maxVal will be between 0.0
    and 1.0 respectively.  Does not clip.
    
    eg: ranger(val=-1.0, minVal=0.5, maxVal=2.5)
    returns: (-1.0 - 0.5) / (2.5-0.5) = -0.75

    eg2: ranger(val=100, minVal=50, maxVal=250):
    returns: (100 - 50) / (250-50) = 0.25
    """
    return (val-minVal)/(maxVal-minVal)

def rangeSet(val, minVal=0.0, maxVal=1.0):
    """rangeSet(val, minVal=0.0, maxVal=1.0)
    Scales val using ranger with minVal and maxVal as
    inputs, then clips all values below 0.0 or above 1.0
    using clip."""
    ranged=ranger(val, minVal, maxVal)
    return clip(ranged)

beginTime=time()

class PointCloudClass():
    def __init__(self,setup,mesh):
        self.fname=setup['fname']
        self.x=setup['x']
        self.y=setup['y']
        self.z=setup['z']
        self.Col1=setup['Col']
        self.Col2=setup['Col2']
        
        self.mesh=mesh
        
        
    def loadItter(self,n):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set()

    

if os.path.isfile('/User/djortley/Desktop/df/setup.json'):
    fid=open('/Users/djortley/Desktop/df/setup.json','r')
    setup=json.load(fid)
    fid.close()

    mesh=bpy.data.meshes.new('PointCloud')
    object=bpy.data.objects.new('PointCloud',mesh)
    
    

    


tmp=fid.readline()

pt=[]
nVal=[]
colDict={}

lines=fid.readlines()
fid.close()
lines=[v.strip().split(',') for v in lines]

for xx,yy,zz,nn in lines:
    pt.append((float(xx),float(yy),float(zz)))
    nVal.append(rangeSet(float(nn),0.0, 4.0))

#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.mesh.select_all(action='TOGGLE')
#bpy.ops.mesh.delete(type='VERT')
#bpy.ops.object.mode_set()

scene=bpy.context.scene
sceneLinked=scene.objects.link(object)
scene.objects.active=object
object.select=True

Col=mesh.vertex_colors.new()
oldLen=0
for p,n in zip(pt,nVal):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,size=0.07,location=p)
    #bpy.ops.mesh.primitive_ico_sphere_add(size=0.07,location=p)
    #bpy.ops.mesh.primitive_cube_add(location=p,radius=0.07)
    bpy.ops.object.mode_set()
    nn = rangeSet(n, 0.0, 1.0)
    newLen=len(Col.data)
    print(oldLen,newLen)
    for i in range(oldLen,newLen):
        mesh.vertex_colors['Col'].data[i].color[0]=nn
        mesh.vertex_colors['Col'].data[i].color[1]=nn
        mesh.vertex_colors['Col'].data[i].color[2]=nn
        
    oldLen=newLen
    #tmp=[m.index for m in mesh.polygons if m.select]
    #for t in tmp: colDict[t]=n

vertlist=bpy.context.active_object.data.vertices
polylist=bpy.context.active_object.data.polygons
colorlist=bpy.context.active_object.data.vertex_colors[0].data

scene.update()
endTime=time()
print(endTime-beginTime)
