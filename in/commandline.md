title: Command line options
linktitle: Cmdline
parent: Configuration
lang: en
ctime: 2009-06-24
mtime: 2009-06-26

Note that command line options can also be specified via [[configuration]].

= Invoke help =

As usualy, you can get command line help with "`-h`" or "`--help`":

	$ webber/webber --help
	usage: webber [options]

	options:
	  -h, --help          show this help message and exit
	  -i DIR, --in=DIR    input directory
	  -o DIR, --out=DIR   output directory
	  --style-dir=STYLE   directory with style sheets
	  -v, --verbose       print status messages to stdout
	  -k, --keepgoing     keep going past errors if possible
	  -V, --test_verbose  print status messages to stdout

= Input directory =

"`-i`" or "`--in`" defaults to "`in`" and specifies where webber
search for source files.

You can access this via "`cfg.in_dir`" (or "`file.in_dir`", see
[[inheritance]]).

= Output directory =

"`-o`" or "`--out`" defaults to "`out`" and specifies where webber
writes the output files.


= Template (Style) =

You can define the style of the generated website via HTML templates. If
you have more of them, you switch between different ones via "`--style-dir`".
The default is "`in/style`".


= Verbosity =

A common option is "`-v`" (or "`--verbose`") to increase the verbosity. Repeat
to increase even more.


= Continue on errors =

With "`-k`" or "`--keepgoing`" you can tell webber to ignore errors in one
page and continue with the next page.
