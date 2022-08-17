from rubicon.objc import *
import pyto_ui as ui

def GetNavigationBar(ui_view):
	# ui.View has to be first presented
	vo = ui_view.__py_view__.managed
	while True:
		super = vo.superview()
		for sv in super.subviews():
			if str(sv).startswith('<UINavigationBar'):
				nb = sv
				return nb
		vo = super
	return None

def did_appear():
  #print('did_appear called')
  nb = GetNavigationBar(v)
  nb.backgroundColor = ObjCClass('UIColor').redColor

if __name__ == '__main__':
  v = ui.View()
  v.title = 'Set NavigationBar color'
  v.frame = (0,0,400,400)
  v.background_color = ui.COLOR_WHITE
  v.did_appear = did_appear
  ui.show_view(v,ui.PRESENTATION_MODE_SHEET)