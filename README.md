Vainstein K 2020jul27

This file, exactly like documentation of GDB itself, is distributed under the
GNU Free Documentation License (Version 1.3); see the bundled GFDL.html file.


_______________________________________________________________________________
[0] Expected contents of distributed archive are:

	./PrCxx/
				/installer
				/COPYING
				/README
				/HOWTO-USE.html
				/GFDL.html
				/img/
										/*.png
				/end-user.gdbinit
				/developer.gdbinit
				/src/
										/*.py
				/test/
										/run-all
										/test-driver
										/*.{h,cpp}


_______________________________________________________________________________
[1] To install, run the ./PrCxx/installer script; if the GDB you wish to
target is not in your $PATH environment variable, you can supply the
absolute path to that GDB's gdb binary as argument.  The installer script
will:

	a.	copy ./PrCxx/src/*.py to their proper location relative to your GDB
	b.	generate a small .gdbinit file in your $HOME directory
	c.	ask you to source that small .gdbinit from your normal .gdbinit file
	d.	generate ./PrCxx/un-installer script


_______________________________________________________________________________
[2] To use, just start GDB as you normally would; all of PrCxx's facilities
will be auto-loaded and available; message "PrCxx loaded" will confirm that.


_______________________________________________________________________________
[3] To test, run the ./PrCxx/test/run-all script.


_______________________________________________________________________________
[4] To uninstall, run the ./PrCxx/un-installer script.
