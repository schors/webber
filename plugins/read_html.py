# -*- coding: iso-8859-1 -*-
from webber import *


@set_hook("read")
def read(params):
	file = params.file
	if file.rel_path.endswith(".html"):
		file.render = "html"
		f = file.read_keywords()
		return f.read()


@set_hook("htmlize")
def htmlize(params):
	"""Parse HTML  and "convert" it to HTML :-)"""

	file = params.file
	if not file.rel_path.endswith(".html"):
		return

	return file.contents
