import maya.cmds as cmds


class Sword:
    def __init__(self):
        # Parameters you can customize
        self.blade_length = 5.0
        self.blade_width = 0.2
        self.blade_thickness = 0.1

        self.guard_width = 1.2
        self.guard_thickness = 0.1
        self.guard_height = 0.2

        self.handle_length = 1.5
        self.handle_radius = 0.15

        self.pommel_radius = 0.2

    def clear_existing(self):
        """Deletes the existing sword before rebuilding"""
        if self.sword_group and cmds.objExists(self.sword_group):
            cmds.delete(self.sword_group)
            self.sword_group = None

    def build_blade(self):
        blade_name, _ = cmds.polyCube(
            height=self.blade_length,
            width=self.blade_width,
            depth=self.blade_thickness,
            name="blade"
        )
        # Position the blade vertically
        cmds.xform(blade_name, translation=[0, self.blade_length / 2.0 + self.guard_height, 0])
        return blade_name

    def build_guard(self):
        guard_name, _ = cmds.polyCube(
            height=self.guard_height,
            width=self.guard_width,
            depth=self.guard_thickness,
            name="guard"
        )
        # Position at base of blade
        cmds.xform(guard_name, translation=[0, self.guard_height / 2.0, 0])
        return guard_name

    def build_handle(self):
        handle_name = cmds.polyCylinder(
            height=self.handle_length,
            radius=self.handle_radius,
            subdivisionsAxis=16,
            name="handle"
        )[0]
        # Position the handle under the guard
        y_pos = -self.handle_length / 2.0
        cmds.xform(handle_name, translation=[0, y_pos, 0])
        return handle_name

    def build_pommel(self):
        pommel_name = cmds.polySphere(
            radius=self.pommel_radius,
            subdivisionsX=16,
            subdivisionsY=8,
            name="pommel"
        )[0]
        y_pos = -self.handle_length - self.pommel_radius
        cmds.xform(pommel_name, translation=[0, y_pos, 0])
        return pommel_name

    def build(self):
        parts = []
        parts.append(self.build_blade())
        parts.append(self.build_guard())
        parts.append(self.build_handle())
        parts.append(self.build_pommel())

        sword_group = cmds.group(parts, name="sword")
        print("Sword created!")
        return sword_group
    
    #UI Controller
class SwordUI:
    def __init__(self):
        self.sword = Sword()
        self.window = "SwordBuilderWin"
        self.create_ui()

    def create_ui(self):
        if cmds.window(self.window, exist=True):
            cmds.deleteUI(self.window)

        self.window = cmds.window(self.window, title= "Sword Builder", widthHeight=(300,400))
        cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

        cmds.text(label="Adjust the sword parameters, then click Rebuild", align="center")

        # -- Blade controls --
        self.blade_length_slider = cmds.floatSliderGrp(label="Blade Length", field=True, min=1, max=15, value=self.sword.blade_length)
        self.blade_width_slider = cmds.floatSliderGrp(label="Blade Width", field=True, min=0.05, max=1.0, value=self.sword.blade_width)
        self.blade_thickness_slider = cmds.floatSliderGrp(label="Blade Thickness", field=True, min=0.05, max=1.0, value=self.sword.blade_thickness)

        # -- Handle Controls --
        self.handle_length_slider = cmds.floatSliderGrp(label="Handle Length", field=True, min=0.5, max=5, value=self.sword.handle_length)
        self.handle_radius_slider = cmds.floatSliderGrp(label="Handle Radius", field=True, min=0.05, max=1.0, value=self.sword.handle_radius)

    def rebuild_sword(self, *args):
        """Reads slider values and rebuilds the sword"""
        self.sword.blade_length = cmds.floatSliderGrp(self.blade_length_slider, query=True, value=True)
        self.sword.blade_width = cmds.floatSliderGrp(self.blade_width_slider, query=True, value=True)
        self.sword.blade_thickness = cmds.floatSliderGrp(self.blade_thickness_slider, query=True, value=True)
        self.sword.handle_length = cmds.floatSliderGrp(self.handle_length_slider, query=True, value=True)
        self.sword.handle_radius = cmds.floatSliderGrp(self.handle_radius_slider, query=True, value=True)
        self.sword.pommel_radius = cmds.floatSliderGrp(self.pommel_radius_slider, query=True, value=True)

        self.sword.build()

    def delete_sword(self, *args):
        self.sword.clear_existing()
        print("Sword deleted.")




# Example usage
if __name__ == "__main__":
    SwordUI()