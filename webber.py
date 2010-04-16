# -*- coding: iso-8859-1 -*-
import sys, os, optparse, fnmatch, stat, re, time, codecs
from config import Holder



###############################################################################
#
#  Global variables
#

__all__ = [
	# Globals
	"cfg",          # configuration from webber.ini
	"directories",  # global hash of directories, by rel_path
	"files",        # global hash of files, by rel_path
	"functions",    # all exported template functions

	# Functions
	"set_hook",     # decorator for hook-functions
	"set_macro",    # define macro
	"set_function", # define functions for the template
	"get_file_for",
	"get_link_from",
	"get_current_file", # because mako-called functions cannot access the
	                # current File object
	"get_program_directory",
	"log",          # misc logging functions
	"info",
	"warning",
	"error",
	]



###############################################################################
#
#  Configuration class
#

cfg = Holder()



directories = {}

class Directory(Holder):
	"""This stores per-directory information. Each file has a pointer
	to a directory object."""

	def __init__(self, **kw):
		Holder.__init__(self, **kw)
		directories[kw["rel_path"]] = self


files = {}
current_file = None

class File(Holder):
	"""This stores file information."""

	def __init__(self, **kw):
		Holder.__init__(self, **kw)
		files[kw["rel_path"]] = self
		self.render = None
		self.contents = None
		mtime = os.stat(self.path)[stat.ST_MTIME]
		self.mtime = mtime
		self.ctime = mtime
		#print self.keys()

	reKeywords = re.compile(r'(\S+)\s*:\s*(.*)')

	def read(self, terminate_line=""):
		f = codecs.open(self.path, "r", self.input_encoding)

		# Read keywords
		read_keywords = True
		txt = []
		for s in f.readlines():
			if read_keywords:
				s = s.strip()
				#print "kwd:", s
				if s == terminate_line:
					read_keywords = False
					continue

				m = self.reKeywords.match(s)
				if not m:
					warning("%s: wrong 'key: value' line '%s'" % (self.rel_path, s))
					break
				key = m.group(1).lower()
				val = m.group(2)

				if key == "mtime":
					val = iso_to_time(val)

				if key == "ctime":
					val = iso_to_time(val)

				if key == "title":
					if not self.has_key("linktitle"):
						self["linktitle"] = val

				#print self.rel_path, key, val
				self[key] = val

				continue
			#print "txt:", s.rstrip().encode("iso-8859-1")
			txt.append(s)

		# Warn about a bogus time entries
		if self.mtime < self.ctime:
			log('%s: modification time cannot be before creation time' % self.rel_path)
			self.ctime = self.mtime

		# Warn about long titles / long linktitles
		if len(self.linktitle) > 20:
			log('%s: define a shorter linktitle' % self.rel_path)

		self.contents = "".join(txt)


_get_file_for_cache = {}
def get_file_for(name):
	"""webber.files is an hash of File objects, but keyed on the real file name.
	This function returns a File object for a specific linktitle."""
	
	try:
		return _get_file_for_cache[name]
	except:
		pass

	#print "get_file_for:", name
	for s in files:
		f = files[s]
		try:
			if f.linktitle == name:
				#print "  via linktitle:", s
				_get_file_for_cache[name] = f
				return f
		except:
			pass
		# Allow exact match as well
		if s == name:
			#print "  exact:", s
			_get_file_for_cache[name] = f
			return f
	#print "  not found"


def relpath(base_path, target):
	"""\
	Return a relative path to the target from either the current directory
	or an optional base directory.

	Base can be a directory specified either as absolute or relative
	to current directory."""
	# Code from http://code.activestate.com/recipes/302594/

	def commonpath(a, b):
		"""Returns the longest common to 'paths' path.

		Unlike the strange commonprefix:
		- this returns valid path
		- accepts only two arguments
		"""
		if a == b:
			return a
		while len(a) > 0:
			if a == b:
				return a
			if len(a) > len(b):
				a = os.path.dirname(a)
			else:
				b = os.path.dirname(b)
		return None

	base_path = os.path.normpath(os.path.normcase(base_path))
	target = os.path.normpath(os.path.normcase(target))

	if base_path == target:
		return '.'

	# On the windows platform the target may be on a different drive.
	if os.path.splitdrive(base_path)[0] != os.path.splitdrive(target)[0]:
		return None

	common_path_len = len(commonpath(base_path, target))

	# If there's no common prefix decrease common_path_len should be less by 1
	base_drv, base_dir = os.path.splitdrive(base_path)
	if common_path_len == len(base_drv) + 1:
		common_path_len -= 1

	# if base_path is root directory - no directories up
	if base_dir == os.sep:
		dirs_up = 0
	else:
		dirs_up = base_path[common_path_len:].count(os.sep)

	ret = os.sep.join([os.pardir] * dirs_up)
	if len(target) > common_path_len:
		ret = os.path.join(ret, target[common_path_len + 1:])

	return ret


def get_link_from(source, dest):
	#print "get_link_from", source, dest
	#print source
	if not isinstance(source, File):
		source = get_file_for(source)
	if not source:
		print "NO SOURCE"
		return "."
	if not isinstance(dest, File):
		dest = get_file_for(dest)
	if not dest:
		print "NO DEST"
		return "."
	rel_path = relpath(directories[source.direc].abs_path, directories[dest.direc].abs_path)
	try:
		out_path = dest.out_path
	except:
		out_path = ""
	#print dest
	rel_path = os.path.join(rel_path, os.path.split(out_path)[1])
	if rel_path.startswith("./"):
		rel_path = rel_path[2:]
	#print "  from path:", source.out_path
	#print "  to path:  ", out_path
	#print "  rel path: ", rel_path
	return rel_path



###############################################################################
#
#  Utility functions
#


def get_program_directory():
	"""Return the path to the directory containing the build software."""
	import __main__
	path = os.path.dirname(__main__.__file__)
	if path == "":
		path = os.getcwd()
	return path



###############################################################################
#
#  Logging
#
#	1    Error
#	2    Warning
#	3    Info
#	4    Log
#	5... Debug
#
def log(s, level=4):
	if level > 4:
		indent = " " * (level-4)
	else:
		indent = ""
	if level <= cfg.verbose:
		print "%s%s" % (indent, s)

def error(s):
	log("error: %s" % s, 1)

def warning(s):
	log("warning: %s" % s, 2)

def info(s):
	log("info: %s" % s, 3)



###############################################################################
#
#  Hooks and plugins
#


# IkiWiki does something like this:
# At startup:
#	getopt               modify ARGV
#	checkconfig          check configuration
#	refresh              allow plugins to build source files
# While scanning files:
#	needsbuild           detect if page needs to be rebuild
#	filter               arbitrary changes
#	scan                 collect metadata
# While rendering files:
#	filter               arbitrary changes
#	preprocess           execute macros
#	linkify              change wikilinks into links
#	htmlize              turns text into html
#	sanitize             sanitize html
#	templatefile         allows changing of the template on a per-file basis
#	pagetemplate         fill template with page
#	format               similar to sanitize, but act on whole page body
# At the end:
#	savestate            plugins can save their state
#
#
# We do something like this:
#
# At startup:
#	addoptions           allow plugins to add command-line options
#	checkconfig          check configuration
#	start                
# While reading files:
#	read                 ask any reader (plugins!) to read the file
#	filter               ask anybody to filter the contents
# While scanning files:
#	scan                 called per file, let plugins act on file data
#	scan_done            Allows post-processing of scanned data
# While rendering files:
#	htmlize              turns text into html-part
#	linkify              convert link macros to HTML
#	pagetemplate         ask template engine (plugin!) to generate HTML out
#	                     of template and body part
# At the end:
#	finish
#
# For more info, see plugins/skeleton.py
#


hooks = {}

def load_plugins():
	"""Loads all plugins in the plugins directory."""
	sys.path.append(os.path.join(get_program_directory(), "plugins"))
	for s in cfg.plugins:
		#print "import:", s
		try:
			exec "import %s" % s
		except:
			print "Could not import plugin '%s'" % s
			sys.exit(1)


def set_hook(name, last=False):
	"""This is a decorator, used for mostly plugins, which can append the
	attached function to some hook"""
	#print "set_hook, name", name
	def inside_set_hook(func):
		#print "inside_set_hook, function", func.__name__, "name", name, "last", last
		if not hooks.has_key(name):
			hooks[name] = []
		func.last = last
		hooks[name].append(func)
		return func
	return inside_set_hook


def run_hooks(name, **kw):
	"""This runs hooks that are marked with @set_hook("name")"""
	#print "run_hooks:", name
	args = Holder(**kw)
	args.setDefault("stop_if_result", False)
	args.setDefault("return_holder", True)

	# Need to wrap this because run_hooks() is called before
	# cfg.verbose has been set
	try:
		log("running hook '%s'" % name, level=7)
	except:
		AttributeError

	if hooks.has_key(name):
		delay = []
		for func in hooks[name]:
			if func.last:
				delay.append(func)
				continue
			#print "running hook:", func
			res = func(args)
			if args.stop_if_result and res:
				return res
		for func in delay:
			#print "running hook (last):", func.__name__
			res = func(args)
			if args.stop_if_result and res:
				return res
	else:
		return None
	if args.return_holder:
		return args
	else:
		return res


macros = {}

def set_macro(name):
	"""This is a decorator, used for mark executable macros"""

	#print "set_macro, name", name
	def inside_set_macro(func):
		#print "inside_set_macro, function", func.__name__, "name", name
		if macros.has_key(name):
			error("macro %s already defined" % name)
			return
		macros[name] = func
		return func
	return inside_set_macro

functions = {}

def set_function(name):
	"""This is a decorator, used for mark executable functions"""

	#print "set_function, name", name
	def inside_set_function(func):
		#print "inside_set_function, function", func.__name__, "name", name
		if functions.has_key(name):
			error("function %s already defined" % name)
			return
		functions[name] = func
		return func
	return inside_set_function


def iso_to_time(val):
	try:
		t = time.strptime(val, "%Y-%m-%d %H:%M")
	except ValueError:
		try:
			t = time.strptime(val, "%Y-%m-%d")
		except ValueError:
			warning("wrong ISO format in '%s'" % val)
	return int(time.mktime(t))

@set_function("format_date")
def format_date(timestamp):
	return time.strftime(cfg.date_format, time.localtime(timestamp))

@set_function("get_time")
def get_time():
	return format_date(time.time())

@set_function("get_current_file")
def get_current_file():
	return current_file





###############################################################################
#
#  File reading
#

def read_file(direc, file):
	"""
	Ask if some reader wants to read this file. If that happens,
	and the reader reads the file in, the contents is also filtered.

	The result is stored in file.contents

	@param direc: directory the file is in
	@type direc: a L{Directory} object
	@param file: file to process
	@type file: a L{File} object
	"""

	contents = run_hooks("read",
		direc=direc,
		file=file,
		stop_if_result=True,
		return_holder=False)
	if not contents:
		return

	log("filtering file %s" % file.rel_path, level=6)
	file.contents = contents
	res = run_hooks("filter",
		direc=direc,
		file=file)


def walk_tree(dirpath):
	"""
	Walks the directory rooted at 'path', and calls func(dirpath, filenames)
	for each directory.

	@param dirpath: starting directory
	@type dirpath: string
	@param func: function to call for found dirs/files
	@type func: function(dirpath, filenames)
	"""

	info("Reading files ...")

	def walk(dirpath):
		#print "walk", dirpath
		rel_path = dirpath[len(cfg.in_dir):]
		direc = Directory(rel_path=rel_path, abs_path=dirpath)
		direc.inheritFrom(cfg)

		if not rel_path: rel_path = "."
		log("reading directory %s" % rel_path, level=5)

		for s in os.listdir(dirpath):
			full_path = os.path.join(dirpath, s)
			ok = True
			if os.path.isdir(full_path):
				for e in cfg.exclude_dir:
					if fnmatch.fnmatchcase(s, e):
						log("ignoring directory %s" % s, level=7)
						ok = False
						break
				if ok:
					#print "DIR", s
					walk(full_path)
			if os.path.isfile(full_path):
				for e in cfg.exclude_files:
					if fnmatch.fnmatchcase(s, e):
						log("ignoring file %s" % s, level=7)
						ok = False
						break
				if ok:
					#print "FILE", s
					rel_path = relpath(cfg.in_dir, full_path)
					# Allow paths to be specified in exclude_files:
					for e in cfg.exclude_files:
						if fnmatch.fnmatch(rel_path, e):
							log("ignoring file %s" % rel_path, level=7)
							ok = False
							break
				if ok:
					log("reading file %s" % rel_path, level=5)
					file = File(
						path = full_path,
						rel_path = rel_path,
						direc = direc.rel_path
					)
					file.inheritFrom(direc)
					read_file(direc, file)
						
	walk(dirpath)



###############################################################################
#
#  Rendering
#

reMacro = re.compile(r'''
	\[\[\!                  # Begin of macro
	\s*
	([^\s\]]+)              # Macro name
	(?:
		\s+                 # optional space
        ([^\]]+)            # optional argumens
	)?
	\]\]                    # End of macro
	''', re.VERBOSE)
reMacroArgs = re.compile(r'''
	([-_\w]+)				# parameter name
	(?:
		\s*
		=
		\s*
		(?:
			"([^"]*)"       # single-quoted
		|
			(\S+)           # unquoted
		)
	)?
	''', re.VERBOSE)

def run_macros(file, contents):
	def do_macro(m):
		name = m.group(1)
		#print "\nname:", name
		kw = {'name':name}
		if m.group(2):
			#print "args:", m.group(2)
			for m2 in reMacroArgs.finditer(m.group(2)):
				#print "  param:", m2.group(1)
				#print "  arg:", m2.group(3) or m2.group(2)
				kw[m2.group(1)] = m2.group(3) or m2.group(2)
		if macros.has_key(name):
			kw["file"] = file
			f = macros[name]
			s = f(kw)
			if isinstance(s, unicode):
				s = s.encode("utf-8")
			return s
		else:
			error("macro %s not defined" % name)
	s = reMacro.sub(do_macro, contents)
	#print s
	return s
	

def scan_files():
	info("Scanning files ...")

	for s in files:
		file = files[s]
		if not file.has_key("contents"):
			continue
#		try:
#			# Just check if the file has contents
#			contents = file.contents
#		except:
#			continue

		direc = directories[file.direc]

		run_hooks("scan",
			direc=direc,
			file=file)
	run_hooks("scan_done")


def render_files():
	info("Rendering files ...")

	for fname_in in files:
		global current_file
		file = files[fname_in]
		current_file = file

		# Do we have a renderer?
		if file.render is None:
			log("unhandled file: %s" % file.rel_path, 7)
			continue

		# Is the renderer not the default HTML renderer?
		if file.render != "html":
			#print file.render, "on", file.rel_path
			run_hooks(file.render,
				file=file,
				stop_if_result=True,
				return_holder=False)
			continue

		# Run default renderer
		direc = directories[file.direc]

		contents = run_macros(file, file.contents)
		#print "contents after 'macrorun':", contents
		file.contents = contents

		contents = run_hooks("htmlize",
			direc=direc,
			file=file,
			stop_if_result=True,
			return_holder=False)
		#print "contents after 'htmlize':", contents
		if not contents:
			continue
		file.contents = contents

		# Output-Filename "berechnen"
		file.out_path = os.path.splitext(fname_in)[0] + ".html"

	for fname_in in files:
		file = files[fname_in]
		current_file = file
		if not file.has_key("out_path"):
			#print "no out_path", file.rel_path
			continue
		direc = directories[file.direc]

		contents = run_hooks("linkify",
			direc=direc,
			file=file,
			return_holder=False)
		#print "contents after 'linkify':", contents
		if not contents:
			continue
		file.contents = contents

		# TODO: einige Fragmente sollen u.U. in eine andere
		# Webseite eingebaut werden und sollten daher nicht in
		# ein HTML-File landen
		contents = run_hooks("pagetemplate",
			direc=direc,
			file=file,
			stop_if_result=True,
			return_holder=False)
		#print "contents after 'pagetemplate':", contents


		# Output-Directory erzeugen
		fname_out = os.path.join(cfg.out_dir, file.out_path)
		dir_out = os.path.split(fname_out)[0]
		#print "dir_out:", dir_out
		try:
			os.makedirs(dir_out)
		except OSError:
			pass

		# TODO: evtl. überprüfen, ob contents == f.read(), dann nicht schreiben
		log("writing file %s" % fname_out, level=6)
		f = open(fname_out, "w")
		f.write(contents)
		f.close()
		# TODO: Time-Stamps setzen?

		#print file.mtime, file.get("ctime","?")
		#print direc.keys()



###############################################################################
#
#  Main program
#

@set_hook("addoptions")
def addoptions(params):
	parser = params["parser"]
	parser.add_option("-i", "--in", dest="in_dir", default="in",
		help="input directory",
		metavar="DIR")
	parser.add_option("-o", "--out", dest="out_dir", default="out",
		help="output directory",
		metavar="DIR")
	parser.add_option("--style-dir", dest="style_dir", default="in/style",
		help="directory with style sheets",
		metavar="STYLE")
	parser.add_option("-v", "--verbose", action="count",
		dest="verbose", default=3,
		help="print status messages to stdout")
	parser.add_option("-k", "--keepgoing", dest="keepgoing",
		action="store_true", default=False,
		help="keep going past errors if possible")

	return parser

	
@set_hook("checkconfig", last=True)
def checkconfig(params):
	# Ensure absolute paths that end in '/'.
	cfg.in_dir = os.path.join(os.getcwd(), cfg.in_dir).rstrip('/') + '/'
	assert cfg.in_dir.endswith('/')


def main():
	global cfg

	# Get configuration from webber.ini
	cfg.load('webber.conf')

	# Now load all plugins
	load_plugins()

	# Create parser and allow plugins to add their own command line stuff
	parser = optparse.OptionParser()
	args = run_hooks("addoptions", parser=parser)
	(options, args) = parser.parse_args()

	# Recast options into a Holder object, this allows
	# us to use it for Mapping.inheritFrom()
	options = Holder(**parser.values.__dict__)

	# link contents of webber.ini into cfg and set some defaults,
	# then let plugins fixup things in cfg.*
	cfg.inheritFrom(options)
	cfg.setDefault("exclude_dir", ["plugins"])
	run_hooks("checkconfig")

	run_hooks("start")

	walk_tree(cfg.in_dir)
	scan_files()
	render_files()

	run_hooks("finish")
