# -*- coding: iso-8859-1 -*-
import webber
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

	# Ignore hidden pages
	if file.has_key("hide") and file.hide:
		return

	if file.has_key("links"):
		memorize_links(file.title, file.links)
	if file.has_key("parent"):
		if file.has_key("order"):
			order = int(file.order)
		else:
			order = 100
		memorize_parent(file.title, file.parent, order)


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
def get_breadcrumbs(orig_page=None):
	if orig_page is None:
		orig_page = get_current_file()
	res = [(orig_page, get_link_from(orig_page, orig_page))]
	page = orig_page
	#print "orig_page:", orig_page
	while _parent.has_key(page.title):
		page = get_file_for(_parent[page.title])
		link = get_link_from(orig_page, page)
		#print "  page, link:", page, link
		res.insert(0, (page, link))
	#print res
	return res


@set_function("get_sidemenu")
def get_sidemenu(root="Home", level=1):
	page = get_current_file()
	if not isinstance(root, webber.File):
		root = get_file_for(root)

	bread = get_breadcrumbs()
	#print "Menu for:", page
	#print "Bread:", bread

	res = [(0, 1, int(root==page), root, get_link_from(page, root))]

	def do_menu(pg, level):
		#print "pg, has_key:", pg, _childs.has_key(pg)
		if _childs.has_key(pg.title):
			for p in _childs[pg.title]:
				subpage = get_file_for(p[1])
				in_bread = False
				for b in bread:
					if b[0] == subpage:
						in_bread = True
						break

				go_deeper = in_bread or (subpage==page)
				#print "subpage:", subpage, "in bread:", in_bread, "go deeper:", go_deeper
				link = get_link_from(page, subpage)
				res.append((level, in_bread, int(subpage==page), subpage, link))
				if go_deeper:
					do_menu(subpage, level+1)

	# TODO: make this configurable, e.g. cfg.rootpage, otherwise a page
	# that is outside of the menu won't show a menu
	do_menu(root, level)
	return res



@set_function("get_hierarchical_sitemap")
def get_hierarchical_sitemap(root="Home", show_orphans=False):
	page = get_current_file()
	if not isinstance(root, webber.File):
		root = get_file_for(root)

	visited = {root: True}
	def do_menu(pg):
		res = []
		if _childs.has_key(pg.title):
			for p in _childs[pg.title]:
				subpage = get_file_for(p[1])
				visited[subpage] = True
				res.append( do_menu(subpage) )
		return (pg, get_link_from(root, pg), res)

	res = do_menu(root)

	if show_orphans:
		for f in files:
			#print f
			file = files[f]
			if not file.has_key("linktitle"):
				continue
			try:
				if file in visited:
					#print "found", file.linktitle
					continue
			except KeyError:
				continue
			#print "not found:", file.linktitle
			res.append( (file, get_link_from(page, file.title), []) )

	#import pprint
	#pprint.pprint(res, indent=4)
	return res


@set_function("get_linear_sitemap")
def get_linear_sitemap(root="Home", show_orphans=False, level=1):
	page = get_current_file()
	if not isinstance(root, webber.File):
		root = get_file_for(root)

	visited = {root: None}
	res = [(0, root, get_link_from(page, root))]

	def do_menu(pg, level):
		#print "pg:", pg
		#, _childs.has_key(pg.title)
		if _childs.has_key(pg.title):
			for p in _childs[pg.title]:
				subpage = get_file_for(p[1])

				#print "subpage:", subpage
				link = get_link_from(page, subpage)
				res.append((level, subpage, link))
				visited[subpage] = None
				do_menu(subpage, level+1)

	do_menu(root, level)

	#print "visited:", visited
	if show_orphans:
		for f in files:
			#print f
			file = files[f]
			if not file.has_key("linktitle"):
				continue
			try:
				if file in visited:
					#print "found", file.linktitle
					continue
			except KeyError:
				continue
			#print "not found:", file.linktitle
			res.append( (0, file, get_link_from(page, file.title)))
	#import pprint
	#pprint.pprint(res)
	return res


@set_function("get_recently")
def get_recently(page=None, max_items=10):
	if page is None:
		page = get_current_file()
	elif not isinstance(page, webber.File):
		page = get_file_for(page)

	res = []
	orig_page = page

	def addPage(res, page):
		#print "page:", page
		res.append( (page, get_link_from(orig_page, page)) )
		if _childs.has_key(page.title):
			for c in _childs[page.title]:
				addPage(res, get_file_for(c[1]))
	addPage(res, orig_page)
	res.sort(cmp = lambda x,y: cmp(y[0].mtime, x[0].mtime))
	return res[:max_items]
