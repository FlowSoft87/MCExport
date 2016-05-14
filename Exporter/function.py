import math
import bpy

def getRoundedInt(number):
    """
    Round up if number > 0.5 and down else.
    
    Returns:
        The number rounded to the nearest integer value.
    """
    
    return int(number+0.499)

def getLocation(obj):
    """
    Convenience method to grab the location from a bpy_types.Object
    (mesh or other kind of blender objects).
    
    Args:
        obj: (bpy_types.Object) Blender object.
    
    Returns:
        Three floats representing x, y and z coordinate of the
        object (in this order).
    """
    
    lx = obj.location[0]
    ly = obj.location[1]
    lz = obj.location[2]
    return lx, ly, lz

def getRotation(obj):
    """
    Convenience method to extract the rotation around x, y
    and z axes. Important: order matters since rotations do
    not commute!
    
    Args:
        obj: (bpy_types.Object) Blender object.
    
    Returns:
        Three floats representing the rotations around x, y and z axes.
    """
    
    rx = obj.rotation_euler[0]#*(180./math.pi)
    ry = obj.rotation_euler[1]#*(180./math.pi)
    rz = obj.rotation_euler[2]#*(180./math.pi)
    rmode = obj.rotation_mode
    return rx, ry, rz, rmode

def getScale(obj):
    """
    Convenience method to extract the scale of an object in x, y
    and z directions.
    
    Args:
        obj: (bpy_types.Object) Blender object.
    
    Returns:
        Three floats representing the scale in x, y and z directions.
    """
    
    sx = obj.scale[0]
    sy = obj.scale[1]
    sz = obj.scale[2]
    return sx, sy, sz

def getDimensions(obj):
    """
    Convenience method to extract the dimensions of an object in x, y
    and z directions.
    For the standard cube model added by this addon it is two times
    the scale.
    
    Args:
        obj: (bpy_types.Object) Blender object.
    
    Returns:
        Three floats representing the dimensions in x, y and z directions.
    """
    
    dx = int(obj.dimensions[0]+0.499)
    dy = int(obj.dimensions[1]+0.499)
    dz = int(obj.dimensions[2]+0.499)
    return dx, dy, dz

def getMinVertex(obj):
    """
    Method that finds the minimum vertex in a model.
    This is the one that has smallest x, y and z values.
    
    Args:
        obj: (bpy_types.Object) Blender mesh-object.
    
    Returns:
        Three floats representing the minimum vertex coordinates.
    """
    
    mesh = obj.data
    vertex_list = mesh.vertices
    vx_min = None
    vy_min = None
    vz_min = None
    for vert in vertex_list:
        if(vx_min == None or vert.co.x < vx_min):
            vx_min = vert.co.x
        if(vy_min == None or vert.co.y < vy_min):
            vy_min = vert.co.y
        if(vz_min == None or vert.co.z > vz_min):
            vz_min = vert.co.z
    return vx_min, vy_min, vz_min

def getMinUV(obj):
    """
    Find the minimum uv coordinates for a mesh.
    Minecraft uses this as the texture offset.
    Note: The v coordinate is projected onto 1-v.
    
    Args:
        obj: (bpy_types.Object) Blender mesh-object.

    Returns:
        Two floats representing the u and v
        coordinates with the smallest values
        for a given mesh or 0,0 if the mesh has no
        active texture assigned.
    """
    
    mesh = obj.data
    u_min = 1.
    v_max = 0.
    # Check if the active texture is not none.
    if(mesh.uv_layers.active != None):
        for uv in mesh.uv_layers.active.data:
            if(uv.uv[0] < u_min):
                u_min = uv.uv[0]
            if(uv.uv[1] > v_max):
                v_max = uv.uv[1]
        return u_min, 1-v_max
    else:
        return 0., 0.

def getTextureSize(which):
    """
    Get the size of the texture at position <which> in pixels.
    
    Returns:
        Two integers representing the width and height of the texture
        at position <which> or 0,0 if it does not exist.
    """
    
    if(len(bpy.data.images) > which):
        return bpy.data.images[which].size[0], bpy.data.images[which].size[1]
    else:
        return 0, 0

def writeObjects(file):
    """
    Write the current mesh to a '.java' file which can be used
    in Minecraft directly to render the model.
    Minecraft uses a ModelRenderer object to hold the necessary
    information to render a mesh consisting of cubes. At construction,
    the texture offset is provided which is used to determine the
    uv-coordinates of the mesh in-game.
    An arbitrary amount of cubes can be added to the ModelRenderer
    object, however, they are always rotated together as only
    the ModelRenderer has a rotation point (position of the mesh).
    Because of that, this function does construct one ModelRenderer
    object for every cube mesh individually.
    Minecraft cube objects have the following properties:
    - Offset of the cube's minimum vertex from the rotation
      point.
    - Dimensions of the cube.
    
    Args:
        file: An open stream object.
    """
    
    file.write('package net.x.package;\n\n'\
        +'import net.minecraft.client.model.ModelBase;\n'\
        +'import net.minecraft.client.model.ModelRenderer;\n'\
        +'import net.minecraft.entity.Entity;\n'\
        +'import net.minecraftforge.fml.relauncher.Side;\n'\
        +'import net.minecraftforge.fml.relauncher.SideOnly;\n\n'\
        +'@SideOnly(Side.CLIENT)\n'\
        +'class ModelName extends ModelBase\n'\
        +'{\n'\
        +'    private float partialTicks;\n')
    
    for obj in bpy.data.objects:
        if(obj.type == "MESH"):
            file.write('    public ModelRenderer '+obj.name+';\n')
    
    tsu, tsv = getTextureSize(0)
    
    file.write('\n'\
            +'    public ModelName()\n'\
            +'    {\n'\
            +'        this.textureWidth = '+str(tsu)+';\n'\
            +'        this.textureHeight = '+str(tsv)+';\n')
    
    for obj in bpy.data.objects:
        if(obj.type == "MESH"):
            lx, ly, lz = getLocation(obj)
            rx, ry, rz, rmode = getRotation(obj)
            sx, sy, sz = getScale(obj)
            dx, dy, dz = getDimensions(obj)
            vx_min, vy_min, vz_min = getMinVertex(obj)
            u_min, v_min = getMinUV(obj)
            
            #file.write('        // '+obj.name+'\n')
            #file.write('        //  scale (MC): '+str(sx)+' '+str(sz)+' '+str(sy)+'\n')
            #file.write('        //  dimensions (MC): '+str(dx)+' '+str(dz)+' '+str(dy)+'\n')
            #file.write('        //  location (MC): '+str(lx)+' '+str(24-lz)+' '+str(ly)+'\n')
            #file.write('        //  local min vertex (MC): '+str(vx_min*sx)+' '+str(-vz_min*sz)+' '+str(vy_min*sy)+'\n')
            #file.write("        //  tex offset (MC): "+str(u_min)+' '+str(v_min)+'\n')
            file.write('        this.'+obj.name+' = new ModelRenderer(this,'+str(int(u_min*tsu+0.5))+','+str(int(v_min*tsv+0.5))+');\n'\
                    +'        this.'+obj.name+'.addBox('+str.format("{0:.6f}",vx_min*sx)+'f,'+str.format("{0:.6f}",-vz_min*sz)+'f,'+str.format("{0:.6f}",vy_min*sy)+'f,'+str(dx)+','+str(dz)+','+str(dy)+',0f);\n'\
                    +'        this.'+obj.name+'.setRotationPoint('+str.format("{0:.6f}",lx)+'f,'+str.format("{0:.6f}",24.-lz)+'f,'+str.format("{0:.6f}",ly)+'f);\n'\
                    +'        this.'+obj.name+'.rotateAngleX = '+str.format("{0:.6f}",rx)+'f;\n'\
                    +'        this.'+obj.name+'.rotateAngleY = '+str.format("{0:.6f}",-rz)+'f;\n'\
                    +'        this.'+obj.name+'.rotateAngleZ = '+str.format("{0:.6f}",ry)+'f;\n'\
#                    +'        this.'+obj.name+'.setTextureSize('+str(tsu)+','+str(tsv)+');\n'\
                    +'        this.'+obj.name+'.mirror = true;\n')
    
    file.write('    }\n\n'\
            +'    public void setLivingAnimations(EntityLivingBase p_78086_1_, float p_78086_2_, float p_78086_3_, float p_78086_4_)\n'\
            +'    {\n'\
            +'        this.partialTicks = p_78086_4_;\n'\
            +'    }\n\n'\
            +'    public void render(Entity p_78088_1_, float p_78088_2_, float p_78088_3_, float p_78088_4_, float p_78088_5_, float p_78088_6_, float p_78088_7_)\n'\
            +'    {\n'\
            +'        this.setRotationAngles(p_78088_2_, p_78088_3_, p_78088_4_, p_78088_5_, p_78088_6_, p_78088_7_, p_78088_1_);\n')
    for obj in bpy.data.objects:
        if(obj.type == "MESH"):
            file.write('        this.'+obj.name+'.render(p_78088_7_);\n')
    file.write('    }\n\n'\
            +'    public void setRotationAngles(float p_78087_1_, float p_78087_2_, float p_78087_3_, float p_78087_4_, float p_78087_5_, float p_78087_6_, Entity p_78087_7_)\n'\
            +'    {\n'\
            +'    }\n'\
            +'}\n')

def writeData(context, filepath):
    """
    Write the current mesh to file.
    
    Args:
        context: The current blender context.
        filepath: String containing the path to the out-file.
    """
    
    if(bpy.context.active_object.mode != "OBJECT"):
        bpy.ops.object.mode_set(mode='OBJECT')
    out = open(filepath, "w")
    writeObjects(out)
    out.close()
    
    return {'FINISHED'}

