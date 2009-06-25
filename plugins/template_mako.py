# -*- coding: iso-8859-1 -*-
from webber import *
from mako.lookup import TemplateLookup
import os

"""
The make template renders a *.tmpl file which can contain things like

	${file}           the current File object
	${body}           HTML for the main contents
	${rootpath}       (relative!) path to the web site root directory
	${description}    used for meta=
	${keywords}       used for meta=

	... and also all functions decorated with "@set_function(name)".
"""


template_cache = {}

def get_template(file):
	filename = file.template
	extra_dir = os.path.split(file.path)[0]
	if not filename.endswith('.tmpl'):
		filename += '.tmpl'
	key = "%s %s" % (filename, extra_dir)
	if template_cache.has_key(key):
		return template_cache[key]
	else:
		lookup = TemplateLookup(
			directories = (extra_dir, file.style_dir),
			input_encoding = file.input_encoding,
			output_encoding = file.output_encoding,
			encoding_errors='replace',
			filesystem_checks = False)
		tmpl = lookup.get_template(filename)

		template_cache[key] = tmpl
		return tmpl


@set_hook("pagetemplate")
def pagetemplate(params):
	#print "in webber_template_mako.pagetemplate"
	#print params.file

	kw = {}
	kw["file"] = params.file
	if isinstance(params.file.contents, unicode):
		kw["body"] = params.file.contents
	else:
		kw["body"] = unicode(params.file.contents, 'iso-8859-1')

	#print "path:", params.file.out_path
	root = []
	for i in range(params.file.out_path.count("/")):
		root.append("..")
	#print "root:", root
	root = "/".join(root)
	if root:
		root = root + "/"
	#print "root:", root
	kw["rootpath"] = root
	try:
		kw["description"] = params.file.description
	except:
		kw["description"] = ""
	try:
		kw['keywords'] = params.file.keywords
	except:
		kw['keywords'] = []
	kw.update(functions)
	tmpl = get_template(params.file)

	contents = tmpl.render(**kw)
	return contents
