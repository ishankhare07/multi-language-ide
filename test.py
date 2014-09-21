from gi.repository import Gtk
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
			if Gtk.Buildable.get_name(widget) == 'lang_c' : self.language = 'c'
			elif Gtk.Buildable.get_name(widget) == 'lang_cpp' : self.language = 'c++'
			elif Gtk.Buildable.get_name(widget) == 'lang_java' : self.language = 'java'
			elif Gtk.Buildable.get_name(widget) == 'lang_py' : self.language = 'python'
			elif Gtk.Buildable.get_name(widget) == 'lang_ruby' : self.language = 'ruby'
			elif Gtk.Buildable.get_name(widget) == 'lang_perl' : self.language = 'perl'

	def on_compile_clicked(self,button):
		lang = self.language
		if lang in compilers:
			self.compile(compilers[lang][0],compilers[lang][1])
		elif lang in interpreters:
			self.interpret(interpreters[lang][0],interpreters[lang][1])
		else:
			print 'language not supported'

	def on_run_clicked(self,button):
		if not os.path.isfile(self.filename):
			self.on_compile_clicked('poof')
		if self.language == 'java':
			response = subprocess.call([self.language,self.filename],stdout=open('output','w'))
		elif self.language in interpreters:
			self.interpret(interpreters[self.language][0],interpreters[self.language][1])
		else:
			response = subprocess.call('./' + self.filename,stdout=open('output','w'))
		self.display()

	def compile(self,command,extension):
		code = self.retrieve_text(self.builder.get_object('code'))
		open(self.filename + extension,'wb').write(code)
		if command == 'javac':
			response = subprocess.call([command,self.filename +extension],stdout=open('output','w'))
		else:
			response = subprocess.call([command,self.filename + extension ,'-o',self.filename],stdout=open('output','w'))
		self.display()

	def interpret(self,command,extension):
		code = self.retrieve_text(self.builder.get_object('code'))
                open(self.filename + extension,'w').write(code)
		response = subprocess.call([command,self.filename + extension],stdout=open('output','w'))
		self.display()

	def retrieve_text(self,tv):
		buffer = tv.get_buffer()
		text = buffer.get_text(*buffer.get_bounds(),include_hidden_chars=True)
		return text

	def display(self):
		tv = self.builder.get_object('output')
		buffer = tv.get_buffer()
		text = self.retrieve_text(tv)
		new_text = open('output').read()
		buffer.set_text(text + new_text)

builder = Gtk.Builder()
builder.add_from_file('test.glade')
builder.connect_signals(handlers(builder))
window = builder.get_object('window1')
window.show_all()
Gtk.main()
