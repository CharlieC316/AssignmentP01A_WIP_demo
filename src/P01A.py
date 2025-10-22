import maya.cmds as cmds

class Sword:
    
    def __init__(self):
     #parameters you can customize
        # Blade
       self.blade_length = 5.0
       self.blade_width = 0.2
       self.blade_thickness = 0.1

       # Gaurd
       self.gaurd_width = 1.2
       self.gaurd_thickness = 0.1
       self.gaurd_height = 0.2

       # Handle 
       self.handle_length = 1.5
       self.handle_radius = 0.15

       # Pommel 
       self.pommel_radius = 0.2

    def build_blade(self):
        blade_name, _ = cmds.polyCube(height=self.blade_length, 
                                      width=self.blade_width,
                                      depth=self.blade_thickness,
                                      name="blade1")
        
        # position of the blade vertically 
        cmds.xform(blade_name, translation=[0, self.blade_length / 2.0 + self.gaurd_height, 0])
        return blade_name
    
    def build_gaurd(self):
        gaurd_name, _ = cmds.polyCube(height=self.gaurd_height, 
                                      width=self.gaurd_width,
                                      depth=self.gaurd_thickness, name="gaurd1")
        
        # position at base of blade
        cmds.xform(gaurd_name, translation=[0, self.gaurd_height / 2.0, 0])
        return gaurd_name
    
    def build_handle(self):
        handle_name = cmds.polyCylinder(height=self.handle_length,
                                        radius=self.handle_radius,
                                        subdivisonsAxis=16,
                                        name="handle1")[0]
        # position the handle under the gaurd
        y_pos = -self.handle_length / 2.0
        cmds.xform(handle_name, translation=[0, y_pos, 0])
        return handle_name