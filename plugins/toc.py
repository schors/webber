# -*- coding: iso-8859-1 -*-
from webber import *
import htmlentitydefs, re


reHeader = re.compile(r'<h(\d)(.*)>(.*)</h\1>', re.IGNORECASE | re.MULTILINE)
_toc = []
_labels = {}
_first = -1

toc_min_lines = 30


@set_hook("checkconfig")
def checkconfig(params):
	if cfg.has_key("toc_min_lines"):
		global toc_min_lines
		toc_min_lines = int(cfg.toc_min_times)


def slugify(text, separator):
	"""
	This function converts a normal text string into a string, that
	can be safely used for HTML links and anchors.

	Based on http://snipplr.com/view/26266/create-slugs-in-python/
	"""

	ret = ""
	for c in text.lower():
		try:
			ret += htmlentitydefs.codepoint2name[ord(c)]
		except:
			ret += c
	ret = re.sub("([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)", r"\1", ret)
	ret = re.sub("\W", " ", ret)
	ret = re.sub(" +", separator, ret)
	return ret.strip()


def repl(m):
	"""
	Function used for re.sub() to find all header elements (h1, h2, ...).
	Data from those elements (level, headline) are stored in the global
	array `toc`.

	This function also modifies the text by adding a anchor to the
	header.
	"""
	global _toc
	global _first
	label = slugify(m.group(3), "_")
	if _labels.has_key(label):
		n = 0
		while True:
			l = "%s_%d" % (label, n)
			if not _labels.has_key(l):
				label = l
				break
			n += 1

	level = int(m.group(1))
	if _first == -1:
		_first = level
	_toc.append( (level - _first, m.group(3), label) )
	_labels[label] = 1
	return '<h%s%s>%s<a name="%s">&nbsp;</a></h%s>' % (
		m.group(1),
		m.group(2),
		m.group(3),
		label,
		m.group(1))



@set_hook("linkify")
def linkify(params):
	global _toc
	global _labels
	global _first
	_toc = []
	_labels = {}
	_first = -1

	# Very small pages don't need a table-of-contents
	if params.file.contents.count("\n") < toc_min_lines:
		return

	params.file.contents = reHeader.sub(repl, params.file.contents)



@set_function("get_toc")
def get_toc():
	return _toc
