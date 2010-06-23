# -*- coding: iso-8859-1 -*-
from webber import *
import htmlentitydefs, re


reHeader = re.compile(r'<h(\d)(.*)>(.*)</h\1>', re.IGNORECASE | re.MULTILINE)
toc = []
labels = {}


toc_min_lines = 30


@set_hook("checkconfig")
def checkconfig(params):
	if cfg.has_key("toc_min_lines"):
		global toc_min_lines
		toc_min_lines = int(cfg.toc_min_times)


def slugify(text, separator):
    """Based on http://snipplr.com/view/26266/create-slugs-in-python/"""

    ret = ""
    for c in text.lower():
        try:
            ret += htmlentitydefs.codepoint2name[ord(c)]
        except:
            ret += c
    ret = re.sub("([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)", r"\1", ret)
    ret = re.sub("\W", " ", ret)
    ret = re.sub(" +", separator, ret)
    return ret.strip()


def repl(m):
    global toc
    label = slugify(m.group(3), "_")
    if labels.has_key(label):
        n = 0
        while True:
            l = "%s_%d" % (label, n)
            if not labels.has_key(l):
                label = l
                break
            n += 1

    toc.append( (label, int(m.group(1))-1, m.group(3)) )
    return '<h%s%s>%s<a name="%s">&nbsp;</a></h%s>' % (
        m.group(1),
        m.group(2),
        m.group(3),
        label,
        m.group(1))


@set_hook("linkify")
def linkify(params):
    global toc
    global labels
    toc = []
    labels = {}

    # Very small pages don't need a table-of-contents
    if params.file.contents.count("\n") < toc_min_lines:
        return

    params.file.contents = reHeader.sub(repl, params.file.contents)



@set_function("get_toc")
def get_toc():
    level = 1
    res = []
    res.append('<ul id="toc">')
    for (label, lvl, txt) in toc:
        while lvl > level:
            res.append("%s<ul>" % ("  "*level))
            level += 1
        while lvl < level:
            level -= 1
            res.append("%s</ul>" % ("  "*level))
        res.append('%s<li><a href="#%s">%s</a></li>' % ("  " * level, label, txt))
    while level:
        level -= 1
        res.append("%s</ul>" % ("  "*level))
    return "\n".join(res)
