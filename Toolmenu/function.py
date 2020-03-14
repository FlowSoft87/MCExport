import bmesh


def set_uv(obj, imagesize):
    mesh = obj.data
    bm = bmesh.from_edit_mesh(mesh)
    
    uv_layer = bm.loops.layers.uv.verify()
    # bm.faces.layers.tex.verify()  # currently blender needs both layers.
    
    dx_u = obj.dimensions[0]/float(imagesize[0])
    dy_u = obj.dimensions[1]/float(imagesize[0])
    dy_v = obj.dimensions[1]/float(imagesize[1])
    dz_v = obj.dimensions[2]/float(imagesize[1])
    offset_u = 0.
    offset_v = 1.
    right_offset = 0.
    down_offset = 0.
    
    # adjust UVs
    for f in bm.faces:
        index = f.index
        if index == 0:
            offset_u = dy_u+dx_u
            offset_v = 1.
            right_offset = dx_u
            down_offset = dy_v
        elif index == 1:
            offset_u = dy_u
            offset_v = 1.
            right_offset = dx_u
            down_offset = dy_v
        elif index == 2:
            offset_u = dy_u+dx_u
            offset_v = 1.-dy_v
            right_offset = dy_u
            down_offset = dz_v
        elif index == 3:
            offset_u = dy_u
            offset_v = 1.-dy_v
            right_offset = dx_u
            down_offset = dz_v
        elif index == 4:
            offset_u = 0.
            offset_v = 1.-dy_v
            right_offset = dy_u
            down_offset = dz_v
        else:
            offset_u = 2*dy_u+dx_u
            offset_v = 1.-dy_v
            right_offset = dx_u
            down_offset = dz_v
        n = 0
        for l in f.loops:
            luv = l[uv_layer]
            # apply the location of the vertex as a UV
            if index == 5:
                if n == 0:
                    luv.uv[0] = offset_u
                    luv.uv[1] = offset_v
                elif n == 1:
                    luv.uv[0] = offset_u
                    luv.uv[1] = offset_v-down_offset
                elif n == 2:
                    luv.uv[0] = offset_u+right_offset
                    luv.uv[1] = offset_v-down_offset
                elif n == 3:
                    luv.uv[0] = offset_u+right_offset
                    luv.uv[1] = offset_v
            elif index == 1:
                if n == 1:
                    luv.uv[0] = offset_u
                    luv.uv[1] = offset_v
                elif n == 2:
                    luv.uv[0] = offset_u
                    luv.uv[1] = offset_v-down_offset
                elif n == 3:
                    luv.uv[0] = offset_u+right_offset
                    luv.uv[1] = offset_v-down_offset
                elif n == 0:
                    luv.uv[0] = offset_u+right_offset
                    luv.uv[1] = offset_v
            else:
                if n == 2:
                    luv.uv[0] = offset_u
                    luv.uv[1] = offset_v
                elif n == 3:
                    luv.uv[0] = offset_u
                    luv.uv[1] = offset_v-down_offset
                elif n == 0:
                    luv.uv[0] = offset_u+right_offset
                    luv.uv[1] = offset_v-down_offset
                elif n == 1:
                    luv.uv[0] = offset_u+right_offset
                    luv.uv[1] = offset_v
            n += 1
    
    bmesh.update_edit_mesh(mesh)


def create_box(width, height, depth):
    """
    This function takes inputs and returns vertex and face arrays.
    No actual mesh data creation is done here.
    """
    
    verts = [(+1.0, +1.0, -1.0),
             (+1.0, -1.0, -1.0),
             (-1.0, -1.0, -1.0),
             (-1.0, +1.0, -1.0),
             (+1.0, +1.0, +1.0),
             (+1.0, -1.0, +1.0),
             (-1.0, -1.0, +1.0),
             (-1.0, +1.0, +1.0),
             ]
    
    faces = [(0, 1, 2, 3),
             (4, 7, 6, 5),
             (0, 4, 5, 1),
             (1, 5, 6, 2),
             (2, 6, 7, 3),
             (4, 0, 3, 7),
             ]
    
    # apply size
    for i, v in enumerate(verts):
        verts[i] = v[0] * width * 0.5, v[1] * depth * 0.5, v[2] * height * 0.5
    
    return verts, faces

