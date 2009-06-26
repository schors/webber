# -*- coding: iso-8859-1 -*-
from webber import *
import os, sys, time

f = None

@set_hook("checkconfig")
def checkconfig(params):
	if not cfg.has_key("main_url"):
		error('no "main_url:" configured:')
		error('  this should be something like "www.yourpage.org"')
		sys.exit(1)
	if not cfg.has_key("sitemap_changefreq"):
		warning('no default "sitemap_changefreq:" configured, using default "monthly"')
		cfg.sitemap_changefreq = "monthly"
	if not cfg.has_key("sitemap_priority"):
		warning('no default "sitemap_priority:" configured, using default "0.5"')
		cfg.sitemap_priority = "0.5"


def write_initial(params):
	global f
	try:
		os.makedirs(params.file.out_dir)
	except:
		pass
	f = open(os.path.join(params.file.out_dir, "sitemap.xml"), "w")
	print >>f, '<?xml version="1.0" encoding="UTF-8"?>'
	print >>f, '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
	print >>f, '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
	print >>f, '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9'
	print >>f, '                            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'


@set_hook("scan")
def sitemap_scan(params):
	global f
	file = params.file
	if not file.has_key("linktitle"):
		return
	if f is None:
		write_initial(params)

	# Sanity checks
	ok = True
	try:
		prio = float(file.sitemap_priority)
	except:
		ok = False
	if not ok or (prio < 0.0 or prio > 1.0):
		error("%s: sitemap_priority '%s' is invalid" % (file.rel_path, file.sitemap_priority))
		return
	if file.sitemap_changefreq not in ("always", "hourly", "daily", "weekly", "monthly", "yearly", "never"):
		error("%s: sitemap_changefreq '%s' is invalid" % (file.rel_path, file.sitemap_changefreq))
		return

	#print file.sitemap_priority, file.sitemap_changefreq, file.rel_path
	f.write('<url>\n')
	f.write('   <loc>http://%s/%s</loc>\n' % (file.main_url, file.rel_path))
	f.write('   <lastmod>%s</lastmod>\n' % time.strftime( "%Y-%m-%d", time.localtime(file.mtime)) )
	f.write('   <changefreq>%s</changefreq>\n' % file.sitemap_changefreq)
	f.write('   <priority>%s</changefreq>\n' % file.sitemap_priority)
	f.write('</url>\n')


@set_hook("finish")
def finish(params):
	global f
	if f:
		print >>f, '</urlset>'
		f.close()
