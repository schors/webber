title: Generate table of contents
linktitle: toc.py
parent: Plugins
ctime: 2010-06-23
change: make get_toc() work like get_recently()

This plugin analyzes the HTML header statements (h1, h2, h3 ...) and
generates a table of contents based on this information.

= Configuration =

== toc_min_lines ==

A page needs with less lines than specified won't get a table-of-contents.

You can use this if you paste the table-of-contents to some screen
corner, and don't want the clutter the display if the HTML page is
very short anyway.

If not specified, this defaults to 30.


= Internal representation =

Given this HTML ...

	<h2>Calling macros</h2>
	<h3>Example</h3>
	<h2>Defining macros</h2>


... the plugin populates the variable "`_toc`" like this:

	_toc = [
	    (2, "Calling macros", "calling_macros"),
	    (3, "Example", "example"),
	    (2, "Defining macros", "defining_macros"),
	]

... where the first item is the level (h1, h2, etc). The
second item is the headline and the last element is a so-called
[[slug|http://en.wikipedia.org/wiki/Slug_(web_publishing)]], used for
local anchors.


= Generation of a table-of-contents =

This again is done via a suitable [[template_mako]]. The template uses
the function "`get_toc()`" and returns (level, headline, slug) tuples.

* "`level`" is the indendation level, starting with 0. You can use
  this for CSS "`id=`" or "`class`" attributes
* "`headline`" is the headline (the text inside <hX>..</hX>)
* "`slug`" is the
  [[slug|http://en.wikipedia.org/wiki/Slug_(web_publishing)]] that can
  be used for link creation

== Example template ==

Here's a sample [[Mako template|template_mako]] excerpt that converts
this into a HTML:

	<ul id="toc">
	% for level, headline, link in toc:
	        <li class="toc${level}"><a href="${link}">${headline | entity}</a></li>
	% endfor
	</ul>


== Example CSS ==

Finally, you use some CSS to format the table-of-contents to your
liking, e.g. with this:

	#toc, #toc ul {
	        list-style-type: none;
	        overflow: hidden;
	        padding: 0;
	        margin: 0;
	}
	#toc {
	        font-size: 90%;
	}
	#toc li {
	        width: 100%;
	        text-align: right;
	}

        .toc1 { padding-left: 1em; }
        .toc2 { padding-left: 2em; }
