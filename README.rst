Requirements:
============================================================

* Torchlight 2 Game and GUTS Editor
* Unpacked game archives 
* OGRE Command Line Tools (Version >= 1.70) `[Windows Download]`_

Install
============================================================

Download the addon as `zip`_ file rename it to ``io_scene_tl2``.
Start Blender, go to User Preferences (``Ctrl Alt U``), choose the Addons Tab 
and press the button at the bottom labeled *Install from File*, choose the downloaded zip file, and confirm.

Search for Torchlight 2 Importer, open the panel and set the addon preferences:

``Torchlight Media Directory``:
	Root Directory of your unpacked game archives typically named MEDIA
``OGRE XML Converter``:
	Location of OgreXMLConverter.exe
``XML Output Directory``:
	Converted XML Files will be saved in this directory
``Use Command Line Arguments``:
	Leave this checked, if you are using the linked OGRE Command Line Tools from above
``Command Line Arguments``:
	Arguments for mesh export. Depend on the version of your OgreXMLConverter.exe (default 1.72)

Usage
============================================================

Import
------

In the 3D View click on the Torchlight 2 Tab Header.
Press the *Import Mesh* Button, in the fileselector dialog choose
the path of a *.MESH* file, and confirm. The path of the corresponding
*.SKELETON* and *.MATERIAL* files will be guessed (same directory),
if you leave these fields empty.

Afterwards select the imported Armature and press the *Import Animation* button
to select a *.SKELETON* file of an animation.	

Export
------

First save your blend file. The mesh will be triangulated and some vertices need to be splitted.

For a mesh without an armature select the object and press the *Export Weapon Mesh* button,
type a name for the *.MESH* file in the fileselector and confirm.

To export a mesh with an armature, select the mesh object and press *Export Monster Mesh*.
type a name for the *.MESH* file at the top of the screen. Further enter the name of the .skeleton file
in the text box labeled ``skeletonlink`` and confirm.

Next select the armature object, press *Export Animation* and tick the checkbox *Bind Pose* at the left,
type the name of your *.MESH* file with the extension replaced by *.SKELETON* and confirm.

To export an animation, select the armature object, press *Export Animation*, 
leave the checkbox *Bind Pose* unchecked, type a name for the *.SKELETON* file and confirm.

For wardrobe characters (multiple materials) use *Export Wardrobe Mesh* instead of *Export Monster Mesh* 
and follow the steps above.

Afterwards revert your blend file.

Also have a look at the GUTS documenation for `export conventions`_

Attaching a Weapon to a Character
---------------------------------

Given you already imported a weapon and character, create an empty object (``Shift + A``)
go to the Properties Panel, choose the constraints tab and add a *Copy Transform*. 
As target object choose the character armature and as target bone a tag bone.

Now parent the weapon to the empty and rotate it 90 degrees around its local Z-axis. (Transform Panel)

Notes
============================================================

* All imported objects are rotated 90 degrees around their X-axis. If you create your own models, skeletons,
  you should rotate these too. (You might use an rotated empty as parent object)

* Some wardrobe meshes do not work properly with their skeleton files in the same directory.
  Choose the ``HUM_M.SKELETON`` / ``HUM_F.SKELETON`` from ``MEDIA/MODELS/PCS/HUM_*`` instead. You can set 
  the path quickly by using the Set Skeleton Path Button

* Some wardrobe meshes refer to ``null01.dds`` in their corresponding *.MATERIAL* file. By pressing 
  the *Assign Wardrobe Textures* and choosing the directory you imported the wardrobe mesh from,
  the operator tries to assign the missing texture by name guessing.
  Further the *Assign Body Textures* operator will assign body textures to blank mesh parts. 

* Blender does not support custom vertex normals, so these are not preserved

.. _[Windows Download]: https://sourceforge.net/projects/ogre/files/ogre-tools/1.7.2/OgreCommandLineTools_1.7.2.zip/download
.. _zip: https://github.com/pink-vertex/blender_addon_torchlight2/archive/Release.zip
.. _export conventions: http://docs.runicgames.com/wiki/Exporting_an_Animation
