title: Configuration inheritance
linktitle: Inheritance
parent: Configuration
lang: en
ctime: 2009-06-24
mtime: 2010-07-06
change: various clarifications, a better example

= Overview =

Internally, webber uses a bunch of `Holder` classes to store information.

We have objects of class `Holder` for this entities:

* "`cfg`" stores [[configuration]] and [[commandline]].
* "`direc`" stores per-directory variables
* "`file`" stores attributes for each file that webber processes

This is like the inheritance works:

* "`direc`" inherits everything from "`cfg`". It can, however,
  override anything. <small>In a future version of webber, the "`direc`"
  object for directory "`foo/bar/`" will inherit from the
  directory object for "`bar/`" and only the last one will inherit from
  "`cfg`". But that's not yet coded.</small>
* "`file`" inherits from "`direc`" and again is free to override
  anything on a per-file basis.


= Example =

Due to parsing the [[commandline]] the attribute "`style_dir`" have
some value. If you don't specify one, it will be "default" by default.

Now the [[configuration]] file "`webber.conf`" gets processed. It may
set "`style`" to "twoframe", if you want a two-frame template for your
web-site.

Assuming you have a subdirectory with source-code examples. In this
directory you have a file "`directory.conf`" which re-sets it to "default".
This makes the default template work now only for your source-code
examples.

There's one page where you use the [[hierarchy]] plugin to generate a
sitemap. This one page should have it's own template. Simply make the
[[page|pageformat]] be like this:

	title: Sitemap
	template: sitemap

	<%
	  site = get_linear_sitemap()
	%>
	<ul>
	% for level, page, link in site:
	  <li id="sidemap${level}"><a href="${link}">${page.title}</a></li>
	% endfor
	</ul>
