import bpy

bl_info = {
    "name": "compify addon by iyofs",
    "blender": (3, 3, 0),
    "category": "Object",
}

class compHelper(bpy.types.Panel):
    bl_label = "iyofs compHelper"
    bl_idname = "NODE_PT_MAINPANEL"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "compHelper"

    def draw(self, context):
        layout = self.layout

        column = layout.column()
        column.label(text="you will need to re-add the node ")
        column.label(text="after changing the resolution")
        
        column.operator("node.vignette")
        column.label(text="Glare node")
        column.operator("node.glare")

        







def create_vignette_group(context, operator, group_name):
#    enable use nodes

    bpy.context.scene.use_nodes = True
    
    vignette_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    group_in = vignette_group.nodes.new('NodeGroupInput')
    group_in.location = (-200,0)
    vignette_group.inputs.new('NodeSocketColor', 'Image')
    vignette_group.inputs.new('NodeSocketFloat', 'Blur factor')
    vignette_group.inputs[1].min_value = 0
    vignette_group.inputs[1].default_value = 1
    
    group_out = vignette_group.nodes.new('NodeGroupOutput')
    group_out.location = (800,0)
    vignette_group.outputs.new('NodeSocketColor', 'Output')
    
    
    
    
    screen_height = bpy.context.scene.render.resolution_y
    screen_width = bpy.context.scene.render.resolution_x
    if screen_height > screen_width:
        vignette_width = screen_width/screen_height
        vignette_height = 1
    elif screen_height < screen_width:
        vignette_width = 1
        vignette_height = screen_height/screen_width
    elif screen_height == screen_width:
        vignette_height = 1
        vignette_width = 1
        
        
        
    EllipseMask_node = vignette_group.nodes.new(type= 'CompositorNodeEllipseMask')
    EllipseMask_node.location = (0,0)
    EllipseMask_node.width = vignette_width
    EllipseMask_node.height = vignette_height
    
    
    
    Blur_node = vignette_group.nodes.new(type= 'CompositorNodeBlur')
    Blur_node.location = (360,50)
    Blur_node.size_x = 350
    Blur_node.size_y = 350
    
    
    MixRGB_node = vignette_group.nodes.new(type= 'CompositorNodeMixRGB')
    MixRGB_node.location = (590,0)
    MixRGB_node.inputs[1].default_value = (0, 0, 0, 1)
    
    
    linkvignette = vignette_group.links.new
    linkvignette(group_in.outputs[1], Blur_node.inputs[1])
    linkvignette(group_in.outputs[0], MixRGB_node.inputs[2])
    linkvignette(Blur_node.outputs[0], MixRGB_node.inputs[0])
    linkvignette(EllipseMask_node.outputs[0], Blur_node.inputs[0])
    linkvignette(MixRGB_node.outputs[0], group_out.inputs[0])
    

    
    return vignette_group


def create_glare_group(context, operator, group_name):
#    enable use nodes

    bpy.context.scene.use_nodes = True
    
    glare_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    group_in = glare_group.nodes.new('NodeGroupInput')
    group_in.location = (-200,0)
    glare_group.inputs.new('NodeSocketColor', 'Image')
    glare_group.inputs.new('NodeSocketFloat', 'glare mix factor')
    glare_group.inputs.new('NodeSocketFloat', 'image mix factor')
    glare_group.inputs.new('NodeSocketFloat', 'glaring factor')
    glare_group.inputs[1].min_value = 0
    glare_group.inputs[1].max_value = 1
    glare_group.inputs[1].default_value = 0.3
    glare_group.inputs[2].min_value = 0
    glare_group.inputs[2].max_value = 1
    glare_group.inputs[2].default_value = 0.3
    
    group_out = glare_group.nodes.new('NodeGroupOutput')
    group_out.location = (800,0)
    glare_group.outputs.new('NodeSocketColor', 'Output')
    
    exposure_node = glare_group.nodes.new(type= 'CompositorNodeExposure')
    exposure_node.location = (-50,-180)
    
    
    
    
    glare_node1 = glare_group.nodes.new(type= 'CompositorNodeGlare')
    glare_node1.location = (100,0)
    glare_node1.glare_type = 'FOG_GLOW'
    glare_node1.quality = 'HIGH'
    glare_node1.mix = 1
    glare_node1.threshold = 10
    glare_node1.size = 6
    
    glare_node2 = glare_group.nodes.new(type= 'CompositorNodeGlare')
    glare_node2.location = (100,-250)
    glare_node2.glare_type = 'FOG_GLOW'
    glare_node2.quality = 'MEDIUM'
    glare_node2.mix = 1
    glare_node2.threshold = 1
    glare_node2.size = 9
    
    glare_mix_node = glare_group.nodes.new(type= 'CompositorNodeMixRGB')
    glare_mix_node.location = (300,-150)
    glare_mix_node.blend_type = 'ADD'

    image_mix_node = glare_group.nodes.new(type= 'CompositorNodeMixRGB')
    image_mix_node.location = (500,0)
    image_mix_node.blend_type = 'ADD'    
    
    
    linkglare = glare_group.links.new
    linkglare(exposure_node.outputs[0], glare_node1.inputs[0])
    linkglare(exposure_node.outputs[0], glare_node2.inputs[0])
    linkglare(group_in.outputs[0], exposure_node.inputs[0])
    linkglare(group_in.outputs[3], exposure_node.inputs[1])
    linkglare(group_in.outputs[0], image_mix_node.inputs[1])
    linkglare(group_in.outputs[2], image_mix_node.inputs[0])
    linkglare(glare_mix_node.outputs[0], image_mix_node.inputs[2])
    linkglare(glare_node1.outputs[0], glare_mix_node.inputs[1])
    linkglare(glare_node2.outputs[0], glare_mix_node.inputs[2])
    linkglare(group_in.outputs[1], glare_mix_node.inputs[0])
    linkglare(image_mix_node.outputs[0], group_out.inputs[0])
    
    
    return glare_group
    







class NODE_VIGNETTE(bpy.types.Operator):
    bl_label = "add vignette node"
    bl_idname = 'node.vignette'
    
    def execute(self, context):
        custom_node_name = "vignette Node"
        my_group = create_vignette_group(self, context, custom_node_name)
        test_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        test_node.node_tree = bpy.data.node_groups[my_group.name]
        
        return{'FINISHED'}
    
    
    
    
class NODE_GLARE(bpy.types.Operator):
    bl_label = "add glare node"
    bl_idname = 'node.glare'
    
    def execute(self, context):
        custom_node_name = "glare Node"
        my_group = create_glare_group(self, context, custom_node_name)
        test_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        test_node.node_tree = bpy.data.node_groups[my_group.name]
        
        return{'FINISHED'}
        
    


def register():
    bpy.utils.register_class(compHelper)
    bpy.utils.register_class(NODE_VIGNETTE)
    bpy.utils.register_class(NODE_GLARE)

    

def unregister():
    bpy.utils.unregister_class(compHelper)
    bpy.utils.unregister_class(NODE_VIGNETTE)
    bpy.utils.unregister_class(NODE_GLARE)

if __name__ == "__main__":
    register()
