from gi.repository import Gtk
import subprocess,os,sys,thread,time

language = 'c'

compilers = {
	'c' : 'gcc',
	'c++' : 'g++',
	'java' : 'javac'
}

interpreters = {
	'python' : 'python',
	'ruby' : 'ruby',
	'perl' : 'perl'
}

class handlers:
	def __init__(self,b):
		self.builder = b
		self.filename = 'test'
		global language,compilers,interpreters

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

	def on_lang_c_toggled(self,button):
		print 'lang c toggled' + button

	def on_lang_cpp_activate(self,button):
		print 'lang c activated'

	def on_compile_clicked(self,button):
		lang = language
		if lang in compilers:
			self.compile(compilers[lang],'test')
		elif lang in interpreters:
			self.interpret(interpreter[lang],'test')
		else:
			print 'language not supported'

	def on_run_clicked(self,button):
		if not os.path.isfile(self.filename):
			self.on_compile_clicked('poof')
		response = subprocess.call('./' + self.filename,stdout=open('output','w'))
		self.display()

	def compile(self,lang,filename):
		code = self.retrieve_text(self.builder.get_object('code'))
		open(self.filename + '.c','wb').write(code)
		response = subprocess.call([lang,self.filename + '.c','-o',self.filename],stdout=open('output','w'))
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
