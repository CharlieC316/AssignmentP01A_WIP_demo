import maya.cmds as cmds


class Sword:
    def __init__(self):
        # Blade
        self.blade_length = 5.0
        self.blade_width = 0.2
        self.blade_thickness = 0.1
        self.blade_taper = 0.3  # NEW taper factor (0 = flat, 1 = very sharp)

        # Guard
        self.guard_width = 1.2
        self.guard_thickness = 0.1
        self.guard_height = 0.2

        # Handle 
        self.handle_length = 1.5
        self.handle_radius = 0.15

        # Pommel 
        self.pommel_radius = 0.2

        self.sword_group = None

    def clear_existing(self):
        if self.sword_group and cmds.objExists(self.sword_group):
            cmds.delete(self.sword_group)
            self.sword_group = None

    def build_blade(self):
        blade, _ = cmds.polyCube(
            height=self.blade_length, 
            width=self.blade_width,
            depth=self.blade_thickness,
            name="blade"
        )
        cmds.xform(blade, translation=[0, self.blade_length / 2.0 + self.guard_height, 0])

        # Apply taper to the top vertices
        self.apply_taper(blade)
        return blade

    def apply_taper(self, blade):
        """Scales top vertices to create a sharp tip"""
        verts = cmds.ls(f"{blade}.vtx[*]", fl=True)
        if not verts:
            return

        # Get world positions of all vertices
        top_y = max(cmds.pointPosition(v, world=True)[1] for v in verts)

        # Find all vertices near the top
        threshold = 0.01  # tolerance
        top_verts = [v for v in verts if cmds.pointPosition(v, world=True)[1] > (top_y - threshold)]

        # Compute scale factor
        taper_scale = max(0.01, 1.0 - self.blade_taper)

        # Scale only the top vertices inward
        cmds.scale(taper_scale, 1.0, taper_scale, top_verts, relative=True, pivot=[0, top_y, 0])
        cmds.polyMergeVertex(blade, distance=0.001)

    def build_guard(self):
        guard, _ = cmds.polyCube(
            height=self.guard_height, 
            width=self.guard_width,
            depth=self.guard_thickness,
            name="guard"
        )
        cmds.xform(guard, translation=[0, self.guard_height / 2.0, 0])
        return guard

    def build_handle(self):
        handle = cmds.polyCylinder(
            height=self.handle_length,
            radius=self.handle_radius,
            subdivisionsAxis=16,
            name="handle"
        )[0]
        cmds.xform(handle, translation=[0, -self.handle_length / 2.0, 0])
        return handle

    def build_pommel(self):
        pommel = cmds.polySphere(
            radius=self.pommel_radius,
            subdivisionsX=16,
            subdivisionsY=8,
            name="pommel"
        )[0]
        y_pos = -self.handle_length - self.pommel_radius 
        cmds.xform(pommel, translation=[0, y_pos, 0])
        return pommel

    def build(self):
        self.clear_existing()
        parts = [
            self.build_blade(),
            self.build_guard(),
            self.build_handle(),
            self.build_pommel()
        ]
        self.sword_group = cmds.group(parts, name="sword")
        print("Sword Created with Taper!")


#  UI Controller

class SwordUI:
    def __init__(self):
        self.sword = Sword()
        self.window = "SwordBuilderWin"
        self.create_ui()

    def create_ui(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window)
        
        self.window = cmds.window(self.window, title="🗡️ Sword Builder", widthHeight=(300, 450))
        cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
        cmds.text(label="Adjust parameters, then click Rebuild Sword:", align="center")

        # --- Blade controls ---
        self.blade_length_slider = cmds.floatSliderGrp(label="Blade Length", field=True, min=1, max=15, value=self.sword.blade_length)
        self.blade_width_slider = cmds.floatSliderGrp(label="Blade Width", field=True, min=0.05, max=1.0, value=self.sword.blade_width)
        self.blade_thickness_slider = cmds.floatSliderGrp(label="Blade Thickness", field=True, min=0.05, max=1.0, value=self.sword.blade_thickness)
        self.blade_taper_slider = cmds.floatSliderGrp(label="Blade Taper", field=True, min=0.0, max=1.0, value=self.sword.blade_taper)

        # --- Handle controls ---
        self.handle_length_slider = cmds.floatSliderGrp(label="Handle Length", field=True, min=0.5, max=5, value=self.sword.handle_length)
        self.handle_radius_slider = cmds.floatSliderGrp(label="Handle Radius", field=True, min=0.05, max=1.0, value=self.sword.handle_radius)

        # --- Pommel controls ---
        self.pommel_radius_slider = cmds.floatSliderGrp(label="Pommel Radius", field=True, min=0.05, max=1.0, value=self.sword.pommel_radius)

        cmds.separator(h=10, style="in")
        cmds.button(label=" Rebuild Sword", height=40, bgc=(0.3, 0.6, 0.3), command=self.rebuild_sword)
        cmds.button(label=" Delete Sword", height=30, bgc=(0.7, 0.3, 0.3), command=self.delete_sword)
        cmds.showWindow(self.window)

    def rebuild_sword(self, *args):
        """Read slider values and rebuild"""
        self.sword.blade_length = cmds.floatSliderGrp(self.blade_length_slider, q=True, value=True)
        self.sword.blade_width = cmds.floatSliderGrp(self.blade_width_slider, q=True, value=True)
        self.sword.blade_thickness = cmds.floatSliderGrp(self.blade_thickness_slider, q=True, value=True)
        self.sword.blade_taper = cmds.floatSliderGrp(self.blade_taper_slider, q=True, value=True)
        self.sword.handle_length = cmds.floatSliderGrp(self.handle_length_slider, q=True, value=True)
        self.sword.handle_radius = cmds.floatSliderGrp(self.handle_radius_slider, q=True, value=True)
        self.sword.pommel_radius = cmds.floatSliderGrp(self.pommel_radius_slider, q=True, value=True)

        self.sword.build()

    def delete_sword(self, *args):
        self.sword.clear_existing()
        print("🧹 Sword deleted.")


if __name__ == "__main__":
    SwordUI()

