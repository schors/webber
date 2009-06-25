title: Functions
parent: Webber
ctime: 2009-06-26

= Calling functions =

You can call functions only from [[template_mako]]. An example:

	Modified ${format_date(mtime)}

Here's list of functions defined by webber and it's default plugins:


== format_date ==

Takes a timestamp (seconds since 1st January 1970) and converts it into
a string, using to `cfg.date_format`.

Defined in `webber.py`.


== get_time ==

Returns the current date/time as a string according to `cfg.date_format`.

Defined in `webber.py`.


== get_breadcrumbs ==

Returns the breadcrumbs as "`(linktitle, link)`" tuples.

Defined in [[hierarchy.py|hierarchy]], where you find an example.


== get_current_file ==

Returns the current `class File` object.

Defined in `webber.py`.


== get_recently ==

Returns a list of up to 10 pages below the current page. For each
page, you'll get a "`(mtime, ctime, title, link)`" tuple back.

Defined in [[hierarchy.py|hierarchy]], where you find an example.


== get_sidemenu(root) ==

Returns a menu for the current page. For each page in this menu you'll
get back a "`(level, part_of_path, is_current, title, link)`" tuple.

Defined in [[hierarchy.py|hierarchy]], where you find an example.


== get_sitemap(home, show_orphans) ==

Returns all pages as "`(level, title, link)`" tuples.

You'll need to specify "`root`" if your top-most page is a different one.

To put pages into the sitemap that are outside the parent/child relationships,
specify "`True`" for "`show_orphans`".

Defined in [[hierarchy.py|hierarchy]], where you find an example.


== func ==

A sample function in the [[skeleton.py|skeleton]]. See below.


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
