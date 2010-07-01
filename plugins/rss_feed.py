# -*- coding: iso-8859-1 -*-
from webber import *
import os, datetime, re
try:
	import PyRSS2Gen
except ImportError:
	print "rss_feed needs the python module PyRSS2Gen"
	raise

items = []
max_age = 0


@set_hook("checkconfig")
def checkconfig(params):
	if not cfg.has_key("rss_file"):
		log('no "rss_file:" configured, using "feed.rss":', 4)
		cfg.rss_file = "feed.rss"
	if not cfg.has_key("rss_max_items"):
		cfg.rss_max_items = 0
	if cfg.has_key("rss_max_age_days"):
		import time
		global max_age
		max_age = int(time.time()) - int(cfg.rss_max_age_days)*86400


# Helper class needed for datetime.datetime to generate GMT timestamps
ZERO = datetime.timedelta(0)
class UTC(datetime.tzinfo):
	"""UTC"""

	def utcoffset(self, dt):
		return ZERO

	def tzname(self, dt):
		return "UTC"

	def dst(self, dt):
		return ZERO
utc = UTC()


@set_hook("scan")
def sitemap_scan(params):
	global items

	file = params.file
	# Only consider new stuff
	if max_age and file["mtime"] < max_age:
		return
	# Ignore non-pages
	if not file.has_key("linktitle"):
		return
	# Ignore hidden pages
	if file.has_key("hide") and file.hide:
		return

	if file.has_key("change"):
		change = file["change"]
	else:
		change = ""

	full_url = "http://%s/%s" % (cfg.main_url, file.out_path)
	item = PyRSS2Gen.RSSItem(
		title = file["title"],
		link = full_url,
		guid = PyRSS2Gen.Guid("%s %s" % (full_url, file["mtime"]), isPermaLink=0),
		description = change,
		pubDate = file["mtime"]
	)
	items.append(item)


@set_hook("finish")
def finish(params):
	global items
	# Sort items by pubDate, which still holds the mtime
	items.sort(key=lambda i: i.pubDate, reverse=True)

	# Limit to requested number
	count = int(cfg.rss_max_items)
	if count:
		items = items[:count]

	# convert mtime to real pupDate
	for i in items:
		i.pubDate = datetime.datetime.fromtimestamp(i.pubDate, utc)

	rss = PyRSS2Gen.RSS2(
		title = cfg.subtitle,
		link = "http://%s" % cfg.main_url,
		description = cfg.subtitle,
		lastBuildDate = datetime.datetime.now(utc),
		items = items,
	)
	# Step one of self-reference
	# (see http://feedvalidator.org/docs/warning/MissingAtomSelfLink.html)
	rss.rss_attrs["xmlns:atom"] = "http://www.w3.org/2005/Atom"

	try:
		os.makedirs(cfg.out_dir)
	except:
		pass
	f = open(os.path.join(cfg.out_dir, cfg.rss_file), "w")
	# Ugly XML beautification
	s = rss.to_xml()
	s = re.sub("<(?!/)", "\n<", s)
	s = s.replace("\n\n", "\n")
	# Step two of self-reference
	s = s.replace('<channel>', '<channel>\n<atom:link href="http://%s/%s" rel="self" type="application/rss+xml" />' % (cfg.main_url, cfg.rss_file))
	f.write(s[1:])
	f.write("\n")
