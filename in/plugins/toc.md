title: Generate table of contents
linktitle: toc.py
parent: Plugins
ctime: 2010-06-23

This plugin analyzes the HTML header statements (h1, h2, h3 ...) and
generates a table of contents based on this information.

= Configuration =

== toc_min_lines ==

A page needs with less lines than specified won't get a table-of-contents.

You can use this if you paste the table-of-contents to some screen
corner, and don't want the clutter the display if the HTML page is
very short anyway.

If not specified, this defaults to 30.


= Usage example =

with this HTML:

	<h2>Calling macros</h2>
	<h3>Example</h3>
	<h3>Defining macros</h2>

the table-of-contents will be like this:

	<ul id="toc">
	  <li><a href="#calling_macros">Calling macros</a></li>
          <ul>
	    <li><a href="#example">Example</a></li>
	  </ul>
	  <li><a href="#defining_macros">Defining macros</a></li>
	</ul>

While doing this, it also modifies the HTML file contents to look like this:

	<h2>Calling macros<a name="calling_macros">&nbsp;</a></h2>
	<h3>Example<a name="example">&nbsp;</a></h3>
	<h2>Defining macros<a name="defining_macros">&nbsp;</a></h2>

== Accessing the TOC ==

Use "`${get_toc()}`" in your [[template|template_mako]] to access
the generated HTML.


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
