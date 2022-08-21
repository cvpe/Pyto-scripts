# based on Slider Pyto example
import pyto_ui as ui
from rubicon.objc import *
from time import sleep

slider = ui.Slider(0)

def did_slide(sender):
    print(sender.value)

def layout(sender):
    sleep(0.5)
    slider.set_value_with_animation(50)

view = ui.View()
view.background_color = ui.COLOR_SYSTEM_BACKGROUND
view.layout = layout

slider.maximum_value = 100
slider.width = 200
slider.center = (view.width/2, view.height/2)
slider.flex = [
    ui.FLEXIBLE_BOTTOM_MARGIN,
    ui.FLEXIBLE_TOP_MARGIN,
    ui.FLEXIBLE_LEFT_MARGIN,
    ui.FLEXIBLE_RIGHT_MARGIN
]
slider.action = did_slide

slider_objc = slider.__py_view__.managed
slider_objc.minimumValueImage = ui.image_with_system_name('volume.1')
slider_objc.maximumValueImage = ui.image_with_system_name('volume.3')
slider_objc.setThumbImage_forState_(ui.image_with_system_name('slowmo'), 0)	
view.add_subview(slider)

ui.show_view(view, ui.PRESENTATION_MODE_SHEET)
