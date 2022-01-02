import pyto_ui as ui
from math import cos,sin,pi
from random import random
from UIKit import *
#from rubicon.objc import *

def SetTextFieldPad(tf, pad=None):
  if not pad:
    pad = [{'key':'1'},{'key':'2'},{'key':'3'},
		{'key':'back space','icon':'delete.left'},
		{'key':'new row'},
		{'key':'4'},{'key':'5'},{'key':'6'},
		{'key':'delete','icon':'delete.right'},
		{'key':'new row'},
		{'key':'7'},{'key':'8'},{'key':'9'},
		{'key':'return', 'icon':'return'},
		{'key':'new row'},    
		{'key':'nul'},{'key':'0'},{'key':'nul'}]
  tfo = tf.__py_view__.managed
	
  def key_pressed(sender):

			if sender.title == 'test':
				return
			tfb = sender.TextField
			tfobjc = tfb.__py_view__.managed
			cursor = tfobjc.offsetFromPosition_toPosition_(tfobjc.beginningOfDocument, tfobjc.selectedTextRange.start)
			if sender.name == 'delete':
				if cursor <= (len(tfb.text)-1):
					tfb.text = tfb.text[:cursor] + tfb.text[cursor+1:]
			elif sender.name == 'back space':
				if cursor > 0:
					#if tfb.text != '':
					tfb.text = tfb.text[:cursor-1] + tfb.text[cursor:]
					cursor = cursor - 1
			elif sender.name == 'return':
				tfb.resign_first_responder()
				return
			else:
				tfb.text = tfb.text[:cursor] + sender.title + tfb.text[cursor:]
				cursor = cursor + 1
				
			# set cursor
			cursor_position = tfobjc.positionFromPosition_offset_(tfobjc.beginningOfDocument, cursor)
			tfobjc.selectedTextRange = tfobjc.textRangeFromPosition_toPosition_(cursor_position, cursor_position)

  # design your keyboard
  # pad = [{key='functionnality',title='title',icon='icon'},...]
  #		new row => new row
  #		nul => no key
  #		back space => left delete
  #		delete => right delete
  #		return => discard the keyboard
  #   other => append the character
	
  # count the maximum width of rows
  row_max_length = 0
  row_length = 0
  for pad_elem in pad:
    if pad_elem['key'] == 'new row':
      if row_length > row_max_length:
        row_max_length = row_length
      row_length = 0		
    else:
      row_length = row_length + 1
  if row_length > row_max_length:
    row_max_length = row_length

  v = ui.View()
  for window in UIApplication.sharedApplication.windows:
    v.width = window.bounds.size.width
    break
  db = 50
  dd = 10
  x0 = (v.width-row_max_length*db-(row_max_length-1)*dd)/2
  x = x0
  y = dd

  for pad_elem in pad:
    if pad_elem['key'] == 'new row':
      y = y + db + dd
      x = x0
    elif pad_elem['key'] == 'nul':			
      x = x + db + dd
    else:			
      b = ui.Button()
      b.name = pad_elem['key']
      b.background_color = ui.Color.rgb(1,1,1,1)
      b.tint_color = ui.Color.rgb(0,0,0,1)
      b.corner_radius = 10 
      b.title = ''
      b.font = ui.Font('Menlo',32)
      if 'icon' in pad_elem:
        b.image = ui.image_with_system_name(pad_elem['icon'])
      elif 'title' not in pad_elem:
        b.title = pad_elem['key']
      if 'title' in pad_elem:
        b.title = pad_elem['title']
      b.frame = (x,y,db,db)
      b.TextField = tf # store tf as key attribute  needed when pressed
      if 'action' in pad_elem:
        b.action = pad_elem['action']
      else:
        b.action = key_pressed
      v.add_subview(b)
      x = x + db + dd
  y = y + db + dd
  
  app = UIApplication.sharedApplication.keyWindow
  bot = app.safeAreaInsets.bottom	

  v.height = y + bot

  # view of keyboard
  vo = v.__py_view__.managed
  tfo.setInputView_(vo)
	
  # color of cursor and selected text
  tfo.tintColor = UIColor.redColor.colorWithAlphaComponent(0.5)

  tfo.inputAssistantItem.setLeadingBarButtonGroups(None)
  tfo.inputAssistantItem.setTrailingBarButtonGroups(None)

if __name__ == '__main__':		
  mv = ui.View()
  mv.frame = (0,0,400,400)
  mv.background_color = ui.Color.rgb(0.5,0.5,0.5,1)
  tf = ui.TextField()
  tf.frame = (10,10,100,30)
  SetTextFieldPad(tf)
  tf.text = ''
  tf.become_first_responder()
  mv.add_subview(tf)
  ui.show_view(mv,ui.PRESENTATION_MODE_SHEET)
