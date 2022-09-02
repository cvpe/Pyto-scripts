from rubicon.objc import *
import pyto_ui as ui

UIColor = ObjCClass('UIColor')

view = ui.View()
view.title = 'shadow'
view.frame=(0,0,200,200)
box = ui.View()
box.frame=(0,0,100,100)

view.background_color = ui.COLOR_WHITE
background_color = 'white'
box.background_color = ui.COLOR_RED
box.center = view.center

view.add_subview(box)

box_pntr = box.__py_view__.managed

box_pntr.layer.setMasksToBounds_(False)
box_pntr.layer.setCornerRadius_(6)
box_pntr.layer.setBorderColor_(UIColor.cyanColor.CGColor)
box_pntr.layer.setShadowColor_(UIColor.blueColor.CGColor)
box_pntr.layer.setBorderWidth_(3)
box_pntr.layer.setShadowRadius_(10)
box_pntr.layer.setShadowOffset_(CGSize(0,0))
box_pntr.layer.setShadowOpacity_(1.0)

ui.show_view(view,ui.PRESENTATION_MODE_SHEET)