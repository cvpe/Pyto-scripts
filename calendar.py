import datetime

from rubicon.objc import Block, ObjCClass, ObjCInstance

def main():
  
  # EKEventStore = calendar database
  store = ObjCClass('EKEventStore').alloc().init()
  
  # Once Pyto has been authorized, this code does not need to be executed
  #------- begin of commented
  import threading
  access_granted = threading.Event()
      
  @Block
  def handler_block(granted: ObjCInstance, err: ObjCInstance) -> None:
    print('completion called')
    access_granted.set()
  
  store.requestAccessToEntityType_completion_(0, handler_block)
  access_granted.wait()
  #------- end of commented
	
  # Convert string yyyymmdd to NSdate
  dateFormat = ObjCClass('NSDateFormatter').alloc().init()
  dateFormat.setDateFormat_('yyyyMMdd HH:mm')

  date1 = dateFormat.dateFromString_('20200101 00:01') 
  date2 = dateFormat.dateFromString_('20201231 23:59')  

  calendars_array = [calendar for calendar in store.calendars if str(calendar.title) == 'Sorties']
  print(store.calendars)
  predicate = store.predicateForEventsWithStartDate_endDate_calendars_(date1, date2, calendars_array)
  events = store.eventsMatchingPredicate_(predicate)
  for event in events:
    print(event.title)
		
  
	


if __name__ == '__main__':
  main()
