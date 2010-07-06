title: Configuration
parent: Webber
lang: en
ctime: 2009-06-24
mtime: 2010-07-06
change: enhanced, fixed and clarified

Configuration happens either via [[commandline]] or with the
configuration file (described below). All configurations are subject
to [[inheritance]]. You can also overwritable any of them on a
per-directory and/or per-file basis.


= Config file format =

Webber expects file named "`webber.conf`" file in the root directory.
It could look like this:

	template: "default"
	date_format: "%d.%m.%Y"
	plugins: [
		"skeleton",
		"hierarchy",
		"link",
		"read_rst",
		"read_html",
		"read_copyonly",
		"read_markdown",
		"template_mako",
		"my_plugin",
		]
	plugin_dirs: [
		"my_plugins"
		]

Options for the [[commandline]] can also be specified in the config file:

	in_dir: "in"
	out_dir: "out"
	style_dir: "in/style"
	verbose: 5

= Webber's configuration =

== in_dir ==

Directory, where the source files (in [[markdown|read_markdown]],
[[rst|read_rst]] or [[html|read_html]] format) reside.

Default: "`in`".

See [[commandline]].


== out_dir ==

Directory where webber creates the output files.

Default: "`out`".

See [[commandline]].


== style_dir ==

Directory where webber reads the [[template_mako]].

Default: "`in/style`".

See [[commandline]] and "`template`".


== template ==

Used by [[template_mako]] to select the template.

Default: `"template`"


== input_encoding ==

Encoding (e.g. 'utf-8', 'iso-8859-1' etc) used when reading [[source pages|pageformat]].

Default: `"iso-8859-1`"


== output_encoding ==

Encoding (e.g. 'utf-8', 'iso-8859-1' etc) used when writing the final HTML pages.

Default: `"iso-8859-1`"


== plugins ==

List of [[Plugins]] to load.


== plugin_dirs ==

List of directories that should be search for [[Plugins]]. Can be empty or
completely omitted.


== exclude_dirs ==

List of directories below "`in_dir`" to skip.

Default: "`[]`"


== exclude_files ==

List of files below "`in_dir`" to skip.

Default: "`['webber.conf', 'directory.conf', '*.tmpl']`"


== date_format ==

Used in `format_date()`. The format is the same as in `"man 2 strftime`".


== verbose ==

How verbose webber should be.

See [[commandline]].


== keep_going ==

If webber should continue after an error.

See [[commandline]].


= Plugin's configuration =

Many [[Plugins]] can use custom options. Read more about them in their
documentation.


= User defined configuration =

Beside those entries, you can specify any additional entries that will
then be available in user-defined [[Plugins]], [[functions]],
[[macros]] or [[template_mako]]. For example, after adding:

	category: "Webber"

you can access in [[template_mako]] with:

	<p>Category: ${page.category}</p>
