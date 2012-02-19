# -*- coding: iso-8859-1 -*-
"""Functions almost the same way like hierarchy, except for two things:

    * The 'parent' attribute should contain the filename of the parent (instead
    of the title), without the extension
    * If the filename isn't found in the current directory, the path tree is traversed.
    """

import webber
import re
import os

from webber import *
from webber import log


reSPLIT = re.compile(r',\s*')

# These hashes store webber.File instances
_childs = {}
_parent = {}

def get_extensionless_path(path):
    """Returns file path and filename for `path` without the file extension."""
    return os.path.splitext(path)[0]

def get_file_for_filename(thisfile, parent_name):
    """webber.files is an hash of File objects, but keyed on the real file name.
    This function returns a File object.

    The directy where `thisfile` is in is the starting point for the search. If
    not present in the same directory, the `parent_name` is looked for by traversing
    the file tree recursively.

    Return None if no file with `name` could be located.
    """

    full_path = os.path.split(thisfile.rel_path)[0]
    path_parts = full_path.split('/')

    # x holds the number of path_parts to use in the search path, from full
    for x in xrange(len(path_parts), -1, -1):
        if x > 0:
            search_path = os.path.join(*path_parts[:x])
        else:
            search_path = ''
        search_path = os.path.join(
            search_path, parent_name
        )

        # Prevent linking to self
        if search_path == get_extensionless_path(thisfile.rel_path):
            continue

        for s in files:
            f = files[s]
            try:
                if get_extensionless_path(f.rel_path) == search_path:
                    return f
            except Exception, e:
                log.error('%s: %s' % (
                    f, e
                ))

            # Allow exact match as well
            #if s == parent_name:
                #print "  exact:", s
            #    _get_file_for_fileparent_name_cache[name] = f
            #    return f

    # As a last possibility, see if we could just return the current page
    if get_extensionless_path(thisfile.rel_path) == parent_name:
        return thisfile

    return None

def get_file_basename(file_path):
    """Returns the filename, without extension, from a path."""
    filename = os.path.basename(file_path)
    basename, extension = os.path.splitext(filename)
    return extension

def memorize_links(thisfile, links):
	global _childs
	if not links:
		return
	order = 100
	for link in reSPLIT.split(links):
		linked = get_file_for(link)
		if not _childs.has_key(thisfile):
			_childs[thisfile] = []
		_childs[thisfile].append( (order, linked))
		order += 100
		#print "memorize_links:", thisfile, "->", linked
		_parent[linked] = thisfile

def memorize_parent(thisfile, parent, order=100):
    # Convert titles or linktitle to entries of webber.File
    if not isinstance(parent, webber.File):
        parent = get_file_for_filename(thisfile, parent)

    if not _childs.has_key(parent):
        _childs[parent] = []
    _childs[parent].append( (order, thisfile) )
    #print "memorize_parent:", thisfile, "->", parent
    _parent[thisfile] = parent


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
        memorize_links(file, file.links)
    if file.has_key("parent"):
        if file.has_key("order"):
            order = int(file.order)
        else:
            order = 100
        memorize_parent(file, file.parent, order)


@set_hook("scan_done")
def scan_done(params):
    """After every file has been scanned, we sort the list of childs-per-page
    in ascending order."""

    for c in _childs:
        # Sort by linktitle
        _childs[c].sort(key = lambda x: x[1].linktitle)
        # And now sort by priority. Since Python 2.2 and upwards has stable-sort,
        # this effectively makes a two-dimensional sort.
        _childs[c].sort(key = lambda x: x[0])

    visited = {}
    visited[get_file_for("Home")] = True

    for f in _parent:
        visited[f] = True
    for f in files:
        file = files[f]
        if not visited.has_key(file):
            warning("orphan file '%s'" % f)


@set_function("get_breadcrumbs")
def get_breadcrumbs(orig_page=None):
    if orig_page is None:
        orig_page = get_current_file()
    res = [(orig_page, get_link_from(orig_page, orig_page))]
    page = orig_page

    while _parent.has_key(page):
        page = _parent[page]
        link = get_link_from(orig_page, page)
        res.insert(0, (page, link))
    return res


@set_function("get_sidemenu")
def get_sidemenu(root="Home", level=1):
    """Returns (level, part_of_path, is_current, page, link) tuples, where
    page is a class File object and link is a relative link from the current
    page to page.
    """

    page = get_current_file()
    if not isinstance(root, webber.File):
        root = get_file_for_filename(page, root)

    res = [(0, 1, int(root==page), root, get_link_from(page, root))]

    bread = get_breadcrumbs()

    def do_menu(pg, level):
        if _childs.has_key(pg):
            for p in _childs[pg]:
                subpage = p[1]
                in_bread = False
                for b in bread:
                    if b[0] == subpage:
                        in_bread = True
                        break

                go_deeper = in_bread or (subpage==page)
                link = get_link_from(page, subpage)
                res.append((level, in_bread, int(subpage==page), subpage, link))
                if go_deeper:
                    do_menu(subpage, level+1)

    # TODO: make this configurable, e.g. cfg.rootpage, otherwise a page
    # that is outside of the menu won't show a menu
    do_menu(root, level)

    # print "-" * 77
    # import pprint
    # pprint.pprint(res)
    # print "-" * 77
    return res



@set_function("get_hierarchical_sitemap")
def get_hierarchical_sitemap(root="Home"):
    page = get_current_file()
    if not isinstance(root, webber.File):
        root = get_file_for(root)

    def do_menu(pg):
        res = []
        if _childs.has_key(pg):
            for p in _childs[pg]:
                subpage = p[1]
                res.append( do_menu(subpage) )
        return (pg, get_link_from(root, pg), res)

    res = do_menu(root)

    #import pprint
    #pprint.pprint(res, indent=4)
    return res


@set_function("get_linear_sitemap")
def get_linear_sitemap(root="Home", level=1):
    page = get_current_file()
    if not isinstance(root, webber.File):
        root = get_file_for(root)

    res = [(0, root, get_link_from(page, root))]

    def do_menu(pg, level):
        #print "pg:", pg
        #, _childs.has_key(pg.title)
        if _childs.has_key(pg):
            for p in _childs[pg]:
                subpage = p[1]

                #print "subpage:", subpage
                link = get_link_from(page, subpage)
                res.append((level, subpage, link))
                do_menu(subpage, level+1)

    do_menu(root, level)

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
        if _childs.has_key(page):
            for c in _childs[page]:
                addPage(res, c[1])
    addPage(res, orig_page)
    res.sort(cmp = lambda x,y: cmp(y[0].mtime, x[0].mtime))
    return res[:max_items]
