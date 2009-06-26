title: Create HTML links
linktitle: link.py
parent: Plugins
ctime: 2009-06-26

This plugin converts strings in the form

<pre><code>[</code><code>[url]]
[</code><code>[text|url]]
[</code><code>[#anchor]]
[</code><code>[text|url#anchor]]
</code></pre>

into HTML `<a href=...>` tags.

= Automatic linkification =

Instead of an URL you can also specify the following things:

* the page title
* the short link title
* the basename of the file (filename without extension and directory name)

In this case the link plugin will search throught all pages and take the
first match.

Example:

Suppose you've two file "`testfile.md`" and "`testfile2.md`" which looks like this:

	title: Foo
	linktitle: bar

---

	title: Test2

then the following two links

<pre><code>[</code><code>[Foo]]
[</code><code>[bar]]
[</code><code>[testfile2]]
</code></pre>

will produce two links to the first file and one link to the second file.
All text part of the HTML link will be substituted with the title of the
referred pages, except you specify a text by yourself.
