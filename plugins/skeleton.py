# -*- coding: iso-8859-1 -*-
from webber import *


#
# The hook "addoptions" can be used by plugins to add their own
# command line options.
#
# params.parser contains the optparse based parser
#
@set_hook("addoptions")
def test_addoptions(params):
	#print "in skeleton.addoptions"
	params.parser.add_option("-V", "--test_verbose", action="count",
		dest="test_verbose", default=0,
		help="print status messages to stdout")


#
# After the command-line options have been processed and incorporated into
# config object, the hook "checkconfig" is called. Here each plugin can
# check if the specified configurations are sane.
#
# params is empty, use cfg instead
#
@set_hook("checkconfig")
def checkconfig(params):
	if cfg.test_verbose:
		print "in skeleton.checkconfig"
	#cfg.blah = "muh"


#
# Just before walking the directory tree, the hook "start"
# get's called.
#
# param is empty
#
@set_hook("start")
def finish(params):
	if cfg.test_verbose:
		print "in skeleton.start"


#
# For each file that is not excluded (and not in an excluded directory, the
# hook "read" is called. Usually a reader-plugin (e.g. "rst" or
# "markdown") looks at the file extension of the file parameter.
#
# If the plugin declares itself responsible for this file, it should return
# the contents of the file. It also should set file.reader to some text
# string that describes itself.
#
# params.direc contains a "class Directory" object
# params.file contains a "class File" object
#
@set_hook("read")
def read(params):
	if cfg.test_verbose:
		print "in skeleton.read", params.file.rel_path
	#return "contents of file"


#
# After a file has been read in, any plugin can filter it's raw
# text.
#
# params.direc contains the "class Directory" object
# params.file has the "class File" object
# params.contents contains the text
#
@set_hook("filter")
def filter(params):
	if cfg.test_verbose:
		print "in skeleton.filter", params.file.rel_path
		if cfg.verbose > 6:
			params.contents = "contents deleted by skeleton.filter"


#
# "scan" should scan for meta-data, mostly for links.
#
# params.direc contains the "class Directory" object
# params.file has the "class File" object
# params.file.contents contains the text
#
@set_hook("scan")
def scan(params):
	if cfg.test_verbose:
		print "in skeleton.scan", params.file.rel_path


#
# "scan_done" is called once after all files have been scanned
#
# params is empty
#
@set_hook("scan_done")
def scan_done(params):
	if cfg.test_verbose:
		print "in skeleton.scan_done"


#
# The "htmlize" converts the contents into html. The
# first htmlize hook that returs anything wins, no other
# htmlize hooks will be called.
#
# params.direc contains the "class Directory" object
# params.file has the "class File" object
# params.file.contents contains the text
#
@set_hook("htmlize")
def htmlize(params):
	if cfg.test_verbose:
		print "in skeleton.htmlize", params.file.rel_path


#
# The "linkify" hook converts any link to html.
#
# params.direc contains the "class Directory" object
# params.file has the "class File" object
# params.file.contents contains body text of the page
#
@set_hook("linkify")
def linkify(params):
	if cfg.test_verbose:
		print "in skeleton.linkify", params.file.rel_path


#
# At the very end of the program execution, the hook "finish"
# get's called.
#
# params is empty
#
@set_hook("finish")
def finish(params):
	if cfg.test_verbose:
		print "in skeleton.finish"



# TODO: Description missing
@set_macro("sample")
def sample_macro(params):
	if cfg.test_verbose:
		print "in macro skeleton.sample_macro, params:", params
	return "{ output of sample macro }"



# TODO: Description missing
@set_function("func")
def sample_func():
	if cfg.test_verbose:
		print "in macro skeleton.sample_func"
	return "{ output from sample function }"
