title: RSS feed generator
linktitle: rss_feed.py
parent: Plugins
keywords: RSS
lang: en
ctime: 2010-06-23
mtime: 2010-06-23

This plugins write an XML file "`feed.rss`" (can be changed) into the
out-directory. The format is according to the RSS feed documentation
at [[http://www.rssboard.org/rss-specification]].


= Configuration =

Please make sure to enable this plugin:

	plugins: [
	         ...
	        	"rss_feed",
	        ]


After this, the following three [[Configurations|configuration]] are
available:

== rss_file ==

The rss feed can use the configuration entry `rss_file` to specify the
path of the generated file.

	rss_file: "rss.xml"

The default is "`feed.rss`".


== rss_max_items ==

Here you can specify how many items (articles) are written into the
RSS feed.

	rss_max_items: 10

If you don't configure this, then the number of published articles
won't be limited.


== rss_max_age_days ==

Here you specify (in days) how young an article must be in order to be
published via RSS.

	rss_max_age_days: 28

If you don't configure this, then any article will be limited,
regardless of it's age.


= Support in the template =

Your [[template|Mako template]] should mention your rss feed. One possible solution
is this:

	<head>
	...
	<link rel="alternate" type="application/rss+xml" title="RSS" href="${rootpath}feed.rss" />
	</head>


= Example of output =

	<?xml version="1.0" encoding="iso-8859-1"?>
	<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
	<channel>
	<atom:link href="http://www.holgerschurig.de/feed.rss" rel="self" type="application/rss+xml" />
	<title>Holger Schurig's Computer Calisthenics &amp; Orthodontia</title>
	<link>http://www.holgerschurig.de</link>
	<description>Holger Schurig's Computer Calisthenics &amp; Orthodontia</description>
	<lastBuildDate>Wed, 23 Jun 2010 08:59:24 GMT</lastBuildDate>
	<generator>PyRSS2Gen-1.0.0</generator>
	<docs>http://blogs.law.harvard.edu/tech/rss</docs>
	<item>
	<title>QtIAX</title>
	<link>http://www.holgerschurig.de/qtiax.html</link>
	<description></description>
	<guid isPermaLink="false">http://www.holgerschurig.de/qtiax.html 1260652641</guid>
	<pubDate>Sat, 12 Dec 2009 21:17:21 GMT</pubDate></item></channel></rss>

