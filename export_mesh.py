from .utils import os, bpy, get_addon_pref

CMD_EXPORT = "{converter:s} -l 0 -e -r {input:s} {output:s}"
SHARED_GEOMETRY = "<sharedgeometry vertexcount=\"{vertexcount:d}\">"

VB_POSITION = "positions=\"{positions:s}\" "
VB_NORMAL	= "normals=\"{normals:s}\" "
VB_TEXDIM	= "texture_coord_dimensions_0=\"{tex_dim:d}\" " 
VB_TEXCO	= "texture_coords=\"{tex_co:d}\""
VERTEX_BUFFER = "".join(("<vertexbuffer ", VB_POSITION, VB_NORMAL, VB_TEXDIM, VB_TEXCO, ">")) 

POSITION = "<position x=\"{x:g}\" y=\"{y:g}\" z=\"{z:g}\" />"
NORMAL   =   "<normal x=\"{x:g}\" y=\"{y:g}\" z=\"{z:g}\" />"
TEXCOORD = "<texcoord u=\"{u:g}\" v=\"{v:g}\" />"

SUBMESH = ("<submesh "
	         "material=\"{material:s}\" "
	"usesharedvertices=\"{shared_vertices:s}\" "
	  "use32bitindexes=\"{use_32bit:s}\" "
	    "operationtype=\"{op_type:s}\">")

GEOMETRY = "<geometry vertexcount=\"{vertexcount:d}\">"
FACES = "<faces count=\"{facecount:d}\">"
FACE  = "<face v1=\"{v1:d}\" v2=\"{v2:d}\" v3=\"{v3:d}\" />"

BONE_ASSIGNMENT = ("<vertexboneassignment "
	"vertexindex=\"{vertexindex:d}\" "
	  "boneindex=\"{boneindex:d}\" "
	     "weight=\"{weight:g}\" />")

SKELETONLINK = "<skeletonlink name=\"{name:s}\" />"

class XMLWriter:
	def __init__(self, file_object):
		self.file_object = file_object
		self.indent_level = 0

	def finish(self):
		self.file_object.close()

	def tag_format(self, fmt, is_empty=True, **kwargs):
		self.file_object.write(4*self.indent_level*" " + fmt.format(**kwargs) + "\n")
		if not is_empty: self.indent_level += 1

	def tag_compose(self, tag_name, attributes):
		composed = " ".join(attributes)
		self.file_object.write(4*self.indent_level*" " + composed + " >\n")

	def tag_open(self, tag_name):
		self.file_object.write(4*self.indent_level*" " + "<%s>\n" % tag_name)
		self.indent_level +=1

	def tag_close(self, tag_name):
		self.indent_level -= 1
		self.file_object.write(4*self.indent_level*" " + "</%s>\n" % tag_name)


def convert_to_mesh(xml_input, mesh_output, create_directory=False):
    if not os.path.exists(xml_input):
        raise FileNotFoundError(xml_input)

    mesh_directory = os.path.dirname(xml_input)
    if not os.path.exists(mesh_directory):
        if create_directory:
            os.makedirs(mesh_directory)
        else:
            raise FileNotFoundError(os.path.dirname(mesh_directory))
    
    ogre_xml_converter = get_addon_pref(bpy.context).ogre_xml_converter
    os.system(CMD_EXPORT.format(
        converter=ogre_xml_converter,
        input=xml_input,
        output=mesh_output
        )) 

def write_vertex_buffer(mesh, vertex_indices, flags, xml):
	(data_position,
	 data_normal,
	 #...
	 data_uv) = flags 

	xml.tag_format(VERTEX_BUFFER, False,
		positions = "true" if data_position else "false",
		normals   = "true" if data_normal   else "false",
		tex_co    =      1 if data_uv       else       0,
		tex_dim   =      2
	)

	if data_uv:
		uv_layer = mesh.uv_layers[0].data
		uv_loops = [None] * len(mesh.vertices)
		for loop in mesh.loops:
			uv_loops[loop.vertex_index] = uv_layer[loop.index]

	for index in vertex_indices:
		v = mesh.vertices[index]
		if data_uv:
			uv_loop = uv_loops[index]
			uv = uv_loop.uv.copy()
			uv.y = 1.0 - uv.y
		
		write_vertex(
			v.undeformed_co if data_position else None,
			v.normal        if data_normal   else None, 
			uv              if data_uv       else None,
			xml
		)

	xml.tag_close("vertexbuffer")

def write_vertex(co, n, uv, xml):
	xml.tag_open("vertex")
	if co: xml.tag_format(POSITION, x=co.x, y=co.y, z=co.z)
	if  n: xml.tag_format(NORMAL,   x= n.x, y= n.y, z= n.z)
	if uv: xml.tag_format(TEXCOORD, u=uv.x, v=uv.y)
	xml.tag_close("vertex")

# =============================================================================
# -----------------------------------WEAPON------------------------------------
# =============================================================================

def write_mesh_weapon(mesh, xml_stream):
	xml = XMLWriter(xml_stream)

	xml.tag_open("mesh")
	write_shared_geometry(mesh, xml)
	
	xml.tag_open("submeshes")
	write_submesh_weapon(mesh, xml)
	xml.tag_close("submeshes")

	xml.tag_close("mesh")
	xml.finish()

def write_submesh_weapon(mesh, xml):
	xml.tag_format(SUBMESH, False,
		material=mesh.materials[0].name,
		shared_vertices="true",
		use_32bit="false",
		op_type="triangle_list"
	)

	xml.tag_format(FACES, False, facecount=len(mesh.polygons))
	for poly in mesh.polygons:
		indices = poly.vertices
		if not len(indices) == 3:
			raise ValueError("Polygon is not a triangle")
		xml.tag_format(FACE, v1=indices[0], v2=indices[1], v3=indices[2])

	xml.tag_close("faces")
	xml.tag_close("submesh")

def write_shared_geometry(mesh, xml):
	xml.tag_format(SHARED_GEOMETRY, False, vertexcount=len(mesh.vertices))
	write_vertex_buffer(mesh, range(len(mesh.vertices)), (True, True, True), xml)
	xml.tag_close("sharedgeometry")

# =============================================================================
# ---------------------------------WARDROBE------------------------------------
# =============================================================================

def write_mesh_wardrobe(mesh, bones, skel_link, xml_stream):
	xml = XMLWriter(xml_stream)
	xml.tag_open("mesh")
	xml.tag_open("submeshes")

	offset = 0
	for mat_index in range(len(mesh.materials)):
		offset += write_submesh_wardrobe(mesh, bones, mat_index, offset, xml)

	xml.tag_close("submeshes")
	xml.tag_format(SKELETONLINK.format(name=skel_link))
	xml.tag_close("mesh")
	xml.finish()

def write_submesh_wardrobe(mesh, bones, mat_index, offset, xml):
	xml.tag_format(SUBMESH, False,
		material = mesh.materials[mat_index].name,
		shared_vertices="false",
		use_32bit="false",
		op_type="triangle_list"
	)

	polys = [poly for poly in mesh.polygons if poly.material_index == mat_index]
	vertex_indices = {i for poly in polys for i in poly.vertices}
	vertex_indices = list(vertex_indices)
	vertex_indices.sort()

	xml.tag_format(FACES, False, facecount=len(polys))
	for poly in polys:
		indices = [i - offset for i in poly.vertices]
		xml.tag_format(FACE, v1=indices[0], v2=indices[1], v3=indices[2])
	xml.tag_close("faces")

	xml.tag_format(GEOMETRY, False, vertexcount=len(vertex_indices))
	write_vertex_buffer(mesh, vertex_indices, (True,  True,  False), xml)
	write_vertex_buffer(mesh, vertex_indices, (False, False, True ), xml)
	xml.tag_close("geometry")

	xml.tag_open("boneassignments")
	for index in vertex_indices:
		v = mesh.vertices[index]
		for g in v.groups:
			if g.group in bones:
				xml.tag_format(BONE_ASSIGNMENT, 
					vertexindex=index - offset,
					boneindex=g.group,
					weight=g.weight
				) 		
	xml.tag_close("boneassignments")

	xml.tag_close("submesh")
	return len(vertex_indices)
