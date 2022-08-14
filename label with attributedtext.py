# coding: utf-8
# experiments with attributed strings
# https://github.com/khilnani/pythonista-scripts/blob/master/thirdparty/ObjC%20Tools/Jsbain-objc_hacks/attribtxt.py

from rubicon.objc import *
import ctypes

NSMutableAttributedString=ObjCClass('NSMutableAttributedString')
NSFontAttributeName = 'NSFont'
UIFont=ObjCClass('UIFont')

attrtext = NSMutableAttributedString.alloc()
strtext='This is a ui.Label with attributed strings!'
attrtext.initWithString_(strtext)
#print(dir(attrtext))

sz=6.0
traits=0
for i in range(int(len(strtext)/2)):
   f=UIFont.systemFontOfSize_traits_(sz,traits)
   nsr=NSRange(i,1)
   attrtext.addAttribute_value_range_(NSFontAttributeName,f,nsr)
   sz+=2.5
   traits+=1
for i in range(int(len(strtext)/2),len(strtext)-1):
   f=UIFont.systemFontOfSize_traits_(sz,traits)
   nsr=NSRange(i,1)
   attrtext.addAttribute_value_range_(NSFontAttributeName,f,nsr)
   sz-=2.5
   traits+=1

import pyto_ui as ui
v=ui.View()
v.frame=(0,0,576,576)
v.background_color = ui.Color.rgb(0.7,0.7,0.7,1)
lbl=ui.Label()
bg_color='white'
v.add_subview(lbl)

lblobj=lbl.__py_view__.managed
lblobj.setAttributedText_(attrtext)
lbl.size_to_fit()
ui.show_view(v,ui.PRESENTATION_MODE_SHEET)
