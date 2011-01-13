title: Read and copy binary files
linktitle: read_copyonly.py
parent: Plugins
lang: en
ctime: 2009-06-26
mtime: 2010-04-23

This plugin copies files (e.g. graphics files) into the destination
folder.

To configure which files should be copied you modify
[[webber.conf|configuration]]. An example snippet might be:

	copy_files: [
	        "*.png",
        	"*.jpg",
	        "*.gif",
	        "*.css",
	        "robots.txt",
	]
