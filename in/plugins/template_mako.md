title: Mako template
linktitle: template_mako.py
parent: Plugins
ctime: 2009-06-26
change: finally documented how templates work

This plugin uses the [[Mako template
library|http://www.makotemplates.org/]] to render the actual pages
during the "`pagetemplate`" [[hook|hooks]].

= Configuration =

== template ==

Name of the template file. Must be specified in "`webber.conf`", but
can be overriden, see "[[inheritance]]" and "[[pageformat]]".

	template: "default"

Note that you don't need to add the "`.tmpl`" file suffix.

== style_dir ==

Directory where templates (and often CSS files) reside. Defaults to
"`in/style`".

== input_encoding and output_encoding ==

Name of the encoding for the input files (page files, templates etc)
and the output files (rendered HTML pages). Must be specified in
"`webber.conf`".

	input_encoding: "iso-8859-1"
	output_encoding: "iso-8859-1"

= Template files =

The "`*.tmpl`" files in the specified style directory can now utilize
the fill power of Mako. Here's an example of a rather minimal
template:

	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html>
	<head>
	<title>${file.title | entity}</title>
	<meta http-equiv="Content-Type" content="text/html; charset=${file.output_encoding}"/>
	% if len(keywords):
	        <meta name="keywords" content="${keywords | entity}" />
	% endif
	% if len(description):
	        <meta name="description" content="${description | entity}" />
	% endif
	</head>
	<body>
	<h1>${file.title | entity}</h1>
	${body}
	</body>
	</html>

== Example of template inheritance ==

However, be replacing "`${body}`" with a named make container, we can
use inheritance to modify the page body on a per-file basis. Add this
at the top of the file:

	<%def name="contents()">\
	${body}
	</%def>\
	#######################################################################

and replace "`${body}`" with:

	${self.contents()}

Now you can create a new template file, e.g. "`history.tmpl`" that
inherits from "`default.tmpl`" and add's a list of recently changed
files:

	<%inherit file="default.tmpl"/>
	#######################################################################
	<%def name="contents()">\
	${body}
	<%
	  recently = get_recently()
	%>
	% if len(recently)>1:
	<h2>What's new?</h2>
	%   for page, link in recently:
	%     if page.mtime > page.ctime:
	        Modified ${format_date(page.mtime)}\
	%     else:
	        Created ${format_date(page.ctime)}\
	%     endif
	: <a href="${link}">${page.title | entity}</a><br />
	%   endfor
	% endif
	</%def>\




== Page attributes ==

As you migt have seen in the above example, you have access to various
objects and their members ("`${page.title}`"), variables ("`${body}`")
and functions ("`$format_date()`").

=== ${file} ===

This is the file object. TODO

=== ${body} ===

This is the page body, as rendered by the [[hooks|hooks]] "`htmlize"`
and "`linkify`".

=== ${rootpath} ===

This is the path from the current file to the top-level directory. You
can use this for relative links inside your document.

Example: conside that the current rendered page is test/foo/bar.html. Then
"`${rootpath}`" is "`../../"`. So you can access your main index.html
file by "`${rootpath}index.html`".

=== ${description} ===

That's the "`description:`" text from your [[page|pageformat]]. You
can use this in meta tags in your HTML header.

=== ${keywords} ===

That's the "`keywords:`" text from your [[page|pageformat]]. You
can use this in meta tags in your HTML header.

=== Functions marked with @set_function() ===

Any function marked with "`@set_function("name")`" can be used in the
template. Whatever text the function returns is put into the final
page.

All functions are documented on the "[[functions]]" page.
