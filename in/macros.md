title: Macros
parent: Webber
lang: en
ctime: 2009-06-24
mtime: 2009-06-26

Macros are executed whenever the sequence
"<code>[</code><code>[!name]]</code>" or "<code>[</code><code>[!name
arg1="1" arg2="2"...]]</code>" is found in a [[source page|pageformat]].

Webber itself doesn't define any macros, that's your task. Use custom
[[Plugins]] for this.


= Defining macros =

A macro is a simply python function which returns HTML. The function needs
to be decorated with "`@set_macro(name)`". There's an example in
[[skeleton.py|skeleton]], which looks like:

	:::python
	@set_macro("sample")
	def sample_macro(params):
        	if cfg.test_verbose:
	                print "in macro skeleton.sample_macro, params:", params
        	return "{ output of sample macro }"

If you call this macro, the returned text "`{
output of sample macro }`" will end up in your HTML file.

Inside the macro, you can access this parameters:

* "`params.name`" contains the name of the macro
* "`params.file`" contains the current "`class File`" object

You can submit additional string arguments, e.g. with
"<code>[</code><code>[!sample arg1="string"]]</code>". Now you get
additionally:

* "`params.arg1`" contains "`string`"

