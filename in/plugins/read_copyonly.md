title: Read and copy binary files
linktitle: read_copyonly.py
parent: Plugins
ctime: 2009-06-26

This plugin copies files (e.g. graphics files) into the destination
folder.

To configure which files should be copied you modify
[[webber.conf|configuration]]. An example snippet migth be:

	copy_files: [
	        "*.png",
        	"*.jpg",
	        "*.gif",
	        "*.css",
	        "robots.txt",
	]
