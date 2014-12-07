Blender CSV Point Cloud Importer
================================

Version 0.4.2

Description
-----------

This addon adds a .csv reader to blender which loads a .csv file with a header line as a Point Cloud.

This point cloud can be loaded as vertices (aka Points), Cubes, Ico Spheres (subdivide=1), or
Ico Spheres (subdivide=2.)

Motivation
----------

The impetus behind this plugin rests in the author's frequent need to load point cloud information
into Blender for scientific visualization.  It is hopeful that such a tool may find broader use
in the community.

Usage
-----

To install, follow the usual procedure of placing the 'io_mesh_csv/' folder into Blender's
'scripts/addons' folder and enable the 'Import-Export: CSV PointCloud reader (.csv)' in the
User Preferences window (Ctrl-Alt-U).

Once the addon is enabled, load a point cloud by navigating to 'File -> Import -> CSV Files (.csv)'.
Select a '.csv' file in the open menu.

In the file open dialog box, you can change the names chosen for the X, Y and Z columns.  Leaving
any column names blank will default the points to 0.0 in that dimension.  Thus, if the 'Y' column
is blanked out, then the loaded point cloud will consist of a 2 dimensional plane at Y=0.0.  A 2-D
and 1-D point cloud can be loaded in this manner.

Additionally, the delimiter and type of point cloud (Points, Cubes, Ico Spheres) can also be
selected in the open dialog box.  There is currently no way to load a tab (\t) delimited file.

Regarding the size of point cloud, Blender is able to handle large (+1million) numbers of
Points (aka, vertices).  However, Blender is not able to handle as many ico spheres or cubes.

The advantage of the ico spheres and cubes are that they contain UV information for every column
in the source .csv file, which can then be used to color the objects.

To render the point cloud when using Points, either dupliverts or Blender Internal's halos
will have to be used.

Issues
------

When the point cloud is being loaded as mesh objects (Cubes and Ico Spheres), 
points numbering more than 1000 or so take a very long time to generate.

I am currently unaware of any way to assign color information to points loaded as 'Points' when
visualizing as Halos or using Dupliverts.

There currently is no way to load point clouds delimited by tabs (\t).  This will be fixed shortly.

There is currently no way to load a headerless .csv file.
