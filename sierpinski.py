import bpy

# create mesh & object
mesh = bpy.data.meshes.new(name="Sierpinsky.Mesh")
obj = bpy.data.objects.new("Sierpinsky", mesh)

# add obj to the scene
scene = bpy.context.scene
scene.objects.link(obj)
scene.objects.active = obj
obj.select = True

# base corners of tetrahedron
OFFSETS = [(0.0, 0.5, 0.0),
           (0.707106781186547, -0.5, 0.0),
           (-0.353553389127747, -0.5, -0.612372436541917),
           (-0.353553393524327, -0.5, 0.61237243400355)]

# add to 3-tuples
def vadd(v0, v1):
    return (v0[0] + v1[0], v0[1] + v1[1], v0[2] + v1[2])

# multiply a scalar by a 3-tuple
def vmul(scalar, v):
    return (scalar * v[0], scalar * v[1], scalar * v[2])

# return the vertices for a tetrahedron
def make_tet(center, height):
    v = [vadd(vmul(height, x), center) for x in OFFSETS]
    return [v[0], v[1], v[2],
            v[0], v[2], v[3],
            v[0], v[3], v[1],
            v[3], v[2], v[1]]

# turn a list of lists into a single flat list
def flatten(list):
    return [item for sublist in list for item in sublist]

# make a sierpenski sponge at center with the specified height and sub-division level
def make_sponge(center, height, subdivs):
    if subdivs == 0:
        return make_tet(center, height)
    else:
        return flatten([make_sponge(vadd(vmul(height / 2.0, x), center), height / 2.0, subdivs - 1) for x in OFFSETS])

center = (0.0, 0.0, 0.0)
height = 1.0
verts = make_sponge(center, height, 0)
faces = [(i, i + 1, i + 2) for i in range(0, len(verts), 3)]

mesh.from_pydata(verts, [], faces)

