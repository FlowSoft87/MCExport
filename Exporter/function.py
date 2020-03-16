import math
import bpy


def get_rounded_int(number: float) -> int:
    """
    Round up if number > 0.5 and down else.
    
    Returns:
        The number rounded to the nearest integer value.
    """

    return int(number+0.499)


def get_location(obj: bpy.types.Object) -> (float, float, float):
    """
    Convenience method to grab the location from a bpy_types.Object
    (mesh or other kind of blender objects).
    
    Args:
        obj: (bpy_types.Object) Blender object.
    
    Returns:
        Three floats representing x, y and z coordinate of the
        object (in this order).
    """

    lx: float = obj.location[0]
    ly: float = obj.location[1]
    lz: float = obj.location[2]
    return lx, ly, lz


def get_rotation(obj: bpy.types.Object) -> (float, float, float):
    """
    Convenience method to extract the rotation around x, y
    and z axes. Important: order matters since rotations do
    not commute!
    
    Args:
        obj: (bpy_types.Object) Blender object.
    
    Returns:
        Three floats representing the rotations around x, y and z axes.
    """

    rx: float = obj.rotation_euler[0]#*(180./math.pi)
    ry: float = obj.rotation_euler[1]#*(180./math.pi)
    rz: float = obj.rotation_euler[2]#*(180./math.pi)
    # rmode = obj.rotation_mode
    return rx, ry, rz


def get_scale(obj: bpy.types.Object) -> (float, float, float):
    """
    Convenience method to extract the scale of an object in x, y
    and z directions.
    
    Args:
        obj: (bpy_types.Object) Blender object.
    
    Returns:
        Three floats representing the scale in x, y and z directions.
    """

    sx: float = obj.scale[0]
    sy: float = obj.scale[1]
    sz: float = obj.scale[2]
    return sx, sy, sz


def get_dimensions(obj: bpy.types.Object) -> (int, int, int):
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


def get_min_vertex(obj: bpy.types.Object) -> (float, float, float):
    """
    Method that finds the minimum vertex in a model.
    This is the one that has smallest x, y and z values.
    
    Args:
        obj: (bpy_types.Object) Blender mesh-object.
    
    Returns:
        Three floats representing the minimum vertex coordinates.
    """

    mesh: bpy.types.Mesh = obj.data
    vertex_list = mesh.vertices
    vx_min: float = None
    vy_min: float = None
    vz_min: float = None
    for vert in vertex_list:
        if(vx_min == None or vert.co.x < vx_min):
            vx_min = vert.co.x
        if(vy_min == None or vert.co.y < vy_min):
            vy_min = vert.co.y
        if(vz_min == None or vert.co.z > vz_min):
            vz_min = vert.co.z
    return vx_min, vy_min, vz_min


def get_min_uv(obj: bpy.types.Object) -> (float, float):
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

    mesh: bpy.types.Mesh = obj.data
    u_min = 1.
    v_max = 0.
    # Check if the active texture is not none.
    if(mesh.uv_layers.active is not None):
        for uv in mesh.uv_layers.active.data:
            if(uv.uv[0] < u_min):
                u_min = uv.uv[0]
            if(uv.uv[1] > v_max):
                v_max = uv.uv[1]
        return u_min, 1-v_max
    else:
        return 0., 0.


def get_active_texture() -> bpy.types.Image:
    active_image: bpy.types.Image = None
    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            active_image = area.spaces.active.image
    return active_image


def get_texture_size() -> (int, int):
    """
    Get the size of the texture at position <which> in pixels.
    
    Returns:
        Two integers representing the width and height of the texture
        at position <which> or 0,0 if it does not exist.
    """

    texture: bpy.types.Image = get_active_texture()
    if texture is not None:
        return texture.size[0], texture.size[1]
    else:
        return 0, 0


def get_animation_frame_range(obj_list, animation_name):
    """
    Grab the number of frames for the current animation.
    An animation always starts at frame zero.
    
    Args:
        obj_list: List of all objects in the scene.
                  (Generally: bpy.data.objects)
        animation_name: Name of the animation.
    
    Returns:
        Integer value representing the number of frames of the
        animation. If the returned value is zero the animation
        does not exist.
    """

    out_maxframe = 0
    for obj in obj_list:
        if obj.type == "MESH":
            if obj.animation_data == None:
                print("Warning: Object has no animation data set!")
                continue
            if len(obj.animation_data.nla_tracks) == 0:
                print("Warning: Object has no nla-track set!")
                continue
            for anim in obj.animation_data.nla_tracks:
                if (anim.name == animation_name) and (anim.strips[0].action_frame_end > out_maxframe):
                    out_maxframe = anim.strips[0].action_frame_end
                    break
    return out_maxframe


#def getObjectMap(obj_list):
#    """
#    Construct a map to assign index to named object.
#    """
#
#    for obj in obj_list:
#        if obj.type == "MESH":
#            


def get_animation_map(obj_list):
    """
    Construct a map, mapping the names of animations to an index and their
    max frame.
    """

    out_map = {}
    cur_index = 0
    for obj in obj_list:
        if obj.type == "MESH":
            if obj.animation_data == None:
                print("Warning: Object has no animation data set!")
                continue
            if len(obj.animation_data.nla_tracks) == 0:
                print("Warning: Object has no nla-track set!")
                continue
            for anim in obj.animation_data.nla_tracks:
                temp_name = anim.name
                if not (temp_name in out_map):
                    temp_max_frame = get_animation_frame_range(obj_list, temp_name)
                    out_map[temp_name] = (cur_index,temp_max_frame,[obj.name])
                    cur_index += 1
                else:
                    out_map[temp_name][2].append(obj.name)
    return out_map


def get_animation_data(obj, animation_name, max_frame):
    """
    Grab the animation data for translation, rotation and scale.
    Usage in blender:
        The general idea is to set the actions initially so blender does
        display the animation as you want it to be. After that, the
        'NLA Editor' is used to build tracks out of them with the name
        of the animation. For starters only one strip per track is permitted.
        If checking an option 'Export animations' it
        will always be necessary to construct an animation called 'idle'!
        RenderModel object will only check for animation and frame in
        entity if animation is exported.
    Export:
        In Minecraft an animation is simply a set of locations, rotations
        and scales (which are simple OGL operations). Since this is the
        same for all entities which have the same model, this information
        should be stored in the RenderModel object. When rendering, the
        RenderObject asks the entity for which animation it is in (this
        should be a simple integer) and what frame is the current one
        (this will be incremented with every tick). The animations will
        be stored in an array which holds arrays for x, y and z locations,
        rotations and scales (this makes a total of 9 arrays).
        The RenderModel object can now simply grab the information about
        next and current frame by selecting the animation with the
        animation integer returned by the entity and the frame by
        the integer for the current frame. In blender, every single
        frame will correspond to a Minecraft tick and Minecraft will
        (like blender) interpolate linearly between two frames.
    
    Args:
        obj: The object.
        animation_name: The name of the animation to extract.
        max_frame: The maximum frame to be extracted. Can be found
                   by calling above function.
    
    Returns:
        A list object whose index corresponds to the values
        of locations, rotations and scales at an index that corresponds
        to the frame or None if the object has no animation data.
        A char sequence indicating what type of data are stored:
            'l'-loc, 'lr'-locrot, 'lrs'-locrotscale or 'n' if none.
        The nine lists correspond to:
        0: locX
        1: locY
        2: locZ
        3: rotX
        4: rotY
        5: rotZ
        6: scaX
        7: scaY
        8: scaZ.
        
        Example:
            anims[1][10] corresponds to the 10-th frame (last index
            10) of the y-location (first index 1) of the model.
    """

    if (obj.animation_data == None) or (len(obj.animation_data.nla_tracks < 1)):
        print("Warning: No animation tracks found in object!")
        return None
    anims = obj.animation_data.nla_tracks
    out_animation = None
    out_type = 'n'
    for anim in anims:
        if(anim.name == animation_name):
            action = anim.strips[0].action
            if(len(action.fcurves) < 3):
                print("Warning: No properties captured!")
                return None
            if len(action.fcurves) == 9:
                # All properties captured.
                out_animation = [[],[],[],[],[],[],[],[],[]]
                out_type = 'lrs'
                for frame in range(max_frame):
                    out_animation[0].append(action.fcurves[0].evaluate(frame))
                    out_animation[1].append(action.fcurves[1].evaluate(frame))
                    out_animation[2].append(action.fcurves[2].evaluate(frame))
                    out_animation[3].append(action.fcurves[3].evaluate(frame))
                    out_animation[4].append(action.fcurves[4].evaluate(frame))
                    out_animation[5].append(action.fcurves[5].evaluate(frame))
                    out_animation[6].append(action.fcurves[6].evaluate(frame))
                    out_animation[7].append(action.fcurves[7].evaluate(frame))
                    out_animation[8].append(action.fcurves[8].evaluate(frame))
            elif len(action.fcurves) == 6:
                # Location and rotation.
                out_animation = [[],[],[],[],[],[]]
                out_type = 'lr'
                for frame in range(max_frame):
                    out_animation[0].append(action.fcurves[0].evaluate(frame))
                    out_animation[1].append(action.fcurves[1].evaluate(frame))
                    out_animation[2].append(action.fcurves[2].evaluate(frame))
                    out_animation[3].append(action.fcurves[3].evaluate(frame))
                    out_animation[4].append(action.fcurves[4].evaluate(frame))
                    out_animation[5].append(action.fcurves[5].evaluate(frame))
            elif len(action.fcurves) == 3:
                # Location only.
                out_animation = [[],[],[]]
                out_type = 'l'
                for frame in range(max_frame):
                    out_animation[0].append(action.fcurves[0].evaluate(frame))
                    out_animation[1].append(action.fcurves[1].evaluate(frame))
                    out_animation[2].append(action.fcurves[2].evaluate(frame))
            break
    return out_animation, out_type


class_file_template = """import net.minecraft.client.model.ModelBase;
import net.minecraft.client.model.ModelRenderer;
import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityLivingBase;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

@SideOnly(Side.CLIENT)
class Model{modelName} extends ModelBase {{

    private float partialTicks;

{boxDeclarations}

    public Model{modelName}() {{
        this.textureWidth = {texWidth};
        this.textureHeight = {texHeight};

{boxInstantiations}
    }}

    @Override
    public void setLivingAnimations(EntityLivingBase entity, float limbSwing, float limbSwingAmount,
            float partialTicks) {{
        this.partialTicks = partialTicks;
    }}

    @Override
    public void render(Entity entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, 
            float headPitch, float scale) {{
        this.setRotationAngles(limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch, scale, entity);

{boxRenderCalls}
    }}

    public void setRotationAngles(float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw,
            float headPitch, float scale, Entity entity) {{
    }}
}}
"""

box_declaration_template = """    public ModelRenderer {boxName};"""

box_instantiation_template = """        this.{boxName} = new ModelRenderer(this, {texOffsetX}, {texOffsetY});
        this.{boxName}.addBox({offsetX}, {offsetY}, {offsetZ}, {width}, {height}, {depth}, {scaleFactor});
        this.{boxName}.setRotationPoint({rotatePointX}, {rotatePointY}, {rotatePointZ});
        this.{boxName}.rotateAngleX = {rotateAngleX};
        this.{boxName}.rotateAngleY = {rotateAngleY};
        this.{boxName}.rotateAngleZ = {rotateAngleZ};
        this.{boxName}.mirror = true;
"""

box_render_template = """        this.{boxName}.render(scale);"""


def write_objects(file):
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
        animations: Boolean indicating if animations shall also be extracted.
    """

    tsu, tsv = get_texture_size()

    box_declarations: str = ""
    box_instantiations: str = ""
    box_render_calls: str = ""
    for obj in bpy.data.objects:
        if(obj.type == "MESH"):
            lx, ly, lz = get_location(obj)
            rx, ry, rz = get_rotation(obj)
            sx, sy, sz = get_scale(obj)
            dx, dy, dz = get_dimensions(obj)
            vx_min, vy_min, vz_min = get_min_vertex(obj)
            u_min, v_min = get_min_uv(obj)

            tex_off_x = str(int(u_min * tsu + 0.5))
            tex_off_y = str(int(v_min * tsv + 0.5))
            offset_x = str.format("{0:.6f}", vx_min * sx) + 'f'
            offset_y = str.format("{0:.6f}", -vz_min * sz) + 'f'
            offset_z = str.format("{0:.6f}", ly) + 'f'
            box_width = dx
            box_height = dz
            box_depth = dy
            box_rotate_point_x = str.format("{0:.6f}", lx) + 'f'
            box_rotate_point_y = str.format("{0:.6f}", 24.-lz) + 'f'
            box_rotate_point_z = str.format("{0:.6f}", ly) + 'f'
            box_rotate_angle_x = str.format("{0:.6f}", rx) + 'f'
            box_rotate_angle_y = str.format("{0:.6f}", -rz) + 'f'
            box_rotate_angle_z = str.format("{0:.6f}", ry) + 'f'

            box_declarations += box_declaration_template.format(boxName=obj.name) + "\n"
            box_instantiations += box_instantiation_template.format(boxName=obj.name,
                                                                    texOffsetX=tex_off_x, texOffsetY=tex_off_y,
                                                                    offsetX=offset_x, offsetY=offset_y,
                                                                    offsetZ=offset_z, width=box_width,
                                                                    height=box_height, depth=box_depth,
                                                                    scaleFactor='0f',
                                                                    rotatePointX=box_rotate_point_x,
                                                                    rotatePointY=box_rotate_point_y,
                                                                    rotatePointZ=box_rotate_point_z,
                                                                    rotateAngleX=box_rotate_angle_x,
                                                                    rotateAngleY=box_rotate_angle_y,
                                                                    rotateAngleZ=box_rotate_angle_z) + "\n"
            box_render_calls += box_render_template.format(boxName=obj.name) + "\n"

    model_class: str = class_file_template.format(modelName="ModelName",
                                                  texWidth=str(tsu),
                                                  texHeight=str(tsv),
                                                  boxDeclarations=box_declarations,
                                                  boxInstantiations=box_instantiations,
                                                  boxRenderCalls=box_render_calls)

    file.write(model_class)


def write_animrenderclass(stream, animation_name, animation_data):
    """
    Write the animation to a stream.
    """

    stream.write(
        '    class '+str(animation_name)+'AnimationRenderer implements IAnimationRenderer {\n'\
        +'        '\
        +'    }')


def write_objects_anim(file):
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
        animations: Boolean indicating if animations shall also be extracted.
    """

    tsu, tsv = get_texture_size(0)
    animap = get_animation_map(bpy.data.objects)
    print(animap)

    # Package imports plus class boilerplate.
    file.write(
        'package net.x.package;\n\n'\
        +'import net.minecraft.client.model.ModelBase;\n'\
        +'import net.minecraft.client.model.ModelRenderer;\n'\
        +'import net.minecraft.entity.Entity;\n'\
        +'import net.minecraftforge.fml.relauncher.Side;\n'\
        +'import net.minecraftforge.fml.relauncher.SideOnly;\n\n'\
        +'@SideOnly(Side.CLIENT)\n'\
        +'class ModelName extends ModelBase\n'\
        +'{\n')
    # Animation interface used to render animation frames.
    file.write(
        '    private interface IAnimationRenderer {\n'\
        +'        public void render(Entity entity, float p_78088_2_, float p_78088_3_, float p_78088_4_, float p_78088_5_, float p_78088_6_, float p_78088_7_);\n'\
        +'    }\n'\
        +'    \n')
    # Partial ticks need to be saved for later use.
    file.write('    private float partialTicks;\n')

    for obj in bpy.data.objects:
        if(obj.type == "MESH"):
            file.write('    public ModelRenderer '+obj.name+';\n')

    file.write('\n'\
            +'    public ModelName()\n'\
            +'    {\n'\
            +'        this.textureWidth = '+str(tsu)+';\n'\
            +'        this.textureHeight = '+str(tsv)+';\n')

    for obj in bpy.data.objects:
        if(obj.type == "MESH"):
            lx, ly, lz = get_location(obj)
            rx, ry, rz, rmode = get_rotation(obj)
            sx, sy, sz = get_scale(obj)
            dx, dy, dz = get_dimensions(obj)
            vx_min, vy_min, vz_min = get_min_vertex(obj)
            u_min, v_min = get_min_uv(obj)

            file.write(
                    '        this.'+obj.name+' = new ModelRenderer(this,'+str(int(u_min*tsu+0.5))+','+str(int(v_min*tsv+0.5))+');\n'\
                    +'        this.'+obj.name+'.addBox('+str.format("{0:.6f}",vx_min*sx)+'f,'+str.format("{0:.6f}",-vz_min*sz)+'f,'+str.format("{0:.6f}",vy_min*sy)+'f,'+str(dx)+','+str(dz)+','+str(dy)+',0f);\n'\
                    +'        this.'+obj.name+'.setRotationPoint('+str.format("{0:.6f}",lx)+'f,'+str.format("{0:.6f}",24.-lz)+'f,'+str.format("{0:.6f}",ly)+'f);\n'\
                    +'        this.'+obj.name+'.rotateAngleX = '+str.format("{0:.6f}",rx)+'f;\n'\
                    +'        this.'+obj.name+'.rotateAngleY = '+str.format("{0:.6f}",-rz)+'f;\n'\
                    +'        this.'+obj.name+'.rotateAngleZ = '+str.format("{0:.6f}",ry)+'f;\n'\
#                    +'        this.'+obj.name+'.setTextureSize('+str(tsu)+','+str(tsv)+');\n'\
                    +'        this.'+obj.name+'.mirror = true;\n')

    file.write(
            '    }\n\n'\
            +'    public void setLivingAnimations(EntityLivingBase entity, float p_78086_2_, float p_78086_3_, float p_78086_4_)\n'\
            +'    {\n'\
            +'        this.partialTicks = p_78086_4_;\n'\
            +'    }\n'\
            +'    \n'\
            +'    public void render(Entity entity, float p_78088_2_, float p_78088_3_, float p_78088_4_, float p_78088_5_, float p_78088_6_, float p_78088_7_)\n'\
            +'    {\n'\
            +'        this.setRotationAngles(p_78088_2_, p_78088_3_, p_78088_4_, p_78088_5_, p_78088_6_, p_78088_7_, entity);\n')
    for obj in bpy.data.objects:
        if(obj.type == "MESH"):
            file.write('        this.'+obj.name+'.render(p_78088_7_);\n')
    file.write(
            '    }\n\n'\
            +'    public void setRotationAngles(float p_78087_1_, float p_78087_2_, float p_78087_3_, float p_78087_4_, float p_78087_5_, float p_78087_6_, Entity p_78087_7_)\n'\
            +'    {\n'\
            +'    }\n'\
            +'}\n')


def write_data(context, filepath, export_anim):
    """
    Write the current mesh to file.
    
    Args:
        context: The current blender context.
        filepath: String containing the path to the out-file.
        export_anim: Boolean specifying if animations are to be exported.
    """

    if(bpy.context.active_object.mode != "OBJECT"):
        bpy.ops.object.mode_set(mode='OBJECT')
    out = open(filepath, "w")
    if export_anim:
        write_objects_anim(out)
    else:
        write_objects(out)
    out.close()

    return {'FINISHED'}

