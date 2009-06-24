# -*- coding: iso-8859-1 -*-
from webber import *
from docutils.writers import html4css1
from docutils import core


@set_hook("read")
def read(params):
	file = params.file
	if file.rel_path.endswith(".rst"):
		file.render = "html"
		f = file.read_keywords()
		return f.read()



class WebHTMLTranslator(html4css1.HTMLTranslator):
	doctype = ""	
	content_type = "<!--%s-->"
	generator = "<!--%s-->"
	
	def __init__(self, document):
		html4css1.HTMLTranslator.__init__(self, document)
		self.head_prefix = []
		self.body_prefix = []
		self.stylesheet = []
		self.body_suffix = []
		self.section_level = 1
		
	def visit_system_message(self, node):
		pass

	def visit_document (self, node):
		pass
	
	def depart_document (self, node):
		pass

class WebWriter(html4css1.Writer):
	def __init__ (self):
		html4css1.Writer.__init__(self)
		self.translator_class = WebHTMLTranslator


@set_hook("htmlize")
def htmlize(params):
	"Parse text as RST and convert it to HTML"

	file = params.file
	if not file.rel_path.endswith(".rst"):
		return

	contents = file.contents

	settings = {
		# cloak email addresses to reduce spam
		'cloak_email_addresses': 1,
		# Emit headers as H2, because H1 is already used
		'doctitle_xform': False,
		'strip_comments': 'true',
		#'dump_pseudo_xml': 'true',
		#'dump_settings': 'true',
		#'dump_transforms': 'true',
		# TODO: language_code?
		}
	# http://docutils.sourceforge.net/docs/dev/hacking.html
	# /usr/share/doc/python-docutils/
	document = core.publish_doctree(
		source_path=params.file.rel_path,
		source=contents,
		settings_overrides=settings)
	return core.publish_from_doctree(document,
		writer=WebWriter(),
		writer_name='html',
		destination_path=params.file.rel_path,
		settings_overrides=settings)
