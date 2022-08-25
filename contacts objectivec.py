#...... not working ........l.
from rubicon.objc import *
from Foundation import *

import Contacts

def main():

  # ObjectiveC contacts
  objc_contacts = {}
  CNContactStore = ObjCClass('CNContactStore').alloc()#.init()#.autorelease()
  print(dir(CNContactStore))
  
  # Once Pyto has been authorized, this code does not need to be executed
  #------- begin of commented
  import threading
  access_granted = threading.Event()
      
  @Block
  def handler_block(granted: ObjCInstance, err: ObjCInstance) -> None:
    print('handler_block called')
    access_granted.set()
  
  CNContactStore.requestAccessForEntityType_completionHandler_(0, handler_block)
  access_granted.wait()
  #------- end of commented

  
  CNContact = ObjCClass('CNContact')
  Containers = CNContactStore.containersMatchingPredicate_error_(None,None)
  containers = {}
  for Container in Containers:
    id = Container.identifier()
    containers[id] = Container
    #print(dir(Container))
    predicate = CNContact.predicateForContactsInContainerWithIdentifier_(id)
    # keys not exactly like in Apple doc
    # found a sample here https://github.com/tdamdouni/Pythonista/blob/master/contacts/Add%20Twitter%20Profile%20Picture%20to%20iOS%20Contacts.py
    predicate_contacts = CNContactStore.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, ['familyName','givenName','middleName'], None)
    for contact in predicate_contacts:
      # crash if attribute not in fetched contacts
      name = str(contact.givenName()) + '|' + str(contact.middleName()) + '|' + str(contact.familyName())
      print(name)
      cont_per_name = objc_contacts.setdefault(name, [])
      cont_per_name.append(id)


if __name__ == '__main__':
  main() 