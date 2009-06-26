title: Configuration inheritance
linktitle: Inheritance
parent: Webber
ctime: 2009-06-24

= Overview =

Internally, webber uses a bunch of `Holder` classes to store information
(command-line options, config file options, parameters for a directory,
parameters for a file).

Each `Holder` "inherits" configuration entries from the layer above:

* `options` for command-line options
* `cfg` for entries from the command line
* `direc` for information about a directory
* `file` (either directly or via `get_current_file()` for data about the
   currently rendered file

= Example =

Due to parsing the [[command line|commandline]] there will exist an entry
`options.style_dir`.

However, you can also access this same value via `cfg.style_dir`,
`direc.style_dir` and `file.style_dir`. Any one of them however could
over-write the settings that originally was in `options`.

Quite often you'll use this for the page template. In `webber.conf`, you
specify `template: "default"`, which will be used for most pages. Any
page that needs a different template will get `template: history` entry
in it's header.
