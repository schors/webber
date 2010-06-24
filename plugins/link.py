# -*- coding: iso-8859-1 -*-
from webber import *
import os, re

# To understand this beast, read /usr/share/doc/python2.5-doc/html/lib/module-re.html :-)

reLink = re.compile(r'''
	\[\[				# Begin of link
	(?=[^!])			# Don't fire for macros
	(?:
		([^\]\|]+)		# 1: link text
		\|				# followed by '|'
	)?					# optional
	([^\n\r\]#]+)		# 2: page to link to
	(
		\#				# '#', beginning of anchor
		[^\s\]]+		# 3: anchor text, doesn't contain spaces or ']'
	)?					# optional
	\]\]				# end of link
	''', re.VERBOSE)

def do_link(m):
	"""Used in re.sub() to substitute link with HTML"""
	text = m.group(1) or ""
	text = text.replace("\n", " ")
	link = m.group(2).replace("\n", " ")
	anchor = m.group(3) or ""
	if link.find(".") == -1:
		for f in files:
			file = files[f]
			if not file.has_key("linktitle"):
				continue
			if file.title == link or \
			   file.linktitle == link or \
			   os.path.splitext(os.path.basename(file.path))[0] == link:
				#print "LINK: '%s' '%s' -> '%s'" % (text, link, file.linktitle)
				if not text:
					text = file.title
				link = get_link_from(get_current_file().linktitle, file.linktitle)
				#print "LINK: '%s' '%s'" % (text, link)
				break
	if not text:
		text = link
	# validate link
	# TODO: validating local files still not working
	if not link.startswith("http:") and not link.endswith(".html") and not link.endswith(".png"):
		file = get_current_file()
		warning("%s: unknown link to '%s'" % (file.rel_path, link) )
	return '<a href="%s%s">%s</a>' % (link, anchor, text)


def test_link():
	for s in (
			'Before [[!macro]] after',
			'Before [[link]] after',
			'Before [[Text|link]] after',
			'Before [[Text|link#anchor]] after'
		):
		m = reLink.search(s)
		if m:
			print "link:", s
			print "	 name:", m.group(1)
			print "	 link:", m.group(2)
			print "	 anchor:", m.group(3)
		else:
			print "No link:", s

def test_sub():
	for s in (
			'Before [[!macro]] after',
			'Before [[link]] after',
			'Before [[Text|link]] after',
			'Before [[Text|link#anchor]] after'
		):
		print s
		res = reLink.sub(do_link, s)
		print "", res


@set_hook("linkify")
def linkify(params):
	params.file.contents = reLink.sub(do_link, params.file.contents)
