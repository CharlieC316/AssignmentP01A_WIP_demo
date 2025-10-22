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
        blade_name, _ = cmds.polycube(height=self.blade_length, 
                                      width=self.blade_width,
                                      depth=self.blade_thickness,
                                      name="blade1")
        
        # position of the blade vertically 
        cmds.xform(blade_name, translation=[0, self.blade_length / 2.0 + self.gaurd_height, 0])
        return blade_name