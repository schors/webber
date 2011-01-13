title: Page format
parent: Webber
lang: en
ctime: 2009-06-26
mtime: 2010-07-06
change: enhanced section on page body

Every page contains a <a href="#page_header">header</a>, then a blank
line, then the <a href="#page_body">page body</a>. This is the
main text that end up in the rendered HTML page.

The header consists of several keywords, followed by a color and a space,
and the the value. After this, the page body comes.


= Page header =

In the page header, you can define any attribute. Some of those keywords
have special meaning for webber or it's plugins:


== title ==

Full (long) title for the page. End's up in
"`<head><title>...</title></head>`".

Very mandatory. Extremely important. You cannot have a page without a title.
Never. Forget. The. Title.

Here's a [[template_mako]] excerpt that uses this:

	<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="${file.lang}" lang="${file.lang}">
	<head>
	<title>${file.title | entity}</title>
	...
	</head>
	<body>
	<h1>${file.title</h1>
	...
	</html>


== linktitle ==

Sometimes the title is simply too long, e.g. for breadcrumbs. Therefore you
can specify a link-title, which will be used by [[hierarchy]] when generating
breadcrumbs and a side-menu.


== parent ==

Used by [[hierarchy]] to indicate relationship.


== links ==

Used by [[hierarchy]] to indicate relationship. Usually it's better to use
"`parent`" instead.


== order ==

All pages with the same "`parent`" will end up below the parent on the
side-menu (see [[hierarchy]] for details). They will be alphabetically sorted.

If you don't want this default sort order, you can specify your own ordering.

The default order is 100, so anything with a lower order will show up on the
top, anything higher at the bottom of the side-menu.


== ctime ==

Here you can specify an ISO formatted date and or time specifier, which contains
the document creation date/time. Examples:

	ctime: 2009-06-29
	ctime: 2009-06-29 14:33

If you don't specify this, then the documents "`mtime`" will be used instead.


Here's a [[template_mako]] excerpt that uses this:

	<%def name="footer()">\
	<%
	  mtime = format_date(file.mtime)
	  ctime = format_date(file.ctime)
	%>
	<span id="foot">Created\
	% if ctime == mtime:
	 ${mtime} \
	% else:
	 ${ctime}, modified ${mtime} \
	% endif
	</span>
	</%def>\

This uses the named block feature of Mako, you can then place this
text into your template with something like this:

	<div class="content" id="foot">${self.footer()}</div>


== mtime ==

Here you can specify an ISO formatted date and or time specifier, which contains
the document modification date/time. Examples:

	mtime: 2009-06-29
	mtime: 2009-06-29 14:33

If you don't specify this, then the "last-modified"-time from the file-system
will be used instead.

For an example, look at <a href="#ctime">ctime</a> above.


== template ==

Allows you to override the default template. Just specify the pure file
name. For convenience, you can omit "`.tmpl`".

	title: Blog
	template: history


== hide ==

	hide: true

will hide the generated page from in the plugins [[hierarchy]] and [[toc]].


== description ==

Anything you specify here will be accessible in the template as ${description}.
You can use this for HTML meta information, see [[template_mako]].

If you don't specify a description, then ${description} will be the empty string.

Here's a [[template_mako]] excerpt that uses this:

	<head>
	...
	% if len(description):
	<meta name="description" content="${description | entity}" />
	% endif
	...

== keywords ==

Anything you specify here will be accessible in the template as ${keywords}.
You can use this for HTML meta information, see [[template_mako]].

If you don't specify a description, then ${keywords} will be the empty string.

Here's a [[template_mako]] excerpt that uses this:

	<head>
	...
	% if len(keywords):
	<meta name="keywords" content="${keywords | entity}" />
	% endif
	...


== main_url ==

Used by [[google_sitemap]]:

Internally, [[Webber]] works with relative URLs and is quite agnostic
about URL of the final website. However, the [[google_sitemap]] plugin
needs absolute URLs, complete with host name.

Used by [[google_sitemap]]:


== sitemap_priority ==

Used by [[google_sitemap]] to specify a relative important-ness of a page.
Should be between "`0.0`" and "`1.0`" (including).


== sitemap_changefreq ==

Used by [[google_sitemap]] as an estimate about how often a page might change.

Should be one of the following values:

* always
* hourly
* daily
* weekly
* monthly
* yearly
* never


= Your own keywords =

Inside the template, functions and macros you can access all entries
by "`file.XXXX`" and you're free to invent your own keywords:

	title: Impressum
	subtitle: What you should know about this web-site

	Hi, I'm Mario and I won't tell you more about me :-)

Now you can access "`${file.subtitle}`" in your template or
"`params.file.subtitle`" in your [[macros|macros]] and
[[functions|functions]].


= Page body =

== Markdown page body ==

Used for files ending with "`*.md`" and implemented by [[read_markdown]].

Here's an example:

	title: Nothin' about me

	Hi, I'm Holger and I won't tell you more about me :-)


== RST formatted ==

Used for files ending with "`*.rst`" and implemented by
[[read_rst]].



== HTML formatted ==

Used for files ending with "`*.html`" and implemented by [[read_html]].

This is actually <b>not</b> really HTML, only the page body is HTML.
You can use it when RST or Markdown can't format the contents the way
you like it, e.g. when using complex tables.

Here's an example:

	title: Beruflicher Werdegang
	linktitle: Werdegang
	parent: Beruf
	keywords: Lebenslauf, Werdegang
	sitemap_changefreq: yearly
	ctime: 2004-08-30
	mtime: 2009-12-12

	<hr size="1" />
	<a href="#1979">1979</a>
	<a href="#1980">1980</a>
	...
	<hr size="1" />
	...
