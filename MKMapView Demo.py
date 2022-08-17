# based on Pythonista example https://gist.github.com/omz/451a6685fddcf8ccdfc5
from rubicon.objc import *
from ctypes import *
import pyto_ui as ui
import mainthread
import location
import time

class MapView (ui.View):
  @mainthread.mainthread
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.title = 'MKMapView'
  
    maptype_button = ui.ButtonItem('satellite')
    maptype_button.action = self.maptype_button_action
    self.button_items = [maptype_button]
    
    MKMapView = ObjCClass('MKMapView')
    frame = CGRect(CGPoint(0, 0), CGSize(self.width, self.height))
    self.mk_map_view = MKMapView.alloc().initWithFrame_(frame)
    self.mk_map_view.mapType = 0 # standard
    flex_width, flex_height = (1<<1), (1<<4)
    self.mk_map_view.setAutoresizingMask_(flex_width|flex_height)
    self_objc = self.__py_view__.managed
    self_objc.addSubview_(self.mk_map_view)
    self.mk_map_view.release()
    
  def maptype_button_action(self, sender):
    self.mk_map_view.mapType += 1
    if self.mk_map_view.mapType > 2:
      self.mk_map_view.mapType = 0
    sender.title = ['satellite', 'hybrid', 'standard'][self.mk_map_view.mapType]
  
  @mainthread.mainthread
  def add_pin(self, lat, lon, title, subtitle=None, select=False):
    '''Add a pin annotation to the map'''
    MKPointAnnotation = ObjCClass('MKPointAnnotation')
    annotation = MKPointAnnotation.alloc().init().autorelease()
    annotation.setTitle_(title)
    if subtitle:
      annotation.setSubtitle_(subtitle)
    annotation.coordinate = (lat,lon)
    self.mk_map_view.addAnnotation_(annotation)
    if select:
      self.mk_map_view.selectAnnotation_animated_(annotation, True)

def main():
  # Create and present a MapView:
  v = MapView()
  v.frame=(0, 0, 600, 600)
  
  location.start_updating()
  time.sleep(1)
  loc = location.get_location()
  #location.stop_updating()
  #print(loc)
  if loc:
    lat, lon = loc[1], loc[0]
    v.add_pin(lat, lon, 'Current Location', str((lat, lon)))
    
  ui.show_view(v,ui.PRESENTATION_MODE_SHEET)
	
if __name__ == '__main__':
  main()