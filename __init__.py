bl_info = {
    "name":         "Minecraft cube-exporter",
    "author":       "Flo",
    "blender":      (2,69,0),
    "version":      (0,0,1),
    "location":     "File > Import-Export",
    "description":  "Export mesh in Minecraft cube format",
    "category":     "Import-Export"
}

import os
import bpy

from MinecraftExporter.Exporter import MinecraftCubeModelExporter
from MinecraftExporter.Toolmenu import Menu

def register():
    bpy.utils.register_class(Menu.OBJECT_OT_unwrapButton)
    bpy.utils.register_class(Menu.OBJECT_OT_addBoxButton)
    bpy.utils.register_class(Menu.ToolsPanel)
    bpy.utils.register_class(MinecraftCubeModelExporter.MinecraftCubeModelExporter)
    # Add the operator to the dynamic menu "INFO_MT_file_export"
    bpy.types.INFO_MT_file_export.append(MinecraftCubeModelExporter.menu_func_export)

def unregister():
    bpy.utils.unregister_class(Menu.OBJECT_OT_unwrapButton)
    bpy.utils.unregister_class(Menu.OBJECT_OT_addBoxButton)
    bpy.utils.unregister_class(Menu.ToolsPanel)
    bpy.utils.unregister_class(MinecraftCubeModelExporter.MinecraftCubeModelExporter)
    bpy.types.INFO_MT_file_export.remove(MinecraftCubeModelExporter.menu_func_export)

if __name__ == "__main__":
    register()
