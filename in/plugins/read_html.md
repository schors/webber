title: Read HTML
linktitle: read_html.py
parent: Plugins
ctime: 2009-06-26

This plugin reads HTML snippets from "`*.html`" files.

Please note that currently the plugin assumes that this is a HTML snippet.
That means: the snippes should only contain what is inside "`<body>`" and
"`</body>`", but without those tags themselfes.

A sample "`test.html`" document looks like this:

	title: Job
	parent: Home
	ctime: 2008-10-01

	<p>What I did in the past:<P>
	<!-- to be continued -->

You'll find more about "`title:`", "`parent:`" and "`ctime:`" in the
[[page format|pageformat.html]] description.
