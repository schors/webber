title: Hooks
parent: Webber
lang: en
ctime: 2009-06-24
mtime: 2010-07-06
change: new introductory text about hooks

Webber can read and use any number of [[Plugins]], even user-supplied.
Therefore, while writing "`webber.py`", it was not clear which plugins
will exist. So a flexible way to share data between "`webber.py`" and
the plugins was needed.

Borrowed from IkiWiki came the idea of "Hooks". At various points
during the execution "`webber.py`" fires some hooks. Any plugin can act
to any hook and has a chance to get the current page or configuration
attributes.

It can then generate local data, change page attributes, generate HTML
or whatever else is needed.


= How to implement hooks =

When you program your own [[Plugins]], you simply write python
functions and mark then with the "`@set_hook(name)`" Decorator. See
the Example at <a href="#addoptions">addoptions</a> below.


= Hooks fired at startup =

When you start "`webber`", the following hooks are executed:

== addoptions ==

Can be used by plugins to add their own command line options.

"`params.parser`" contains the "`optparse`" based parser.

Example:

	:::python
	@set_hook("addoptions")
	def test_addoptions(params):
		params.parser.add_option("-V", "--test_verbose", action="count",
			dest="test_verbose", default=0,
			help="print status messages to stdout")

== checkconfig ==

After the command-line options have been processed and incorporated into
config object, this hook is called. Here each plugin can check if the
specified configurations are sane.

* "`params`" is empty, you should use "`cfg`" directly:

Example:

	:::python
	@set_hook("checkconfig")
	def test_checkconfig(params):
		if cfg.test_verbose:
			print "WARNING: I'll be now much more noisy"
		# I could also directly modify the configuration:
		cfg.foo = "mooh"

== start ==

This hook is called just before walking the directory tree.

* "`params`" is empty:

Example:

	:::python
	@set_hook("start")
	def test_start(params):
		print "in start hook"


= Hooks fired while reading source files =

For each file read, the following hooks are fired:

== read ==

Now webber walks the directory tree specified in "`cfg.in_dir"`, excluding
anything from "`cfg.exclude_dirs`" and "`cfg.exclude_files"`. For each of the
remaining files this hook is called.

Usually the the "`read_*`" plugins implement this hook. And usually they look
at the file-extension and decide if they the can proprocecess this file or not.
If they do, the plugin should also set "`file.render`" is normally "`html"`.
However, it can be something else. In this case "`file.render`" specifies a
hook that gets called for this file.

The first hook that returns contents wins, no further hook-functions
will be called.

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" contains a "`class File`" object

Example:

	:::python
	@set_hook("read")
	def read(params):
		file = params.file
		if file.rel_path.endswith(".html"):
			file.render = "html"
			f = file.read_keywords()
			return f.read()

== filter ==

Any file that got read will be filtered. At this stage the text is still in the
original format.

Currently no webber-supplied plugin implements this.

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" contains a "`class File`" object
* "`params.contents`" contains the text

Example:

	:::python
	@set_hook("filter")
	def filter(params):
		params.content = params.content.replace("e", "EEEEE")


= Hooks fired after files are read =

Now all pages and their meta-information has been read.

The following hooks allow plugins to use this data and generate
additional data, e.g. a page hierarchy, tag-clouds, lists of recently
changed files, etc.

For example, the plugin [[hierarchy]] uses this mechanism.

== scan ==

This hook is called once per file with contents:

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" has a "`class File`" object
* "`params.file.contents`" contains the text

== scan_done ==

Finally one "`scan_done`" hook is called. The plugin [[hierarchy]]
uses this to sort links.

* "`params`" is empty.


= Hooks fired while creating HTML =

The following hooks are called for each file that renders itself. This is indicated
by the "`file.render`" attribute. See the "`read"`-hook on how to set that.

If "`file.render`" is "`html"`, then the hooks "`htmlize"`, "`linkify`" and
"`pagetemplate`" are run (in that order).

Otherwise the hook specified in "`file.render`" is called. This can
even be a custom hook.

== htmlize ==

This hook converts contents into HTML.

If more than one plugin receive this hook, then the first function
returning HTML "wins". No other hook-functions will be called
afterwards.

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" has a "`class File`" object
* "`params.file.contents`" contains the text

== linkify ==

Functions that are called by this hook receive a pre-rendered HTML page.
They can now modify this HTML further, e.g. py converting links to HTML.

They can directly modify params.file.contents and don't need to return
anything.

Implemented by the plugin [[link]] and [[toc]].

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" has a "`class File`" object
* "`params.file.contents`" contains the HTML for the body text of the page

== pagetemplate ==

The implementation for this is responsible to generate the final html page,
ready to be written. Implemented in the [[template_mako]] plugin.

The first hook that returns a finished HTML page wins, no further
hook-functions will be called.

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" has a "`class File`" object
* "`params.file.contents`" contains the HTML for the body text of the page

== copyfile ==

This is an example of a plugin-defined hook. It's run instead of the
"`htmlize"`, "`linkify`" and "`pagetemplate`" hooks by virtue of the
"`file.render`" attribute.

It's defined and implemented by the plugin [[read_copyonly]].

The first hook that returns anything wins, no further hook-functions
will be called.

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" has a "`class File`" object

= At the end =

Now everything has been converted to HTML and written out. And we're just
one hook away from finishing program execution:

== finish ==

This hook is called at the end of webber's execution.

* "`params`" is empty

Plugins that use this are [[link]] (to warn about wrong links),
[[google_sitemap]] (to generate the "`sitemap.xml`" file) and [[rss_feed]]
(to generate the "`feed.rss`" file).
