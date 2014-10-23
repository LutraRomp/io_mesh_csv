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

        fid=open(self.fname,'r')
        self.header=fid.readline().split(',')

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

        #mesh.update()
        #mesh.validate()
        #
        if scene.objects.active is None or scene.objects.active.mode == 'OBJECT':
            scene.objects.active = object

        Col=mesh.vertex_colors.new()

        oldLen=0
        for p in self.points:
            x=float(p[0])
            y=float(p[1])
            z=float(p[2])
            n=float(p[3])
            # for now, column 'n' is 'Col'.  This will change in the future

            xyz=(x,y,z)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,size=0.07,location=xyz)
            #bpy.ops.mesh.primitive_ico_sphere_add(size=0.07,location=xyz)
            #bpy.ops.mesh.primitive_cube_add(location=xyz,radius=0.07)
            bpy.ops.object.mode_set()
            nn = rangeSet(n, 0.0, 1.0)
            newLen=len(Col.data)
            for i in range(oldLen,newLen):
                mesh.vertex_colors['Col'].data[i].color[0]=nn
                mesh.vertex_colors['Col'].data[i].color[1]=nn
                mesh.vertex_colors['Col'].data[i].color[2]=nn
        
            oldLen=newLen


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
