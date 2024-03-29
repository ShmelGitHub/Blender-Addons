import bpy

bl_info = {
    "name": "Auto Smooth",
    "author": "DZXBK",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Object",
    "description": "Automatically adds or toggles the Auto Smooth modifier to the selected object",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

class OBJECT_MT_add_node_group_menu(bpy.types.Menu):
    bl_label = "Node Group Modifier Menu"
    bl_idname = "OBJECT_MT_add_node_group_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.add_node_group", text="Add Node Group Modifier")

class OBJECT_OT_add_node_group(bpy.types.Operator):
    """Add Node Group Modifier"""
    bl_label = "Add Node Group"
    bl_idname = "object.add_node_group"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the selected object
        obj = context.active_object

        # Check if the object exists and is of type MESH
        if obj and obj.type == 'MESH':
            # Check if the "Node Group" modifier with the name "Smooth by Angle" exists
            modifier_exists = False
            modifier_index = None
            for index, modifier in enumerate(obj.modifiers):
                if modifier.type == 'NODES' and modifier.node_group.name == "Smooth by Angle":
                    modifier_exists = True
                    modifier_index = index
                    break
            
            # If the modifier exists, move it to the end of the list and change its name
            if modifier_exists:
                obj.modifiers.move(modifier_index, len(obj.modifiers) - 1)
                obj.modifiers[-1].name = "Auto Smooth"
            else:
                # If the modifier doesn't exist, add it and change its name
                bpy.ops.object.modifier_add_node_group(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="geometry_nodes\\smooth_by_angle.blend\\NodeTree\\Smooth by Angle")
                obj.modifiers[-1].name = "Auto Smooth"

        # Add the Auto Smooth modifier
        bpy.ops.object.shade_smooth()

        return {'FINISHED'}

def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator_context = 'INVOKE_DEFAULT' # To invoke the operator through the context menu
    layout.operator("object.add_node_group", text="Auto Smooth")

classes = (
    OBJECT_MT_add_node_group_menu,
    OBJECT_OT_add_node_group,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(draw_menu)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_menu)

if __name__ == "__main__":
    register()
