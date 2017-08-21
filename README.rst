Requirements:
============================================================

* Torchlight 2 Game and TL2Editor
* Unpacked game archives 
* OGRE Command Line Tools (Version => 1.70)

Install
============================================================

	Download the addon as zip file rename it to "io_scene_tl2"
	and install it via Blender->User Preferences->Addons->Install from File.
	
	Search for Torchlight 2 Importer, open the panel and set the addon preferences:

	* Torchlight Media Directory: Root Directory of your unpacked game archives typically name MEDIA
	* OGRE XML Converter: Location of OgreXMLConverter.exe
	* XML Output Directory: Converted XML Files will be saved in this directory

Usage
============================================================
	In the 3D View click on the Torchlight 2 Tab Header.
	Press the ImportMesh Button, in the fileselector dialog choose
	the path of a .MESH file, and confirm. The path of the corresponding
	.SKELETON and .MATERIAL files will be guessed, if you leave the fields
	empty.

	Afterwards select the imported Armature and press the Import Animation button
	to select a .SKELETON file of an animation.	

Notes
============================================================
	* Some WARDROBE meshes do not work properly with their SKELETON files in the same directory.
	  Choose the HUM_M.SKELETON / HUM_F.SKELETON from MEDIA/MODELS/PCS/HUM_* instead. You can set 
	  the path quickly by using the Set Skeleton Path Button
