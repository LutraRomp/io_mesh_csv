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

        fid=open(self.fname,'r')
        self.header=[v.strip() for v in fid.readline().split(',')]

        self.headCols={}
        for col,h in enumerate(self.header):
            self.headCols[h]=col

        self.points=[]
        for line in fid.readlines():
            self.points.append([float(v.strip()) for v in line.split(',')])

        fid.close()


class MeshGenerator():
    def __init__(self,pointCloud):
        self.pointCloud=pointCloud

    def createMesh(self,objName):
        """createMesh()
           For now, assumes a proper set of points has been loaded
           and generates the mesh from the first three columns.
        """

        self.scene = bpy.context.scene
        for object in self.scene.objects:
            object.select = False

        self.mesh=bpy.data.meshes.new(objName)
        self.object = bpy.data.objects.new(objName, self.mesh)
        self.scene.objects.link(self.object)
        self.object.select = True

        for h in self.pointCloud.header:
            self.mesh.vertex_colors.new(h)

        if self.scene.objects.active is None or self.scene.objects.active.mode == 'OBJECT':
            self.scene.objects.active = self.object

    def populateMesh(self):
        for object in self.scene.objects:
            object.select = False
        self.object.select = True
        self.scene.objects.active = self.object

        bpy.ops.object.mode_set(mode='EDIT')

        for p in self.pointCloud.points:
            xyz=(p[0],p[1],p[2])
            #bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,size=0.07,location=xyz)
            #bpy.ops.mesh.primitive_ico_sphere_add(size=0.07,location=xyz)
            bpy.ops.mesh.primitive_cube_add(location=xyz,radius=0.07)

        bpy.ops.object.mode_set()
        self.mesh.update()

        numItems=len(self.pointCloud.points)
        for key in self.mesh.vertex_colors.keys():
            numVertsPerItem=int(len(self.mesh.vertex_colors[key].data)/numItems)
            for i in range(numItems):
                n=self.pointCloud.points[i][self.pointCloud.headCols[key]]
                for j in range(numVertsPerItem):
                    data=self.mesh.vertex_colors[key].data[j+i*numVertsPerItem]
                    data.color[0]=n
                    data.color[1]=n
                    data.color[2]=n

    def destroyMesh(self):
        for object in self.scene.objects:
            object.select = False
        self.object.select = True
        self.scene.objects.active = self.object

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set()


def read(directory,filepath):
    objName = bpy.path.display_name_from_filepath(filepath)

    pCloud=PointCloud(filepath)
    pCloud.loadPoints()

    meshGen=MeshGenerator(pCloud)
    meshGen.createMesh(objName)
    meshGen.populateMesh()
