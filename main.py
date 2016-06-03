#!/usr/bin/env python3

import gi
from gi.repository import WebKit2
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from gi.repository import GObject
import signal
import os
import threading


def with_args_test(*args):
	print ('this is a function with args, see the args:')
	for element in args:	
		print (element)

def no_args_test():
	print ('this is a function with no args')


def list_directory(): # List files on path of this script, show them on page
	path = os.getcwd()
	files_list = os.listdir(path)
	files_string = "<br>".join(files_list)
	script = 'document.getElementById("return").innerHTML = "'+files_string+'";'  
	
	m.webview.run_javascript(script, None, None, None)
	m.webview.run_javascript_finish(result)

	
def run_js_callback(context_view, parent_result, error): # Not used, maybe will fix the run_javascript_finish issue later
	
	result = context_view.run_javascript_finish(parent_result)
	if result is None:
		return
	
	value = result.get_value()
	print(value)

def start_gtk_thread(): # Create a GTK thread

	thread = threading.Thread(target=Gtk.main())
	thread.daemon = True
	thread.start()
	GObject.threads_init()

################################################################
# Classes
################################################################

class Window(): # Create general window
	def __init__(self):
		
		self.window = Gtk.Window()
		self.window.connect("delete-event", Gtk.main_quit)					
	
		#self.get_window().set_decorations(Gdk.WMDecoration.BORDER) # remove window decoration
	
		signal.signal(signal.SIGINT, signal.SIG_DFL)	

class Browser(Window): # Create a browser instance

	def __init__(self):
		super().__init__()
		self.webview = WebKit2.WebView()
		
		
	def load_uri(self, uri):
		self.webview.load_uri(uri)

	
class MainScreen(Browser): # Create the main app window

	def callback_uri(self, view, decision, decision_type): # Receive page function request e call functions
		
		if decision_type == 0:
			request = decision.get_request()			
			uri = request.get_uri()			
			
			scheme = uri[0:4]
			query = uri[7:]			
			has_args = query.find('%')			
									
			if scheme == 'clbk':
				decision.ignore()				
				
				if has_args != -1:
									
					args = query.split('%')						
					func = args[0]				
					del args[0] 
					
					nfunc = globals()[func]
					nfunc(args)
				else:
					func = query					
					nfunc = globals()[func]
					nfunc()										
				
			
	def __init__(self):
		super().__init__()
		
		#self.window.fullscreen()
		self.window.set_size_request(800, 600)		
		self.window.add(self.webview)
		self.window.show_all()
		self.webview.connect("decide-policy", self.callback_uri)
		
		self.mainUri = 'file://' + os.path.abspath('index.html')
		#print(self.mainUri)
		self.webview.load_uri(self.mainUri)
		
	
if  __name__ =='__main__':
	m = MainScreen()	
	start_gtk_thread()


