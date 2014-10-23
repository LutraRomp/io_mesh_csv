Blender CSV Point Cloud Importer
================================

Version 0.1

Overview
--------

This addon adds a .csv reader to blender which loads the file as a Point Cloud.

Future Direction
----------------

This code as well as documentation is currently very lacking.  I will fill in more here
when I get the time.

Issues
------

Due to the fact that the point cloud is being loaded as mesh objects (ico sphere at the moment),
this code will not find much use for points numbering more than 1000 or so as Blender takes too long
to generate the meshes.

I don't know how much of this is my personal implementation and how much is the fact that I'm trying
to do something that wasn't originally intended.
