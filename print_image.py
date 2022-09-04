from rubicon.objc import *
from mainthread import mainthread
import photos
import io

def pil2ui(pilimage):
    with io.BytesIO() as bIO:
      pilimage.save(bIO, 'PNG')
      uiimage = ObjCClass('UIImage').alloc().initWithData_(bIO.getvalue())
    return uiimage

@mainthread
def print_image_orientation(UIImages, orientation = 'P'):
	printController = ObjCClass('UIPrintInteractionController').sharedPrintController
	printInfo = ObjCClass('UIPrintInfo').printInfoWithDictionary_(None)
	# orientation P=Portrait L=Landscape
	printInfo.orientation = int(orientation[0].upper() == 'L')
	#printInfo.outputType = 0	# UIPrintInfoOutputGeneral
	# to avoid margins, we have to set output type as photo
	printInfo.outputType = 1	# UIPrintInfoOutputPhoto
	printController.printInfo = printInfo

	printController.setPrintingItems_(UIImages)
	printController.showsPageRange = True
	printController.showsPaperSelectionForLoadedPapers = True
	printController.showsNumberOfCopies = True
	#print(dir(printController))	
	printController.presentAnimated_completionHandler_(0, None)

pil = photos.pick_photo()
uiimage = pil2ui(pil)

print_image_orientation([uiimage])
