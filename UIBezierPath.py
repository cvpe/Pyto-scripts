from rubicon.objc import *
import pyto_ui as ui
from math import pi

UIColor = ObjCClass('UIColor')
class MyClass(ui.View):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    path = ObjCClass('UIBezierPath').alloc().init()
    path.moveToPoint_((0, 0))
    path.lineToPoint_((0, 50))
    path.lineToPoint_((50, 50))
    path.addArcWithCenter_radius_startAngle_endAngle_clockwise_((50,25),25,pi/2,-pi/2,False)
    path.lineToPoint_((50, 0))
    path.closePath()

    shapeLayer = ObjCClass('CAShapeLayer').alloc().init()
    shapeLayer.path = path.CGPath
    shapeLayer.fillColor = UIColor.cyanColor.CGColor
    shapeLayer.strokeColor = UIColor.redColor.CGColor
    shapeLayer.lineWidth = 2.0
    shapeLayer.position = CGPoint(10, 10)
  
    self.__py_view__.managed.layer.addSublayer(shapeLayer)

if __name__ == '__main__':
  w, h = 400,300
  f = (0, 0, w, h)
  mc = MyClass()
  mc.frame = f
  mc.title = 'UIBezierPath: draw in ui.View'
  mc.background_color = ui.COLOR_LIGHT_GRAY
  ui.show_view(mc,ui.PRESENTATION_MODE_SHEET)