# -*- coding: iso-8859-1 -*-
from webber import *
import re

reSPLIT = re.compile(r',\s*')

_childs = {}
_parent = {}

def memorize_links(title, links):
	global _childs
	if not links:
		return
	order = 100
	for link in reSPLIT.split(links):
		#print title, link
		if not _childs.has_key(title):
			_childs[title] = []
		_childs[title].append( (order,link))
		order += 100
		_parent[link] = title


def memorize_parent(title, parent, order=100):
	#print "memorize_parent:", title, parent
	#print "  parent:", _parent
	#print "  childs:", _childs
	#print "order:", title, order
	if not _childs.has_key(parent):
		_childs[parent] = []
	_childs[parent].append( (order, title) )
	_parent[title] = parent
	

#
# The "scan" plugins should scan for meta-data, mostly for links.
#
# params.direc contains the "class Directory" object
# params.file has the "class File" object
# params.file.contents contains the text
#
@set_hook("scan")
def scan(params):
	file = params["file"]
	if file.has_key("links"):
		memorize_links(file.linktitle, file.links)
	if file.has_key("parent"):
		if file.has_key("order"):
			order = int(file.order)
		else:
			order = 100
		memorize_parent(file.linktitle, file.parent, order)


@set_hook("scan_done")
def scan_done(params):
	"""After every file has been scanned, we sort the list of childs-per-page
	in ascending order."""

	for c in _childs:
		_childs[c].sort()
	return

	print "_parent:"
	for c in _parent:
		print " ", c, _parent[c]
	print "_childs:"
	for c in _childs: print " ", c,_childs[c]


@set_function("get_breadcrumbs")
def get_breadcrumbs(orig_page):
	"""Returns something like ['Home', 'Beruf', 'Werdegang']. This can
	be easyly used to generate breadcrumbs HTML code."""
	res = [(orig_page, get_link_from(orig_page, orig_page))]
	page = orig_page
	#print "orig_page:", orig_page
	while _parent.has_key(page):
		page = _parent[page]
		link = get_link_from(orig_page, page)
		#print "  page, link:", page, link
		res.insert(0, (page, link))
	return res



@set_function("get_sidemenu")
def get_sidemenu(page):
	"""Returns an array with a side-menu. Everything from the current
	page upwards is shown, as well as one level below the current
	position. The array has the following items:

	level  part-of-path  current-page  title

	Example:
		0 1 0 Home
		1 1 0 Beruf
		2 0 0 Kenntnisse
		2 1 0 Werdegang
		3 0 1 Alte
		1 0 0 Haus
	"""
	# Determine root page:
	bread = get_breadcrumbs(page)
	#print "Menu for:", page
	#print "Bread:", bread

	root = "Home" #TODO
	res = [(0, 1, int(root==page), root, get_link_from(page, root))]

	def do_menu(pg, level):
		#print "pg, has_key:", pg, _childs.has_key(pg)
		if _childs.has_key(pg):
			for p in _childs[pg]:
				subpage = p[1]
				in_bread = False
				for b in bread:
					if b[0] == subpage:
						in_bread = True
						break

				go_deeper = in_bread or (subpage==page)
				#print "subpage:", subpage, "in bread:", in_bread, "go deeper:", go_deeper
				link = get_link_from(page, subpage)
				res.append((level, int(subpage in bread), int(subpage==page), subpage, link))
				if go_deeper:
					do_menu(subpage, level+1)

	# TODO: make this configurable, e.g. cfg.rootpage, otherwise a page
	# that is outside of the menu won't show a menu
	do_menu(root, 1)
	return res



@set_function("get_sitemap")
def get_sitemap(page):
	# Determine root page:
	root = "Home" #TODO
	
	res = [(0, get_file_for(root).title, get_link_from(page, root))]

	visited = {root: None}
	def do_menu(pg, level):
		#print "pg, has_key:", pg, _childs.has_key(pg)
		if _childs.has_key(pg):
			for p in _childs[pg]:
				subpage = p[1]

				#print "subpage:", subpage, "in bread:", in_bread, "go deeper:", go_deeper
				link = get_link_from(page, subpage)
				res.append((level, subpage, link))
				visited[subpage] = None
				do_menu(subpage, level+1)

	do_menu(root, 1)
	#print visited
	for f in files:
		#print f
		file = files[f]
		try:
			if file.linktitle in visited:
				#print "found", file.linktitle
				continue
		except KeyError:
			continue
		#print "not found:", file.linktitle
		res.append( (0, file.title, get_link_from(page, file.linktitle)))
	#for t in res: print t
	return res


@set_function("get_recently")
def get_recently(file):
	#file = get_current_file()
	#print "XXXXXX:", file.linktitle
	pg = []

	max_n = 10	# TODO: configurable?
	orig_page = file.linktitle

	def addPage(pg, title):
		#print "addPage", title
		for f in files:
			file = files[f]
			#print file
			if file.has_key("linktitle") and file.linktitle == title:
				pg.append( (file.mtime, file.ctime, file.title, get_link_from(orig_page, file.linktitle)) )
				if _childs.has_key(file.linktitle):
					for c in _childs[file.linktitle]:
						#print "c:", c
						addPage(pg, c[1])
						if len(pg) == max_n:
							return
	addPage(pg, orig_page)
	pg.sort(reverse=True)
	#for p in pg: print p
	return pg


	
	

if __name__ == "__main__":
	# You can call this test-code this way:
	#
	#	PYTHONPATH=`pwd` python plugins/hierarchy.py
	#
	memorize_parent("Impressum", "Home", 99999)
	memorize_parent("Beruf", "Home", 100)
	memorize_parent("Werdegang", "Beruf", 100)
	memorize_parent("Kenntnisse", "Beruf", 200)
	scan_done(None)
	
	#print get_breadcrumbs("Home")
	#print get_breadcrumbs("Beruf")
	#print get_breadcrumbs("Werdegang")
	#print get_breadcrumbs("Kenntnisse")
	#for t in get_sidemenu("Home"): print t
	#for t in get_sidemenu("Beruf"): print t
	#for t in get_sidemenu("Kenntnisse"): print t
	for t in get_sitemap("Home"): print t
