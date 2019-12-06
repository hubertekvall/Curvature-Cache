

bl_info = {
    "name": "CurvatureCache",
    "category": "3D View",
    "blender": (2, 81, 0),
    "author": "Hubert Ekvall",
    "description": "Simple tool for quickly baking curvature information into the object's vertex colors. Useful for edge masking etc"
    }

import bpy

class CurvatureCachePanel(bpy.types.Panel):
    """Curvature Cache Panel"""
    bl_label = "CurvatureCache"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "Curvature Generator"


    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='SCENE')

    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.separator()
        row = col.row(align = True)
        op = row.operator("cur.bake", text="BAKE", icon="RENDER_RESULT")

        









class CurvatureBaker(bpy.types.Operator):
    """Bake curvature into vertex colors"""
    bl_idname = "cur.bake"
    bl_label = "CurvatureCache"
    bl_options = {"UNDO"}


    def generate_curvature():
        bpy.ops.paint.vertex_paint_toggle()
        bpy.ops.mesh.vertex_color_remove()
        bpy.ops.paint.vertex_color_dirt()
        bpy.ops.paint.vertex_paint_toggle()


    def bake():
        # The base object needs a set of vertex colors for this to work
        obj = bpy.context.active_object
        generate_curvature()
        
        # Try to find an existing Vertex cache and Vertex Color Transfer modifier
        vertex_cache = next((vc for vc in bpy.data.objects if 'VertexCache' in vc.name and vc.parent == obj), None)
        vertex_color_transfer = next((vcf for vcf in obj.modifiers if vcf.name == "VertexColorTransfer"), None)

        
        
        # Create a duplicate of our base object and convert it to a mesh, then generate curvature
        if vertex_cache is None:
            bpy.ops.object.duplicate()
            vertex_cache = bpy.context.active_object
            bpy.ops.object.convert(target='MESH')  
            generate_curvature()
            
        # Remove the existing Vertex Cache and redo the process
        else:
            bpy.data.objects.remove(vertex_cache)
            
            bpy.ops.object.duplicate()
            vertex_cache = bpy.context.active_object
            bpy.ops.object.convert(target='MESH')  
            generate_curvature()
                    
            
        # If no modifier could be find create one and set the proper settings
        if vertex_color_transfer is None:
            vertex_color_transfer = obj.modifiers.new('VertexColorTransfer', type='DATA_TRANSFER')
            vertex_color_transfer.use_loop_data = True
            vertex_color_transfer.data_types_loops = {'VCOL'}
            vertex_color_transfer.loop_mapping = 'POLYINTERP_NEAREST'
            vertex_color_transfer.object = vertex_cache   
            
        # Just make sure the new vertex cache is the target    
        else:
            vertex_color_transfer.object = vertex_cache
        
        # Set the name and parent it to the base, then hide it from render and viewing, will still transfer like normal
        vertex_cache.name = 'VertexCache'
        vertex_cache.select_set(False)
        vertex_cache.parent = obj   
        vertex_cache.hide_set(True)
        vertex_cache.hide_render = True
            
        # Make sure our base is selected again    
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    

    def execute(self, context):  
        bake()
        return {'FINISHED'}




def register():
    bpy.utils.register_class(CurvatureBaker)
    bpy.utils.register_class(CurvatureCachePanel)


def unregister():
    bpy.utils.unregister_class(CurvatureBaker)
    bpy.utils.unregister_class(CurvatureCachePanel)



    
if __name__ == "__main__":
    register()
