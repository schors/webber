title: Read RST
linktitle: read_rst.py
parent: Plugins
lang: en
ctime: 2009-06-26
mtime: 2009-06-26

This plugin reads "`*.rst`" files and converts them to HTML.

"RST" is the abbreviation for
[[reStructuredText|http://docutils.sourceforge.net/rst.html]], a format
common for many python programmers. The plugin "`read_rst.py`" uses the
standard Python module "`docutils`" to convert RST into HTML. A sample
"`test.rst`" document looks like this:

	title: Impressum
	parent: Home
	ctime: 2008-10-01

	Address
	=======

	|Mario Marionetti
	|10, Mariott St
	|Marioland 1007

	Don't send me spam, *ever*!

You'll find more about "`title:`", "`parent:`" and "`ctime:`" in the
[[page format|pageformat]] description.
