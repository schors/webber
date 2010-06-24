title: Configuration
parent: Webber
ctime: 2009-06-24
mtime: 2009-06-24

Configuration happens either the [[commandline]] or
via the configuration file (described below). All Configurations are
[[inherited|inheritance]] and or overwritable on a per-directory and
per-file basis.

The main means for configuration is the config file:

= Format =

Webber expects a `webber.conf` file in it's root directory. It should look like this:

	template: "default"
	date_format: "%d.%m.%Y"
	input_encoding: "iso-8859-1"
	output_encoding: "iso-8859-1"
	plugins: [
	        "skeleton",
	        "hierarchy",
        	"link",
	        "read_rst",
        	"read_html",
	        "read_copyonly",
        	"read_markdown",
	        "template_mako",
        	]
	plugin_dirs: [
		"my_plugins"
		]
	exclude_dir: [
		"webber.conf",
		"*.tmpl",
	        ]
	exclude_files: [
	        ]

You could also some options with are normally defined by [[commandline]].
This saves you from specifying them on ever run of webber:

	in_dir: "in"
	out_dir: "out"
	style_dir: "in/style"
	verbose: 5

Beside those entries, you can specify any additional entries that will then
be available in your plugins or templates.

= Meaning =

== template ==

Used by the [[template_mako]] to select the template.

== date_format ==

Used in `format_date()`.

== input_encoding ==

Encoding ('utf-8', 'iso-8859-1' etc) used for reading files.

== output_encoding ==

Encoding ('utf-8', 'iso-8859-1' etc) used when writing the final HTML pages.

== plugins ==

List of  to load.

== plugin_dirs ==

List of directories that should be search for [[plugins|Plugins]]. Can be empty or
completely omitted.

== exclude_dirs ==

List of directories below `cfg.in_dir` to skip.

== exclude_files ==

List of files below `cfg.in_dir` to skip.

== in_dir, out_dir, style_dir ==

See [[commandline]].
