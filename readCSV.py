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

class PointCloud():
    def __init__(self,fname):
        self.fname=fname
        self.header=[]
        self.points=[]
        self.headCols={}

    def loadPoints(self,fname=None):
        """loadPoints(fname=None)
           This is very dumb at the moment.  It simply reads the
           file from disk assuming its a proper .csv file and stores
           it internally without error checking.

           If fname is None and self.fname is none, returns False
           If fname is set, then assigns new filepath to self.fname
        """

        if fname: self.fname=fname
        if not self.fname: return False
        self.headCols={}

        fid=open(self.fname,'r')
        self.header=[v.strip() for v in fid.readline().split(',')]

        for line in fid.readlines():
            self.points.append(line.split(','))

        fid.close()

    def createMesh(self,objName):
        """createMesh()
           For now, assumes a proper set of points has been loaded
           and generates the mesh from the first three columns.
        """

        scene = bpy.context.scene
        for object in scene.objects:
            object.select = False


        mesh=bpy.data.meshes.new(objName)
        object = bpy.data.objects.new(objName, mesh)
        scene.objects.link(object)
        object.select = True

        if scene.objects.active is None or scene.objects.active.mode == 'OBJECT':
            scene.objects.active = object

        bpy.ops.object.mode_set(mode='EDIT')
        for p in self.points:
            x=float(p[0])
            y=float(p[1])
            z=float(p[2])

            xyz=(x,y,z)
            #bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,size=0.07,location=xyz)
            #bpy.ops.mesh.primitive_ico_sphere_add(size=0.07,location=xyz)
            bpy.ops.mesh.primitive_cube_add(location=xyz,radius=0.07)
        bpy.ops.object.mode_set()
        #
        mesh.update()
        mesh.validate()

        for col,h in enumerate(self.header):
            self.headCols[h]=(col,mesh.vertex_colors.new(h))

        #for i in range(len(vertCount)):
        #    for k in self.headCols:
        #        col,h = self.headCols[k]
        #        print(dir(h.data))
        #        print(dir(h.data.keys()))
        #        nn=float(p[col])
        #        d=h.data[i]
        #        d.color[0]=nn
        #        d.color[1]=nn
        #        d.color[2]=nn

        return (object,mesh)
            

    def destroyMesh(self,n):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set()





def read(directory,filepath):
    objName = bpy.path.display_name_from_filepath(filepath)
    pc=PointCloud(filepath)
    pc.loadPoints()  # TODO: Add some error checking
    object,mesh=pc.createMesh(objName)
