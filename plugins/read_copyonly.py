# -*- coding: iso-8859-1 -*-
from webber import *
import os, shutil, fnmatch


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
	log.info("copying file %s" % file.rel_path)
	out_path = os.path.join(cfg.out_dir, file.rel_path)
	out_dir  = os.path.split(out_path)[0]
	try:
		os.makedirs(out_dir)
	except OSError:
		pass
	try:
		shutil.copy(os.path.join(cfg.in_dir, file.rel_path), out_path)
	except:
		os.remove(out_path)
		shutil.copy(os.path.join(cfg.in_dir, file.rel_path), out_path)
	shutil.copystat(os.path.join(cfg.in_dir, file.rel_path), out_path)
