import bpy
from bpy.props import PointerProperty
from math import cos, sin, radians
import blf
from mathutils import Vector
from bpy_extras import view3d_utils

###### GENERIC INTRO ######

bl_info = {
    'name': 'Creating a Perspective Grid for Grease Pencil',
    'category': 'All',
    'author': 'Nerses Chorekchyan',
    'version': (1, 0, 0),
    'blender': (2, 90, 0),
    'location': '',
    'description': 'A Simple Perspective Grid Generator for Grease Pencil'
}




#Custom Settings for Perspective Grid
class ScenePerspectiveSettings(bpy.types.PropertyGroup):
    # use an annotation
    LineCount : bpy.props.IntProperty(
        name = "LineCount",
        description = "",
        default = 20,
        min = 1,
        max = 100
        )    
    LineWidth : bpy.props.IntProperty(
        name = "LineWidth",
        description = "",
        default = 1,
        min = 1,
        max = 5
        ) 
    LineDensity2PP : bpy.props.IntProperty(
        name = "2PP Density",
        description = "",
        default = 1000,
        min = 1,
        max = 2000
        ) 
    Spacing2PP : bpy.props.IntProperty(
        name = "2PP Spacing",
        description = "",
        default = 1,
        min = 1,
        max = 5
        ) 

######################################### UI ###########################################
#PANEL FOR UI###############

class PERSPECTIVEGRID_PT_main(bpy.types.Panel):
    bl_idname = "PERSPECTIVEGRID_PT_main.panel"
    bl_label = "Perspective Grid Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Perspective Grid"
    
    ###Draw the Buttons And Stuff
    def draw(self, context):
        panelOp=self.layout.operator
        panelOp("onepointperspective.obj", icon='MESH_CUBE', text="Create 1PP VP")
        panelOp("onepointperspective.grid", icon='MESH_CUBE', text="Create 1PP Map")
        panelOp("twopointperspective.obj", icon='MESH_CUBE', text="Create 2PP VPs")
        panelOp("twopointperspective.grid", icon='MESH_CUBE', text="Create 2PP Grid")  
        
        row1=self.layout.row(align=True)
        row2=self.layout.row(align=True)
        row3=self.layout.row(align=True)
        row4=self.layout.row(align=True)
        
        row1.prop(PerspectiveSettings, "LineCount")    
        row2.prop(PerspectiveSettings, "LineWidth")
        row3.prop(PerspectiveSettings, "LineDensity2PP")
        row4.prop(PerspectiveSettings, "Spacing2PP")
        
        
        scene = context.scene
        layout = self.layout
        col = layout.column()
        col.prop(scene, "my_collection")
        col = layout.column()
        col.enabled = True if scene.my_collection else False
        col.prop(scene, "my_collection_objects")
        panelOp("twopointperspective.lock", icon='MESH_CUBE', text="Lock Other Objects")
        panelOp("twopointperspective.release", icon='MESH_CUBE', text="Release Locks")
        
        panelOp("twopointperspective.guide", icon='MESH_CUBE', text="2PP Assists")
        
        
#########################################################################################################
##################################CLASSES##################################
#ONE POINT PERSPECTIVE

class ONEPOINTPERSPECTIVE_OT_obj(bpy.types.Operator):
    bl_idname = "onepointperspective.obj"
    bl_label = "One Point Perspective System" 

    def execute(self, context):    
#        global gp_1PP
        gp_1PP = ''

        #Delete and Recreate Objects to avoid duplicates
        try:
            bpy.data.grease_pencils['One Point Perspective']
            bpy.data.grease_pencils.remove(bpy.data.grease_pencils['One Point Perspective'])
            bpy.data.objects.remove(bpy.data.objects['One Point Perspective'])
        except:
            gp_1PP = GP_CREATE("One Point Perspective")      
            
        GP_VP_CREATION(gp_1PP, 1)                   

        return {'FINISHED'}

class ONEPOINTPERSPECTIVE_OT_vp(bpy.types.Operator):
    bl_idname = "onepointperspective.grid"
    bl_label = "One Point Perspective Vanishing Point Generation"  
    
    def execute(self, context):
        GP_1PP_MAP(bpy.data.grease_pencils['One Point Perspective']) 
        return {'FINISHED'}


#TWO POINT PERSPECTIVE         
class TWOPOINTPERSPECTIVE_OT_obj(bpy.types.Operator):
    bl_idname = "twopointperspective.obj"
    bl_label = "Two Point Perspective Grease Pencil Object Genration"   
    
    def execute(self, context):    
        gp_2PP = ''
        
        #Delete and Recreate Objects to avoid duplicates
        try:
            bpy.data.grease_pencils['Two Point Perspective']
            bpy.data.grease_pencils.remove(bpy.data.grease_pencils['Two Point Perspective'])
            bpy.data.objects.remove(bpy.data.objects['Two Point Perspective'])
        except:
            gp_2PP = GP_CREATE("Two Point Perspective")             
        
        GP_VP_CREATION(gp_2PP, 2)   
        return {'FINISHED'}    
       
class TWOPOINTPERSPECTIVE_OT_vp(bpy.types.Operator):
    bl_idname = "twopointperspective.grid"
    bl_label ="One Point Perspective Grease Pencil Object Genration" 
    
    

    def execute(self, context):
        gp_2PP = bpy.data.grease_pencils['Two Point Perspective']
        GP_2PP_MAP(gp_2PP)
        return {'FINISHED'}
    
class TWOPOINTPERSPECTIVELOCK_OT_lock(bpy.types.Operator):
    bl_idname = "twopointperspective.lock"
    bl_label ="Two Point Perspective Locks"
         
    #This locks everything except what is selected in the panel
    def execute(self,context):

        obj_count = len(bpy.data.objects)
        obj_values = [True]*obj_count
        for i in range(len(obj_values)):
            setattr(bpy.data.objects[i], "hide_select", obj_values[i])
            
        bpy.data.scenes["Scene"].my_collection_objects.hide_select = False
        return {'FINISHED'}
        
class TWOPOINTPERSPECTIVERELEASE_OT_lock(bpy.types.Operator):
    bl_idname = "twopointperspective.release"
    bl_label ="Two Point Perspective Lock Release" 
        
    #This release locks on everything
    def execute(self, context):

        obj_count = len(bpy.data.objects)
        obj_values = [False]*obj_count
        for i in range(len(obj_values)):
            setattr(bpy.data.objects[i], "hide_select", obj_values[i])
        return {'FINISHED'}
            

############################## FUNCTIONS ###############################################    
######################### HIGH LEVEL FUNCTIONS ###########################################
#CREATE GREASE PENCIL OBJECTS
def GP_CREATE(gp_name):





    gp_data = bpy.data.grease_pencils.new(gp_name)
    gp_obj = bpy.data.objects.new(gp_data.name, gp_data)
    bpy.context.collection.objects.link(gp_obj)
    #Create layer
    gp_layer = gp_data.layers.new(gp_name)
    #Create frame
    gp_frame = gp_layer.frames.new(bpy.context.scene.frame_current)
    #Create stroke for the Horizon Line or VPs
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.line_width = PerspectiveSettings.LineWidth + 10

    return gp_data

###
#CREATE VANISHING POINTS
def GP_VP_CREATION(gp_input, vp_count):

    gp_stroke = gp_input.layers[0].frames[0].strokes[0]
    gp_stroke.line_width = PerspectiveSettings.LineWidth + 10

    #Add the Vanishing Point
    if vp_count == 1:
        gp_stroke.points.add(count=1)
        gp_stroke.points[0].co = (0,0,0)
    elif vp_count == 2:
        gp_stroke.points.add(count=2)
        gp_stroke.points[0].co = (-5,0,0)
        gp_stroke.points[1].co = (5,0,0)
        
    return {'FINISHED'}

#########################################################
###
#ONE POINT PERSPECTIVE MAP

def GP_1PP_MAP(gp_input):

    linecount = PerspectiveSettings.LineCount
    line_width = PerspectiveSettings.LineWidth
    radius = 15
    vp_loc = gp_input.layers[0].frames[0].strokes[0].points[0].co

    
    for x in range(linecount):
        gp_stroke = gp_input.layers[0].frames[0].strokes.new()
        gp_stroke.line_width = line_width
        gp_stroke.points.add(count=2)
        
        angle=radians(180/linecount*(x+1))
        gp_stroke.points[0].co = (vp_loc[0] + (radius * sin(angle)), 0, vp_loc[2] + (radius * cos(angle)))
        gp_stroke.points[1].co = (vp_loc[0] - (radius * sin(angle)), 0, vp_loc[2] - (radius * cos(angle)))

###
#TWO POINT PERSPECTIVE MAP
def GP_2PP_MAP(gp_input):

    density = PerspectiveSettings.LineDensity2PP
    line_width = PerspectiveSettings.LineWidth 
    spacing = PerspectiveSettings.Spacing2PP  
    plot_y = 0 
    plot_z_top = 5
    plot_z_bottom = -5
    #Identify Vanishing Point Locations
    vp1_loc = gp_input.layers[0].frames[0].strokes[0].points[0].co
    vp2_loc = gp_input.layers[0].frames[0].strokes[0].points[1].co
    vp_diff = vp1_loc - vp2_loc
       
    def GP_2PP_GRID_STROKE(location, vp, line_width):
        gp_stroke = gp_input.layers[0].frames[0].strokes.new() 
        gp_stroke.points.add(count = density)
        

        #Add points based on the density        
        for x in range(density):
            plot_x_1 = (vp1_loc[0] + (spacing * x/2)) + vp_diff[0] 
            plot_x_2 = (vp1_loc[1] - (spacing * x/2)) - vp_diff[0] 
            grid_stroke = gp_input.layers[0].frames[0].strokes.new()
            
            grid_stroke.line_width = line_width
            grid_stroke.points.add(count = 2)
            grid_stroke.points[0].strength = 1
            grid_stroke.points[1].strength = 0
            
            #Plot the grid
            if location == "top":               
                if vp == 1:
                    grid_stroke.points[0].co = (plot_x_1 , plot_y, plot_z_top)
                    grid_stroke.points[1].co = vp1_loc
                elif vp == 2:
                    grid_stroke.points[0].co = (plot_x_2 , plot_y, plot_z_top)
                    grid_stroke.points[1].co = vp2_loc
            if location == "bottom":
                if vp == 1:
                    grid_stroke.points[0].co = (plot_x_1, plot_y, plot_z_bottom)
                    grid_stroke.points[1].co = vp1_loc
                elif vp == 2:
                    grid_stroke.points[0].co = (plot_x_2, plot_y, plot_z_bottom)
                    grid_stroke.points[1].co = vp2_loc


    GP_2PP_GRID_STROKE("top", 1, 5)
    GP_2PP_GRID_STROKE("bottom", 1,  5)
    GP_2PP_GRID_STROKE("top", 2, 5)
    GP_2PP_GRID_STROKE("bottom", 2, 5)
                
    return {'FINISHED'}  


########################################################
#TWO POINT PERSPECTIVE ASSISSTS
class TWOPOINTPERSPECTIVE_OT_guide(bpy.types.Operator):

    bl_idname = "twopointperspective.guide"
    bl_label = "Two Point Perspective Guide"





    def modal(self, context, event):

      
        context.area.tag_redraw()
        
        #Get the mouse position thanks to the event            
        self.mouse_pos = event.mouse_region_x, event.mouse_region_y
        
        #Contextual active object, 2D and 3D regions
        self.object = bpy.context.object
        region = bpy.context.region
        region3D = bpy.context.space_data.region_3d

        #The direction indicated by the mouse position from the current view
        self.view_vector = view3d_utils.region_2d_to_vector_3d(region, region3D, self.mouse_pos)
        #The view point of the user
        self.view_point = view3d_utils.region_2d_to_origin_3d(region, region3D, self.mouse_pos)
        #The 3D location in this direction
        self.world_loc = view3d_utils.region_2d_to_location_3d(region, region3D, self.mouse_pos, self.view_vector)
 
        z = Vector( (0,0,1) )
        self.normal = z

        if self.object:
            bpy.data.grease_pencils['Assist Tool'].layers['Assists'].frames[0].strokes[0].points[1].co = self.world_loc
            self.object.rotation_euler = z.rotation_difference( self.normal ).to_euler()

        #ESC to Escape Assists
        if event.type in {'ESC'}:
            bpy.data.grease_pencils['Assist Tool'].layers['Assists'].frames[0].strokes[0].points[1].co = bpy.data.grease_pencils['Two Point Perspective'].layers[0].frames[0].strokes[0].points[1].co
            context.window_manager.event_timer_remove(self.timer)
            return {'CANCELLED'}
        elif event.type == 'MOUSEMOVE':
            bpy.ops.gpencil.draw('INVOKE_DEFAULT',wait_for_input=False)
            return {'RUNNING_MODAL'}

        return {'RUNNING_MODAL'}
    
    #############
    
    def invoke(self, context, event):
        self.timer = context.window_manager.event_timer_add(1e3, window=context.window)
        
        try:
            gp_Assist = bpy.data.grease_pencils['Assist Tool']
            bpy.data.grease_pencils.remove(bpy.data.grease_pencils['Assist Tool'])
        except:
            print("Great")
        
        gp_Assist = GP_CREATE('Assist Tool')        
        
        
        try:
            gp_Assist.layers['Assists']
        except:
            gp_Assist_layer = gp_Assist.layers.new('Assists')
            gp_Assist_frame = gp_Assist_layer.frames.new(bpy.context.scene.frame_current)
            gp_Assist_stroke = gp_Assist_frame.strokes.new()

            gp_Assist_stroke.line_width = PerspectiveSettings.LineWidth + 10

            gp_Assist_point = gp_Assist_stroke.points.add(count = 3)


        gp_Assist = bpy.data.grease_pencils['Assist Tool']  
        gp_Assist.layers['Assists'].frames[0].strokes[0].points[0].co = bpy.data.grease_pencils['Two Point Perspective'].layers[0].frames[0].strokes[0].points[0].co
        gp_Assist.layers['Assists'].frames[0].strokes[0].points[1].co = bpy.data.grease_pencils['Two Point Perspective'].layers[0].frames[0].strokes[0].points[1].co 
        gp_Assist.layers['Assists'].frames[0].strokes[0].points[2].co = bpy.data.grease_pencils['Two Point Perspective'].layers[0].frames[0].strokes[0].points[1].co        

        
        
        
        
        if context.area.type == 'VIEW_3D':
            args = (self, context)
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            gp_Assist.layers['Assists'].frames[0].strokes[1].points[1].co = self.world_loc
            context.window_manager.event_timer_remove(self.timer)
            return {'CANCELLED'}
        
        
########################################################




############OBJECT SELECTOR CALLBACK FUNCTION

def filter_callback(self, object):
    return object.name in self.my_collection.objects.keys()


####### TESTING


#bpy.utils.register_class(ScenePerspectiveSettings)
#bpy.types.Scene.PerspectiveSettings = bpy.props.CollectionProperty(type=ScenePerspectiveSettings)
#PerspectiveSettings = bpy.context.scene.PerspectiveSettings.add()

#REGISTRATION#############################################

def register():
    
    #new
    bpy.utils.register_class(ScenePerspectiveSettings)
    bpy.types.Scene.PerspectiveSettings = bpy.props.CollectionProperty(type=ScenePerspectiveSettings)
    
    
    bpy.utils.register_class(PERSPECTIVEGRID_PT_main)
    bpy.utils.register_class(ONEPOINTPERSPECTIVE_OT_obj)
    bpy.utils.register_class(ONEPOINTPERSPECTIVE_OT_vp)
    bpy.utils.register_class(TWOPOINTPERSPECTIVE_OT_obj)
    bpy.utils.register_class(TWOPOINTPERSPECTIVE_OT_vp)
    bpy.utils.register_class(TWOPOINTPERSPECTIVE_OT_guide)
    bpy.utils.register_class(TWOPOINTPERSPECTIVERELEASE_OT_lock)
    bpy.utils.register_class(TWOPOINTPERSPECTIVELOCK_OT_lock)


    bpy.types.Scene.my_collection = PointerProperty(
        name="Collection",
        type=bpy.types.Collection)
    bpy.types.Scene.my_collection_objects = PointerProperty(
        name="Object",
        type=bpy.types.Object,
        poll=filter_callback)

#UNREGISTRATION
    
def unregister():
    
    bpy.utils.unregister_class(ScenePerspectiveSettings)
   
    bpy.utils.unregister_class(PERSPECTIVEGRID_PT_main)
    bpy.utils.unregister_class(ONEPOINTPERSPECTIVE_OT_obj)
    bpy.utils.unregister_class(ONEPOINTPERSPECTIVE_OT_vp)
    bpy.utils.unregister_class(TWOPOINTPERSPECTIVE_OT_obj)
    bpy.utils.unregister_class(TWOPOINTPERSPECTIVE_OT_vp)
    bpy.utils.unregister_class(TWOPOINTPERSPECTIVE_OT_guide)
    bpy.utils.unregister_class(TWOPOINTPERSPECTIVERELEASE_OT_lock)
    bpy.utils.unregister_class(TWOPOINTPERSPECTIVELOCK_OT_lock)
    
    bpy.types.Scene.my_collection = PointerProperty(
        name="Collection",
        type=bpy.types.Collection)
        
    bpy.types.Scene.my_collection_objects = PointerProperty(
        name="Object",
        type=bpy.types.Object,
        poll=filter_callback)
  
        
    del bpy.types.Scene.PerspectiveSettings
    del bpy.types.Scene.my_collection
    del bpy.types.Collection.my_collection_objects
    
    

    
if __name__ == '__main__':
    register()
    PerspectiveSettings = bpy.context.scene.PerspectiveSettings.add()


