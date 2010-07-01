title: Page format
parent: Webber
lang: en
ctime: 2009-06-26
mtime: 2009-06-26

Every page contains a header, then a blank line, and then the text that
should show up in the web page.

The header consists of several keywords, followed by a color and a space,
and the the value.

Here's an example:

	title: Impressum

	Hi, I'm Mario and I won't tell you more about me :-)


= Your own keywords =

Inside the template, functions and macros you can access all entries
by "`file.XXXX`" and you're free to invent your own keywords:

	title: Impressum
	subtitle: What you should know about this web-site

	Hi, I'm Mario and I won't tell you more about me :-)

Now you can access "`${file.subtitle}`" in your template or
"`params.file.subtitle`" in your [[macros|macros]] and
[[functions|functions]].


= Overriding configuration =

As "`file`" inherits all configuration from "`cfg`" (see [[inheritance]]),
you can also specify a different template on a per-file basis:

	title: Impressum
	template: boring_bg

	Hi, I'm Mario and I won't tell you more about me :-)


= Webber's keywords =

== title ==

Full (long) title for the page. End's up in
"`<head><title>...</title></head>`".

Very mandatory. Extremely important. You cannot have a page without a title.
Never. Forget. The. Title.

Depending on your template it will also be set inside "`<h1>...</h1>`" at the
start of your web page.


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


== mtime ==

Here you can specify an ISO formatted date and or time specifier, which contains
the document modification date/time. Examples:

	mtime: 2009-06-29
	mtime: 2009-06-29 14:33

If you don't specify this, then the "last-modified"-time from the file-system
will be used instead.


== template ==

Allows you to override the default template. Just specify the pure file
name. For convenience, you can ommit "`.tmpl`".

	title: Blog
	template: history


== hide ==

	hide: true

will hide the generated page from in the plugins [[hierarchy]] and [[toc]].


== description ==

Anything you specify here will be accessible in the template as ${description}.
You can use this for HTML meta information, see [[template_mako]].

If you don't specify a description, then ${description} will be the empty string.


== keywords ==

Anything you specify here will be accessible in the template as ${keywords}.
You can use this for HTML meta information, see [[template_mako]].

If you don't specify a description, then ${keywords} will be the empty string.


== main_url ==

Used by [[google_sitemap]]:

Internally, [[Webber]] works with relative URLs and is quite agonistic about
the final website. However, the [[google_sitemap]] plugin needs absolute URLs,
complete with host name. So we need this configuration ...

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
