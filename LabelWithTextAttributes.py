import pyto_ui as ui
from UIKit import *
from rubicon.objc import *

UIred = UIColor.redColor
strtext='This is a ui.Label with attributed strings!'
attrtext = ObjCClass('NSMutableAttributedString').alloc().initWithString_(strtext)
attrtext.addAttribute_value_range_('NSColor',UIred, NSRange(0,len(strtext)))

lbl=ui.Label()
lbl.frame = (0,0,320,20)
lbl.background_color=ui.COLOR_WHITE

lblobj = lbl.__py_view__.managed
lblobj.setAttributedText_(attrtext)

ui.show_view(lbl,ui.PRESENTATION_MODE_SHEET)
