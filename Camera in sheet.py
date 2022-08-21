# https://github.com/jsbain/objc_hacks/blob/master/live_camera_view.py
from rubicon.objc import *
import pyto_ui as ui
from UIKit import *

class LiveCameraView(ui.View):
  def __init__(self,device=0, *args, **kwargs):
    # device =  0 = camera back
    #           1 = camera front
    #           2 = micro
    ui.View.__init__(self,*args,**kwargs)
    self._session=ObjCClass('AVCaptureSession').alloc().init()
    self._session.setSessionPreset_('AVCaptureSessionPresetHigh');
    inputDevices=ObjCClass('AVCaptureDevice').devices()
    #print(inputDevices)
    self._inputDevice=inputDevices[device]
    deviceInput = ObjCClass('AVCaptureDeviceInput').deviceInputWithDevice_error_(self._inputDevice, None);
    if self._session.canAddInput_(deviceInput):
      self._session.addInput_(deviceInput)
    self._previewLayer = ObjCClass('AVCaptureVideoPreviewLayer').alloc().initWithSession_(self._session)
    self._previewLayer.setVideoGravity_( 
         'AVLayerVideoGravityResizeAspectFill')
    rootLayer = self.__py_view__.managed.layer
    rootLayer.setMasksToBounds_(True)
    self._previewLayer.setFrame_(CGRect(CGPoint(-70, 0), CGSize(self.height,self.height)))
    rootLayer.insertSublayer_atIndex_(self._previewLayer,0)
    self._session.startRunning()
      
  def will_close(self):
    self._session.stopRunning()
      
  def layout(self):
    if not self._session.isRunning():
      self._session.startRunning()

rootview = LiveCameraView()
app = ObjCClass('UIApplication').sharedApplication.keyWindow
for window in UIApplication.sharedApplication.windows:
  wi = window.bounds.size.width
  hi = window.bounds.size.height
  break
w = 400
h = w * hi/wi
rootview.frame = (0,0,w,h)
rootview.title = 'Camera in Sheet'
ui.show_view(rootview,ui.PRESENTATION_MODE_SHEET)