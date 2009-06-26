title: Google Sitemap generation
linktitle: google_sitemap.py
parent: Plugins
keywords: Google, XML, Sitemap generator
ctime: 2009-06-26

This plugins write an XML "`sitemap.xml`" file into the out-directory. The
format is documented at [[http://www.sitemaps.org]].


= Configuration =

The sitemap generator needs three [[Configuration]] items:

	main_url: "www.holgerschurig.de"
	sitemap_changefreq: "monthly"
	sitemap_priority: 0.5


== main_url ==

This is the main URL of your website, without the "`http://`" stuff.


== sitemap_changefreq ==

You can define an estimated change frequency on each page by specifying
this keyword at the header of each [[page|Page format]]. However, the
"`sitemap_changefreq`" from the configuration file will be used as a
default.


== sitemap_priority ==

You can define an relative page importance on each page by specifying
this keyword at the header of each [[page|Page format]]. However, the
"`sitemap_priority`" from the configuration file will be used as a
default.


= robots.txt =

Please note that you'll also specify the sitemap in your "`robots.txt`" file,
e.g.:

	User-agent: *
	Disallow: /logs/
	Sitemap: http://www.holgerschurig.de/sitemap.xml

Also make sure that your "`robots.txt`" file get's copied, by adding

	copy_files: [
		...
		"robots.txt",
		...
	]

to "`webber.conf`".
