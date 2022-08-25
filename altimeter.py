# coding: utf-8
from rubicon.objc import Block, ObjCClass, ObjCInstance, py_from_ns
from rubicon.objc.runtime import objc_id

pressure = None

# solution with @Block
@Block
def handlerb(altitudeData:ObjCInstance, err:ObjCInstance) -> None:
   print(ObjCInstance(altitudeData).pressure)


# solution with block() function
#def handler(_data) -> None:
#    nspressure = ObjCInstance(_data).pressure
#    global pressure
#    pressure = py_from_ns(nspressure)

#handler_block = Block(handler, None, (objc_id))

def get_pressure():
    CMAltimeter = ObjCClass('CMAltimeter')
    NSOperationQueue = ObjCClass('NSOperationQueue')
    if not CMAltimeter.isRelativeAltitudeAvailable():
        print('This device has no barometer.')
        return
    altimeter = CMAltimeter.new()
    main_q = NSOperationQueue.mainQueue
    #altimeter.startRelativeAltitudeUpdatesToQueue_withHandler_(main_q, handler_block)
    altimeter.startRelativeAltitudeUpdatesToQueue_withHandler_(main_q, handlerb)
    print('Started altitude updates.')
    try:
        while pressure is None:
            pass
    finally:
        altimeter.stopRelativeAltitudeUpdates()
        print('Updates stopped.')
        return pressure

if __name__ == '__main__':
    result = get_pressure()
    print(result)
    del pressure