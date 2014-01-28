#!/c/Python2.7/python.exe

#modules to import
import os, fnmatch, string, sys

#functions
def locate(pattern, root=os.curdir):
    """ walk the current directory searching for a file type """
    for path, dirs, files in os.walk(root):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(filename + " ", path[2:])

def build_dict():
    """ walk directory and build dictionary """
    entries = {}
    space_errors = 0
    for tiffs in locate("*.tif"):
        try:
            file, folder = tiffs.split() #it breaks here with a ValueError because of spaces in folder/filenames
            try:
                entries[folder[1:]].append(file)
            except KeyError:
                entries[folder[1:]] = [file]
        except ValueError:
            spaces = open("spaces.txt", "a")
            print >> spaces, tiffs
            spaces.close()
            tiffs.replace(" ", "Q") #replace the spaces with a Q in the stream
            file, delim, folder = tiffs.partition("\\") #switch to separating by '\' instead of
            #a space as all of the spaces were replaced with Q's
            try:
                entries[folder[:-1]].append(file) #added the slice because I was getting a new line
                #on the folders from these entries
            except KeyError:
                entries[folder[:-1]] = [file[:-1]] #added the slice because I was getting a new line
                #on the folders and an extra space at the end of the lefts
    return entries

def main():
    total_tiffs = 0
    total_negatives_slides = 0
    total_docs_prints= 0
    total_magicked = 0
    naming_errors = 0
    result = build_dict()
    for folders, images in result.iteritems():
	if images[0] == "00010001.tif":
            magicked = open("magicked.txt", "a")
            print >>magicked, folders
            magicked.close()
            total_magicked += 1
	elif images[0] == "000100fc.tif":
	    magicked = open("magicked.txt", "a")
            print >>magicked, folders
            magicked.close()
            total_magicked += 1
	elif images[0] == "000100tp.tif":
	    magicked = open("magicked.txt", "a")
            print >>magicked, folders
            magicked.close()
            total_magicked += 1
	elif len(images) >= 100:
	    for num in range(len(images)):
	    	if images[num] == (folders + "_%03d.tif" % (num + 1)):
		    total_docs_prints += 1
		elif naming_errors == 0:
		    name_error = open("naming_errors.txt", "w")
                    print >>name_error, "*****Folder and TIFF names do not match*****\n", folders
                    name_error.close()
                    naming_errors += 1
		else:
		    name_error = open("naming_errors.txt", "a")
                    print >>name_error, folders
                    name_error.close()
                    naming_errors += 1
	elif len(images) >= 2:
	    for num in range(len(images)):
	    	if images[num] == (folders + "_%02d.tif" % (num + 1)):
		    total_docs_prints += 1
		elif naming_errors == 0:
		    name_error = open("naming_errors.txt", "w")
                    print >>name_error, "*****Folder and TIFF names do not match*****\n", folders
                    name_error.close()
                    naming_errors += 1
		else:
		    name_error = open("naming_errors.txt", "a")
                    print >>name_error, folders
                    name_error.close()
                    naming_errors += 1
	if len(images) == 1:
	    if (folders + ".tif") == images[0]:
		total_negatives_slides += 1
	    else:
		while naming_errors == 0:
		    name_error = open("naming_errors.txt", "w")
                    print >>name_error, "*****Folder and TIFF names do not match*****\n", folders
                    name_error.close()
                    naming_errors += 1
		else:
		    name_error = open("naming_errors.txt", "a")
                    print >>name_error, folders
                    name_error.close()
                    naming_errors += 1
	total_tiffs += len(images)
    if naming_errors >= 1:
    	print ("There are %s mismatched identifiers." % (naming_errors))
    	print "enter 'cat naming_errors.txt' to see the errors"
    	print '''enter cat naming_errors.txt | tail -n +2 | while read x junk; do echo "$x"; done > folders.txt; sort -u folders.txt > errors.txt' for a nice display of folders with problems'''
    if total_negatives_slides >= 1:
	print ("There are %s TIFFs that appear to be negatives and/or slides." % (total_negatives_slides))
    if total_docs_prints >= 1:
	print ("There are %s TIFFs that appear to be documents and/or prints." % (total_docs_prints))
    if total_magicked >= 1:
	print ("There are %s magicknumbered items" % (total_magicked))
	print "enter 'cat magicked.txt' to see the magicknumbered items"
    print ("There are %s TIFFs" % (total_tiffs))



if __name__ == "__main__":
    main()
