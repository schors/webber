title: Hooks
parent: Webber
ctime: 2009-06-24

= At Startup =

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


= While reading source files =

== read ==

Now webber walks the directory tree specified in "`cfg.in_dir"`, excluding
anything from "`cfg.exclude_dir`" and "`cfg.exclude_file"`. For each of the
remaining files this hook is called.

Usually the the "`read_*`" plugins implement this hook. And usually they look
at the file-extension and decide if they the can procecess this file or not.
If they do, the plugin should also set "`file.render`" is normally "`html"`.
However, it can be something else. In this case "`file.render`" specifies a
hook that get's called for this file.

The first hook that returns contents wins, no other hooks will be called.

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


= After reading files =

At this stage all pages and their meta-information has been read. Now we can
generate additional data, e.g. page hierarchy, tag-clouds, lists of recently
changed files, etc. This is done via the following two hooks.

The webber-supplied plugin [[hierarchy]] uses this
mechanism.

== scan ==

This hook is called once per file with contents:

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" has a "`class File`" object
* "`params.file.contents`" contains the text

== scan_done ==

Finally one "`scan_done`" hook is called. The plugin [[hierarchy]]
uses this to sort links.

* "`params`" is empty.

= While rendering files =

The following hooks are called for each file that has a rendered in
"`file.render`" set. See the "`read"`-hook in how to set it.

If "`file.render`" is "`html"`, then the hooks "`htmlize"`, "`linkify`" and
"`pagetemplate`" are run in this order. Otherwise the hook specified
in "`file.render`" is called.

== htmlize ==

This hook converts contents into HTML.

The first hook that returns HTML, no other hooks will be called.

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" has a "`class File`" object
* "`params.file.contents`" contains the text

== linkify ==

Functions that are called by this hook receive a pre-rendered HTML page.
They can now modify this HTML further, e.g. py converting links to HTML.

They can directly modify params.file.contents and don't need to return anything.

Implemented by the plugin [[link]] and [[toc]].

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" has a "`class File`" object
* "`params.file.contents`" contains the HTML for the body text of the page

== pagetemplate ==

The implementation for this is responsible to generate the final html page,
ready to be written. Implemented by [[template_mako]] plugin.

The first hook that returns a finished HTML page, no other hooks will be
called.

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" has a "`class File`" object
* "`params.file.contents`" contains the HTML for the body text of the page

== copyfile ==

This is one local hook, run instead of the "`htmlize"`, "`linkify`" and
"`pagetemplate`" hooks. It's defined and implemented by the plugin
[[read_copyonly]].

The first hook that returs anything wins, no other hooks will be called.

* "`params.direc`" contains a "`class Directory`" object
* "`params.file`" has a "`class File`" object

= At the end =

Now everythings has been converted to HTML and written out. And we're just
one hook away from finishing webber:

== finish ==

This hook is called at the end of webber's execution. No webber-supplied
plugin uses it currently, but you could use this to save local state into some
file.

* "`params`" is empty
