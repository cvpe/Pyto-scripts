from UIKit import *
import mainthread

app = UIApplication.sharedApplication

@mainthread.mainthread
def disab():
  app.setIdleTimerDisabled_(True)

disab()
