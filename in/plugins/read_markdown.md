title: Read Markdown
linktitle: read_markdown.py
parent: Plugins
lang: en
ctime: 2009-06-26
mtime: 2009-06-26

This plugin reads "`*.md`" files and converts them to HTML.

"[[Markdown|http://daringfireball.net/projects/markdown/]]" is a wiki-like
text format. The plugin "`read_markdown.py`" doesn't use the 
standard Python module "`markdown`", but instead the faster and simpler
[[markdown2|http://code.google.com/p/python-markdown2/]] module.

A sample "`test.md`" document looks like this:

	title: Impressum
	parent: Home
	ctime: 2008-10-01

	# Address

	  Mario Marionetti
	  10, Mariott St
	  Marioland 1007

	Don't send me spam, *ever*!

You'll find more about "`title:`", "`parent:`" and "`ctime:`" in the
[[page format|pageformat]] description.

= Modifications =

This implementation is based on python-markdown2 version 1.0.1.12, but has been
changed this way:

* file-vars (emacs-style settings inside the file) have been disabled
* "Standardize line endings" removed
* call to _do_links() removed (we have the [[linkify|link.html]] pass for
  this)
* logging removed
* allow "= Header =" in addition to "# Header #"

Python

	>>> s = "KEK"
	>>> s
	"KEK"
