import pyto_ui as ui
from   SetTextFieldPad import SetTextFieldPad
from UIKit import *
import sharing

Version = 'V02.00'
with open('outline.versions', mode='rt', encoding='utf-8', errors="surrogateescape") as fil:	
  Versions = fil.read()
	
class Outliner(ui.View):
    
  def __init__(self):
    super().__init__()
        
    self.background_color = ui.COLOR_SYSTEM_BACKGROUND
    self.navigation_bar_hidden = True
    
    nb = 13
    for window in UIApplication.sharedApplication.windows:
      w = window.bounds.size.width
      break
    self.width = w
    dd = 4
    wb = (w - (nb+1)*dd)/nb
    if wb > 32:
      wb = 32
      dd = (w - wb*nb)/(nb+1)
    d = int(w/nb)
    y = 10 + wb
    x = dd
    b_close	= ui.Button()
    b_close.name = 'b_close'
    b_close.frame = (x,y,wb,wb)
    b_close.image = ui.image_with_system_name('x.circle')
    b_close.tint_color = ui.COLOR_SYSTEM_BLUE
    b_close.action = self.close_action
    self.add_subview(b_close)
        
    x = x + wb + dd
    b_version = ui.Button()
    b_version.name = 'b_version'
    b_version.frame = (x,y,wb,wb)
    b_version.title = Version
    fs = 12
    b_version.font = ui.Font('Menlo',fs)
    b_version.size_to_fit()
    w12 = b_version.width
    fs = 12 * wb/w12
    b_version.font = ui.Font('Menlo',fs)
    b_version.size_to_fit()
    b_version.height = wb
    b_version.tint_color = ui.COLOR_SYSTEM_GREEN
    b_version.action = self.button_version_action
    self.add_subview(b_version)

    x = x + wb + dd
    b_files = ui.Button()
    b_files.name = 'b_files'
    b_files.frame = (x,y,wb,wb)
    b_files.image = ui.image_with_system_name('folder')
    b_files.tint_color = ui.COLOR_SYSTEM_BLUE
    b_files.action = self.button_files_action
    self.add_subview(b_files)
    
    x = x + wb + dd				
    b_settings = ui.Button()
    b_settings. ame = 'b_settings'
    b_settings.frame = (x,y,wb,wb)
    b_settings.image = ui.image_with_system_name('gear')
    b_settings.tint_color = ui.COLOR_SYSTEM_BLUE
    #b_settings.action = self.button_settings_action
    self.add_subview(b_settings)
    
    x = x + wb + dd							
    b_filter = ui.Button()
    b_filter.name = 'b_filter'
    b_filter.frame = (x,y,wb,wb)
    #b_filter.action = self.button_filter_action
    b_filter.image = ui.image_with_system_name('slider.horizontal.3')
    b_filter.tint_color = ui.COLOR_SYSTEM_BLUE
    self.add_subview(b_filter)
    
    x = x + wb + dd							
    b_show = ui.Button()
    b_show.name = 'b_show'
    b_show.frame = (x,y,wb,wb)
    #b_show.action = self.button_show_action
    b_show.image = ui.image_with_system_name('eye')
    b_show.tint_color = ui.COLOR_SYSTEM_BLUE
    self.add_subview(b_show)
    
    x = x + wb + dd							
    b_undo = ui.Button()
    b_undo.name = 'undo_button'
    b_undo.frame = (x,y,wb,wb)
    #b_undo.action = self.button_undo_action
    b_undo.image = ui.image_with_system_name('arrow.uturn.left')
    b_undo.tint_color = ui.COLOR_SYSTEM_BLUE
    b_undo.enabled = False
    self.add_subview(b_undo)
		
    b_redo = ui.Button()
    b_redo.name ='redo_button'
    b_redo.frame = (x,10,wb,wb)
    #b_redo.action = self.button_redo_action
    b_redo.image = ui.image_with_system_name('arrow.uturn.right')
    b_redo.tint_color = ui.COLOR_SYSTEM_BLUE
    b_redo.enabled = False
    self.add_subview(b_redo)
		
    title = ui.Label()
    title.name = 'title'
    title.frame = (0,10,b_redo.x - 10,wb)
    title.font = ui.Font('Menlo',16)
    title.text_color = ui.COLOR_SYSTEM_GREEN
    title.text_alignment = ui.TEXT_ALIGNMENT_CENTER
    self.add_subview(title)
    title.text = 'test'
    
		
    x = x + wb + dd
    b_select = ui.Button()
    b_select.name = 'b_select'
    b_select.frame = (x,y,wb,wb)
    b_select.image = ui.image_with_system_name('checkmark.circle')
    b_select.tint_color = ui.COLOR_SYSTEM_BLUE
    #b_select.action = self.button_select_action
    self.add_subview(b_select)


    x = x + wb + dd		
    b_search = ui.Button()
    b_search.name = 'b_search'
    b_search.frame = (x,y,wb,wb)
    b_search.image = ui.image_with_system_name('magnifyingglass')
    b_search.tint_color = ui.COLOR_SYSTEM_BLUE
    b_search.action = self.button_search_action
    self.add_subview(b_search)

    x = x + wb + dd				
    b_fsize = ui.Button()
    b_fsize.name = 'b_fsize'
    b_fsize.frame = (x,y,wb,wb)
    b_fsize.image = ui.image_with_system_name('textformat.size')
    b_fsize.tint_color = ui.COLOR_SYSTEM_BLUE
    b_fsize.action = self.button_fsize_action
    self.add_subview(b_fsize)

    x = x + wb + dd				
    b_font = ui.Button()
    b_font.name = 'b_font'
    b_font.frame = (x,y,wb,wb)
    b_font.image = ui.image_with_system_name('f.circle')
    b_font.tint_color = ui.COLOR_SYSTEM_BLUE
    b_font.action = self.button_font_action
    self.add_subview(b_font)

    x = x + wb + dd				
    b_color = ui.Button()
    b_color.name = 'b_color'
    b_color.frame = (x,y,wb,wb)
    b_color.image = ui.image_with_system_name('paintpalette')
    b_color.tint_color = ui.COLOR_SYSTEM_BLUE
    b_color.action = self.button_color_action
    self.add_subview(b_color)
    self.outline_rgb = (1,0,0)
    #self.outline_color = UIColor.colorWithRed_green_blue_alpha_(self.outline_rgb[0], self.outline_rgb[1], self.outline_rgb[2], 1)

    x = x + wb + dd
    b_format = ui.Button()
    b_format.name = 'b_format'
    b_format.frame = (x,y,wb,wb)
    b_format.image = ui.image_with_system_name('list.number')
    b_format.tint_color = ui.COLOR_SYSTEM_BLUE
    #b_format.action = self.button_format_action
    self.add_subview(b_format)
    self.outline_format = 'decimal'
    self.first_level_has_outline = True

    sep = ui.Label()
    sep.name = 'sep'
    sep.frame = (0,y+wb,self.width,1)
    sep.background_color = ui.COLOR_LIGHT_GRAY
    self.add_subview(sep)
    
  def present_popover(self, view, menu= None, popover_location=None, hide_title_bar=False,  color=False, shield_height=False, shield=True):
    if shield:
      try:
        self.shield.hidden = False
      except:
        self.shield = ui.Button()
        self.shield.frame = (0,0,self.width, self.height)
        self.shield.background_color = ui.Color.rgb(1,1,0, 0.3)
        self.shield.hidden = False
        self.shield.action = self.shield_tapped
        self.add_subview(self.shield)
      if shield_height:
        self.shield.height = self['sep'].y
      else:
        self.shield.height = self.height
      self.shield.shield_height = self.shield.height
      self.shield.view = view
    if isinstance(view, ui.TableView):
      cells = []
      h = 0
      for item in menu:
        cell = ui.TableViewCell(ui.TABLE_VIEW_CELL_STYLE_SUBTITLE)
        cell.text_label.text = item
        cells.append(cell)
        h += cell.height
      view.frame = (0,0,330,h)
      # one section with empty title => no title row displayed
      view.sections = [ui.TableViewSection("", cells)]
      for section in view.sections:
        section.did_select_cell = self.selected
        self.select_view = view
    view.border_width = 1
    view.x, view.y = popover_location
    view.x = min(view.x, self.width - view.width - 2)
    view.y = min(view.y, self.height - view.height - 2)
    view.border_width = 1
    view.border_color = ui.COLOR_SYSTEM_BLUE
    view.corner_radius = 5
    self.add_subview(view)
    #view.bring_to_front()
    if isinstance(view, ui.TextField):
      view.become_first_responder()
                
  def selected(self, section, cell_index):
    print("selected: cell_index=", cell_index)
    TableViewSection = self.select_view.sections[0]
    cell = TableViewSection.cells[cell_index]
    option = cell.text_label.text
    print(option)
    if option == 'Open':
      filePicker = sharing.FilePicker()
      filePicker.file_types = ["public.item"]
      filePicker.allows_multiple_selection = False

      def files_picked() -> None:
        file = sharing.picked_files()
        print(file)

      filePicker.completion = files_picked
      sharing.pick_documents(filePicker)
      
    self.shield.hidden = True
    self.select_view.remove_from_superview()
    del self.select_view
	

  def shield_tapped(self, sender):
    # tap outside the popover view
    sender.hidden = True
    try:
      sender.view.remove_from_superview()
      if 'due date' in sender.view.name:
        self.set_due_date(sender.view)
      elif sender.view.name == 'select':
        self.select_action('cancel')
      elif sender.view.name == 'external_keyboard_keys_combinations':
        self.set_key_event_handlers()	
    except:
      pass
    self.selected_row = None
    
  def button_files_action(self,sender):
    if not isinstance(sender, ui.Button):
      act = sender
      #self.files_action(sender, act)
    else:
      x = sender.x + sender.width/2
      y = sender.y + sender.height
      sub_menu = ['Set current path', 'New', 'Open','Save', 'Rename']
      #if self.log == 'yes':
      #  sub_menu.append('Play log')
      sub_menu.append('Send text to app')
      sub_menu.append('Search')
      tv = ui.TableView()
      tv.name = 'files'
      self.present_popover(tv, menu=sub_menu, popover_location=(x,y),  hide_title_bar=True)

    
  def button_version_action(self,sender):
    x = sender.x + sender.width/2
    y = sender.y + sender.height
    tv = ui.TextView()
    tv.name = 'versions'
    tv.editable = False
    w = self.width  - 100
    h = self.height - 200
    tv.frame = (0,0,w-10,h-10)
    tv.font = ui.Font('Menlo',14)
    tv.text = Versions
    tv.name = 'Versions'
    self.present_popover(tv, popover_location=(x,y),hide_title_bar=True)
    
  def button_search_action(self,sender, simul_find=None):
    x = sender.x +sender.width/2
    y = sender.y + sender.height
    tf = ui.TextField()
    tf.name = 'search'
    tf.background_color = ui.Color.rgb(1,1,0, 0.3)
    tf.font = ui.Font('Menlo',18)
    tf.frame = (x,y,400,20)
    tf.placeholder = 'type text to be searched'
    if simul_find:
      tf.text = self.search_text_in_files
    else:
      tf.text = ''
    self.present_popover(tf, 'popover', popover_location=(x,y), hide_title_bar=True)
    #if simul_find:
    #  ui.delay(partial(self.textfield_did_change,tf), 0.2)
    
  def button_color_action(self,sender):
    rgb = ui.pick_color()
    print(rgb)
    
  def button_font_action(self,sender):
    font = ui.pick_font()
    print(font)
    
  def button_fsize_action(self,sender):
    x = sender.x +sender.width/2
    y = sender.y + sender.height
    tf = ui.TextField()
    SetTextFieldPad(tf)
    tf.name = 'font_size'
    tf.frame = (x,y,200,24)
    tf.placeholder = 'type font size in pixels'
    #tf.delegate = self
    #SetTextFieldPad(tf, pad_integer)
    #tf.text = str(self.font_size)
    self.present_popover(tf, 'popover',popover_location=(x,y),hide_title_bar=True)

  def close_action(self, sender):
    self.close()
        
def main():
  mv = Outliner()
  ui.show_view(mv,ui.PRESENTATION_MODE_FULLSCREEN)
	
if __name__ == '__main__':
  main()