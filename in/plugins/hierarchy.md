title: Generate hierarchy
linktitle: hierarchy.py
parent: Plugins
ctime: 2009-06-26

This is one of the more complex plugins, used to generate menus and
breadcrumbs. For this, it reads certain keyword from the
[[pageformat]], built an internal parent-child representation.

This is later used for by the functions "`get_breadcrumbs()`" and
"`get_sidemenu()`", which you call from the [[template_mako]].

= Page attributes =

At the "`scan`" [[hook|hooks]], the plugin looks for entries like:

	parent: Home

or

	childs: Cmdline, Inheritance

Here's an example of five pages with different attributes:

---

	title: Homepage
	linktitle: Home

---

	title: Impressum
	parent: Home

---

	title: Job
	parent: Home

---

	title: CV
	parent: Job

---

	title: Knowledge
	parent: Job

---

= Internal representation =

the plugin would populate the variables "`_childs`" and "`_parent`" like this:

	_parent = {
		'Impressum': 'Home',
		'CV': 'Job',
		'Knowledge': 'Job',
		'Job': 'Home'
	}

	_childs = {
		'Home': [(100, 'Job'),
		         (100, 'Impressum')],
		'Job':  [(100, 'CV'),
		         (100, 'Knowledge')]}

That's all you need to generate a sidemap, breadcrumbs or a side-menu.

The pages are first ordered by some number, then by the "`linktitle`". If
a page has no "`linktitle:`" attribute, then the normal title will be used
instead.

If you want to modify the sort-order, simply specify a "`order: 200`" in the
page itself.

= Generation of breadcrumbs =

This is done via a suitable [[template_mako]]. The template uses the
function "`get_breadcrumbs()`" and returns (linktitle, link) tuples. As a
bonus: all the links are always relative to the calling page.

Here's a sample Mako template excerpt:

	<ul>\
	% for page, link in get_breadcrumbs():
	<li><a href="${link}">${page.linktitle}</a></li>\
	% endfor
	</ul>\


= Generation of a side-menu =

This again is done via a suitable [[template_mako]]. The
template uses the function "`get_sidemenu()`" and returns (level,
part_of_path, is_current, title, link) tuples. Again all links are relative
to the calling page.

* "`level`" is the indendation level, starting with 0. You can use this for
  CSS "`id=`" or "`class`" attributes
* "`part_of_path`" is a flag telling you if the mentioned page is part
  of your path, i.e. if the specified page is in the breadcrumbs.
* "`is_current`" is a flag marking the current page.
* "`title`" is the full title for the page
* "`link`" is the relative URL to the page

Here's a sample Mako template excerpt that converts this into a HTML menu:

	<ul id="sidebar">
	% for level, part_of_path, current, page, link in get_sidemenu():
	<li class="sidebar${level}"\
	%    if current:
	 id="sidebar_current">${page.linktitle | entity}</li>
	%    else:
	><a href="${link}">${page.linktitle | entity}</a></li>
	%    endif
	% endfor
	</ul>

= Generate a list of recently changed pages =

To get a list of recently changed pages, do this:

	<%
	  history = get_recently())
	%>
	% if len(history)>1:
	<h2>Recent changed</h2>
	%   for page, link in history:
	%     if page.mtime > page.ctime:
	        Modified ${format_date(page.mtime)}\
	%     else:
	        Created ${format_date(page.ctime)}\
	%     endif
	: <a href="${link}">${page.title | entity}</a><br />
	%   endfor
	% endif


= Generate a sitemap =

To generate a site map for your whole project, do something like
this:

	<%
	  site = get_sitemap()
	%>
	<ul>
	% for level, page, link in site:
	<li id="sidemap${level}"><a href="${link}">${page.title}</a></li>
	% endfor
	</ul>

Now you'd need to use CSS to indent the entries. If you prefer a more
normal "`<ul>..<li><ul><li></li></ul>..</il>`" style, you'd could do this
with some more advanced Mako template magic:

	<%
	  site = get_sitemap()
	  lvl = -1
	%>
	% for level, page, link in site:
	### Adjust level by indenting/detenting via <ul> or </ul>:
	%   while lvl < level:
	<ul><% lvl += 1 %>
	%   endwhile
	%   while lvl > level:
	</ul><% lvl -= 1 %>
	%   endwhile
	### Print out the <li>
	<li id="sidemap${level}"><a href="${link}">${page.title}</a></li>
	% endfor
	### At the end of the sitemap, detent back to level -1
	% while lvl >= 0:
	</ul><% lvl -= 1 %>
	% endwhile
