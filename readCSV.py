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
        self.headCols={}

        fid=open(self.fname,'r')
        self.header=[v.strip() for v in fid.readline().split(',')]

        for line in fid.readlines():
            self.points.append([float(v.strip()) for v in line.split(',')])

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
            x=p[0]
            y=p[1]
            z=p[2]

            xyz=(x,y,z)
            #bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,size=0.07,location=xyz)
            #bpy.ops.mesh.primitive_ico_sphere_add(size=0.07,location=xyz)
            bpy.ops.mesh.primitive_cube_add(location=xyz,radius=0.07)
        bpy.ops.object.mode_set()
        #
        mesh.update()

        for col,h in enumerate(self.header):
            mesh.vertex_colors.new(h)
            self.headCols[h]=col
            
        numItems=len(self.points)
        for key in mesh.vertex_colors.keys():
            numVertsPerItem=int(len(mesh.vertex_colors[key].data)/numItems)
            for i in range(numItems):
                n=self.points[i][self.headCols[key]]
                for j in range(numVertsPerItem):
                    data=mesh.vertex_colors[key].data[j+i*numVertsPerItem]
                    data.color[0]=n
                    data.color[1]=n
                    data.color[2]=n

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
