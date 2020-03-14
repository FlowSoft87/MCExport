bl_info = {
    "name":         "Minecraft cube-exporter",
    "author":       "Flo",
    "version":      (2,0,0),
    "blender":      (2,81,0),
    "location":     "File > Import-Export",
    "description":  "Export mesh in Minecraft cube format.",
    "warning":      "",
    "category":     "Import-Export"
}

import bpy

from MCExport.Exporter import MinecraftCubeModelExporter
from MCExport.Toolmenu import Menu


def register():
    bpy.utils.register_class(Menu.OBJECT_OT_unwrapButton)
    bpy.utils.register_class(Menu.OBJECT_OT_addBoxButton)
    bpy.utils.register_class(Menu.ToolsPanel)
    bpy.utils.register_class(MinecraftCubeModelExporter.MinecraftCubeModelExporter)
    # Add the operator to the dynamic menu "INFO_MT_file_export"
    bpy.types.TOPBAR_MT_file_export.append(MinecraftCubeModelExporter.menu_func_export)


def unregister():
    bpy.utils.unregister_class(Menu.OBJECT_OT_unwrapButton)
    bpy.utils.unregister_class(Menu.OBJECT_OT_addBoxButton)
    bpy.utils.unregister_class(Menu.ToolsPanel)
    bpy.utils.unregister_class(MinecraftCubeModelExporter.MinecraftCubeModelExporter)
    bpy.types.TOPBAR_MT_file_export.remove(MinecraftCubeModelExporter.menu_func_export)


if __name__ == "__main__":
    register()
