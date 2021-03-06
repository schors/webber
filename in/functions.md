title: Functions
parent: Webber
lang: en
ctime: 2009-06-24
mtime: 2011-01-13
change: remove reference to show_orphan

You can call functions only from [[template_mako]], not from
[[pages|pageformat]]. If you need the latter, look at [[macros]].

= Example =

	Modified ${format_date(mtime)}

= List of functions =

Here's list of functions defined by webber and it's default plugins:


== format_date(timestamp, format) ==

Takes a timestamp (seconds since 1st January 1970) and converts it into
a string.

"`format`" is optional. If not used, "`cfg.date_format`" will be used.
Otherwise it should be a format-string as documented by "`man strftime`". For
example, "`%Y-%m-%d`" stands for year-month-date.

Defined in `webber.py`.


== get_time(format) ==

Returns the current date/time as a string.

"`format`" is optional. If not used, "`cfg.date_format`" will be used.
Otherwise it should be a format-string as documented by "`man strftime`". For
example, "`%Y-%m-%d`" stands for year-month-date.

Defined in `webber.py`.


== get_breadcrumbs() ==

Returns the breadcrumbs as "`(page, link)`" tuples, where "`page`" is a "`class
File`"-object and link is a relative link from the current page to "`page`".

Defined in [[hierarchy.py|hierarchy]], where you find an example.


== get_current_file() ==

Returns the current "`class File`" object.

Defined in `webber.py`.


== get_recently(page) ==

Returns a list of up to 10 pages below the specified page. If you don't
specify a page, the current page will be used. For each page, you'll get a
"`(page, link)`" tuple back, where "`page`" is a "`class File`"-object and
link is a relative link from the current page to "`page`".

Defined in [[hierarchy.py|hierarchy]], where you find an example.


== get_sidemenu(root) ==

Returns a menu for the current page. For each page in this menu you'll get
back a "`(level, part_of_path, is_current, page, link)`" tuple, where
"`page`" is a "`class File`"-object and link is a relative link from the
current page to "`page`".

You'll need to specify "`root`" if your top-most page isn't named "`Home`".

Defined in [[hierarchy.py|hierarchy]], where you find an example.


== get_linear_sitemap(root, level) ==

Returns all pages as "`(level, page, link)`" tuples, where "`page`" is a
"`class File`"-object and link is a relative link from the current page to
"`page`".

You'll need to specify "`root`" if your top-most page isn't named "`Home`".

The "`level`" will by default start at 1.

Defined in [[hierarchy.py|hierarchy]], where you find an example.

== get_toc() ==

Returns an unsorted list with the hierarchy of the table-of-contents.

Defined in [[toc.py|toc]], where you find an example.


= Writing functions =

A function is a simply python function which returns HTML. The function needs
to be decorated with "`@set_function(name)`". There's an example in
[[skeleton.py|skeleton]], which looks like:

	:::python
	@set_function("func")
	def sample_func():
	        if cfg.test_verbose:
        	        print "in macro skeleton.sample_func"
	        return "{ output from sample function }"

Inside your template, you can call the function without parameters or
with arbitrary parameters, like this:

	${func(a=1, b="test")}

Inside your function you can access this as ...

* "`params.a`" which contains the integer "`1`"
* "`params.b`" which contains the string "`test`"
