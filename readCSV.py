# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import os

def clipper(val,minVal=0.0, maxVal=1.0):
    """clipper(val, minVal=0.0, maxVal=1.0
       Clips 'val' between minVal and maxVal.
    """
    return min(maxVal, max(minVal, val))

def ranger(val, minVal=0.0, maxVal=1.0):
    """ranger(val, minVal=0.0, maxVal=1.0)
       Shifts and scales val such that any number between minVal and maxVal
       will be between 0.0 and 1.0 respectively.  Does not clip.

       Uses the equation: (val - minVal) / (maxVal - minVal)
    """
    return (val-minVal)/(maxVal-minVal)

def rangeSet(val, minVal=0.0, maxVal=1.0):
    """rangeSet(val, minVal=0.0, maxVal=1.0)
       Scales val using ranger with minVal and maxVal as inputs, then
       clips all values below 0.0 or above 1.0 using clip.
    """
    ranged=ranger(val, minVal, maxVal)
    return clipper(ranged)

class PointCloudClass():
    def __init__(self,fname):
        self.fname=fname
        self.header=[]
        self.points=[]

    def loadFile(self):
        """loadFile()
           This is very dumb at the moment.  It simply reads the
           file from disk assuming its a proper .csv file and stores
           it internally without error checking.
        """

        fid=open(self.fname,'r')
        self.header=fid.readline().split(',')

        for line in self.lines:
            self.points.append(line.split(','))

        fid.close()

    def createMesh(self):
        """createMesh()
           For now, assumes a proper set of points has been loaded
           and generates the mesh from the first three columns.
        """
        mesh=bpy.data.meshes.new('PointCloud')
        for p in self.points

    def destroyMesh(self,n):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set()



mesh=bpy.data.meshes.new('PointCloud')
object=bpy.data.objects.new('PointCloud',mesh)


pt=[]
nVal=[]
colDict={}

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

def readMesh(filename, objName):
    pass

def addMeshObject(mesh, objName):
    scene = bpy.context.scene
    for object in scene.objects:
        object.select = False

    mesh.update()
    mesh.validate()

    nobj = bpy.data.objects.new(objName, mesh)
    scene.objects.link(nobj)
    nobj.select = True

    if scene.objects.active is None or scene.objects.active.mode == 'OBJECT':
        scene.objects.active = nobj


def read(filepath):
    objName = bpy.path.display_name_from_filepath(filepath)
    mesh = readMesh(filepath, objName)
    addMeshObj(mesh, objName)
