# -*- coding: iso-8859-1 -*-
from webber import *
import os, fnmatch


@set_hook("read")
def read(params):
	file = params.file
	#print "file:", file.rel_path
	for c in cfg.copy_files:
		if fnmatch.fnmatchcase(file.rel_path, c):
			#print "Copy:", file.rel_path
			file.render = "copyfile"
			file.contents = ""

@set_hook("copyfile")
def copyfile(params):
	file = params.file
	log("copying file %s" % file.rel_path, level=7)
	out_path = os.path.join(cfg.out_dir, file.rel_path)
	out_dir  = os.path.split(out_path)[0]
	try:
		os.makedirs(out_dir)
	except OSError:
		pass
	cmd = "cp -l %s %s" % (
		os.path.join(cfg.in_dir, file.rel_path),
		out_path
		)
	#print cmd
	os.system(cmd)
