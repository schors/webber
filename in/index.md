title: Webber
lang: en
ctime: 2009-06-24
mtime: 2010-07-06
change: added Tutorial

*Webber* is a <b>static</b> web-site generation tool, loosely based on ideas
from IkiWiki and my own likings.

It works by ...

 * reading one [[configuration file|configuration]]
 * reading one or more [[page files|pageformat]]
 * considering any number of [[plugins|Plugins]]
 * execution of [[macros|macros]]
 * execution of [[hooks|hooks]]
 * rendering through a [[template|template_mako]], using [[functions|functions]]

Finally webber creates static HTML files that you can upload to your
web-site. I recommend [[sitecopy|http://www.manyfish.co.uk/sitecopy/]]
for this.

= Tutorial =

First, make an empty directory and change into it:

	$ mkdir web
	$ cd web

Then, get webber:

	$ git clone --depth 1 git://gitorious.org/webber/webber.git

Now we need a directory for our input files and output files:

	$ mkdir in out

and create our first page using your favorite ${EDITOR}. It should
look like this:

	$ ${EDITOR} in/index.conf
	$ cat in/index.md
	title: Nothin' about me

	Hi, I'm Holger and I won't tell you more about me :-)

I'm using [[markdown|read_markdown]] here (you can also use
[[RST|read_rst]] or [[HTML|read_html]], or even have some pages in one
format and other pages in another format).

Now, webber needs a simple [[config file|configuration]]. Create one,
it should be similar to this:

	$ ${EDITOR} webber.conf
	$ cat webber.conf
	template: "default"
	plugins: [
		"link",
		"read_markdown",
		"template_mako",
		]

As you see, we specified a [[template|template_mako]]. That's a HTML
skeleton that webber fills out. Let's create a very simple one:

	$ mkdir in/style
	$ ${EDITOR} in/default.tmpl
	$ cat in/default.tmpl
	<html>
	<head>
	<title>${file.title | entity}</title>
	<meta http-equiv="Content-Type" content="text/html; charset=${file.output_encoding}"/>
	</head>
	<body>
	<h1>${file.title | entity}</h1>
	${body}
	</body>
	</html>

And finally, we can run webber without any [[command line options|commandline]]:

	$ webber/webber
	info: Reading files ...
	info: Scanning files ...
	info: Rendering files ...

If "`webber/webber`" is too cumbersome to type, just do this:

	$ ${EDITOR} Makefile
	$ cat Makefile
	all:
		webber/webber

Now can can simply type "`make`".

Now you wonder what file has been produced?  Let's see:

	$ cat out/index.html
	<html>
	<head>
	<title>Nothin' about me</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
	</head>
	<body>
	<h1>Nothin' about me</h1>
	<p>Hi, I'm Holger and I won't tell you more about me :-)</p>

	</body>

You make things way more complex, but that's basically it.


= More Info =

* [[pageformat]]
* [[configuration]]
 * [[commandline]]
 * [[inheritance]]
* [[inheritance]]
* [[Plugins]]
 * [[read_rst]]
 * [[read_markdown]]
 * [[read_html]]
 * [[read_copyonly]] (e.g. images)
 * [[link]]
 * [[hierarchy]]
 * [[template_mako]]
 * [[skeleton]]
 * [[google_sitemap]]
 * [[rss_feed]]
 * [[skeleton]]
* [[hooks]]
* [[functions]]
* [[macros]]
