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

# Example usage
if __name__ == "__main__":
    sword = Sword()
    
    # Customize your sword here
    sword.blade_length = 8
    sword.blade_width = 0.3
    sword.blade_thickness = 0.1
    sword.handle_length = 2.0
    sword.pommel_radius = 0.25
    
    sword.build()

