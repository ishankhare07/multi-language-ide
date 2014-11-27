from gi.repository import Gtk, GtkSource, GObject
import subprocess,os,sys,thread,time

compilers = {
	'c' : ['gcc','.c'],
	'c++' : ['g++','.cpp'],
	'java' : ['javac','.java']
}

interpreters = {
	'python' : ['python','.py'],
	'ruby' : ['ruby','.rb'],
	'perl' : ['perl','.pl']
}

class handlers:
	def __init__(self,b):
		self.builder = b
		self.filename = 'myfile'
		self.language = 'c'

		self.buffer = self.builder.get_object('code').get_buffer()
		self.lang_manager = GtkSource.LanguageManager()
		self.buffer.set_language(self.lang_manager.get_language('c'))

		global compilers,interpreters

	def on_delete(self,*args):
		Gtk.main_quit(args)

	def toggle_bar(self,button):
		paned = self.builder.get_object('paned1')
		if paned.get_position() > 0:
			pos = 100
			while pos >= 0:
				paned.set_position(pos)
				time.sleep(0.005)
				pos-=1
			button.set_label('Show')
		else:
			pos = 0
			while pos <= 100:
				paned.set_position(pos)
				time.sleep(.005)
				pos+=1
			button.set_label('Hide')

	def on_options_clicked(self,button):
		thread.start_new_thread(self.toggle_bar,(self.builder.get_object('options'),))

	def toggle_lang(self,widget):
		if widget.get_active():
			if Gtk.Buildable.get_name(widget) == 'lang_c' :
				self.language = 'c'
				self.buffer.set_language(self.lang_manager.get_language('c'))
			elif Gtk.Buildable.get_name(widget) == 'lang_cpp' :
				self.language = 'cpp'
                                self.buffer.set_language(self.lang_manager.get_language('c++'))
			elif Gtk.Buildable.get_name(widget) == 'lang_java' :
				self.language = 'java'
                                self.buffer.set_language(self.lang_manager.get_language('java'))
			elif Gtk.Buildable.get_name(widget) == 'lang_py' :
				self.language = 'python'
                                self.buffer.set_language(self.lang_manager.get_language('python'))
			elif Gtk.Buildable.get_name(widget) == 'lang_ruby' :
				self.language = 'ruby'
                                self.buffer.set_language(self.lang_manager.get_language('ruby'))
			elif Gtk.Buildable.get_name(widget) == 'lang_perl' :
				self.language = 'perl'
                                self.buffer.set_language(self.lang_manager.get_language('perl'))

	def on_run_clicked(self,button):
		if not os.path.isfile(self.filename) and self.language in compilers:
			self.on_compile_clicked('poof')
		if self.language == 'java':
			response = subprocess.call([self.language,self.filename],stdout=open('output','w'),stderr=open('output','w'))
			self.display()
		elif self.language in interpreters:
			print 'calling interpret from run'
			self.interpret(interpreters[self.language][0],interpreters[self.language][1])
		else:
			print 'executing'
			response = subprocess.call('./' + self.filename,stderr=open('output','w'),stdout=open('output','w'))
			self.display()

	def on_compile_clicked(self,btn):
		#lang = self.language
		if self.language in compilers:
			self.compile(compilers[self.language][0],compilers[self.language][1])
		elif self.language in interpreters:
			print 'calling interpret from compile'
			self.interpret(interpreters[self.language][0],interpreters[self.language][1])
		else:
			print 'language not supported'

	def compile(self,command,extension):
		code = self.retrieve_text(self.builder.get_object('code'))
		open(self.filename + extension,'wb').write(code)
		if command == 'javac':
			print command,self.filename+extension
			response = subprocess.call([command,self.filename +extension],stderr=open('output','w'),stdout=open('output','w'))
		else:
			response = subprocess.call([command,self.filename + extension ,'-o',self.filename],stderr=open('output','w'),stdout=open('output','w'))
		self.display()

	def interpret(self,command,extension):
		print 'interpret called'
		code = self.retrieve_text(self.builder.get_object('code'))
                open(self.filename + extension,'w').write(code)
		response = subprocess.call([command,self.filename + extension],stderr=open('output','w'),stdout=open('output','w'))
		self.display()

	def retrieve_text(self,tv):
		buffer = tv.get_buffer()
		text = buffer.get_text(*buffer.get_bounds(),include_hidden_chars=True)
		return text

	def display(self):
		print 'executing display'
		tv = self.builder.get_object('output')
		buffer = tv.get_buffer()
		text = self.retrieve_text(tv)
		new_text = open('output').read()
		buffer.set_text(text + new_text)

builder = Gtk.Builder()
GObject.type_register(GtkSource.View)
builder.add_from_file('test.glade')
builder.connect_signals(handlers(builder))
window = builder.get_object('window1')
window.show_all()
Gtk.main()
