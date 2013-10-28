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
    for tiffs in locate("*.tif"):
        file, folder = tiffs.split() #it breaks here with a ValueError because of spaces in folder/filenames
        try:
            entries[folder[1:]].append(file)
        except KeyError:
            entries[folder[1:]] = [file]
    return entries

def naming_errors_zero():
    """ creates the naming errors text file """
    name_error = open("naming_errors_images.txt", "w")
    print >>name_error, "*****Folder and TIFF names do not match*****\n", folders
    name_error.close()
    naming_errors += 1

def naming_errors():
    """ appends folders with naming errors to the already created text """
    name_error = open("naming_errors_images.txt", "a")
    print >>name_error, folders
    name_error.close()
    naming_errors += 1

def main():
    """ Check identifiers against the folder name
    
    Magicknumbers will be tested for first, by checking images[0] against the usual
    use cases. Then checking for over 100 images in a folder against 3 digit filenames,
    2-99 images against 2 digit filenames, negatives/slides, and finally if the folder
    is empty it is added to a text file. Still need to add serialized images to the list
    """
    total_tiffs = 0
    total_negatives_slides = 0
    total_docs_prints= 0
    total_magicknumbered = 0
    naming_errors = 0
    result = build_dict()
    for folders, images in result.iteritems():
	if images[0] == "00010001.tif":
	    total_magicknumbered += 1
	elif images[0] == "000100fc.tif":
	    total_magicknumbered += 1
	elif images[0] == "000100tp.tif":
	    total_magicknumbered += 1
	elif len(images) >= 100:
	    for num in range(len(images)):
	    	if images[num] == (folders + "_%03d.tif" % (num + 1)):
		    total_docs_prints += 1
		elif naming_errors == 0:
		    naming_errors_zero()
		else:
		    naming_errors()
	elif len(images) >= 2:
	    for num in range(len(images)):
	    	if images[num] == (folders + "_%02d.tif" % (num + 1)):
		    total_docs_prints += 1
		elif naming_errors == 0:
		    naming_errors_zero()
		else:
		    naming_errors()
	elif len(images) == 1:
	    if (folders + ".tif") == images[0]:
		total_negatives_slides += 1
	    else:
		while naming_errors_count_identifier == 0:
		    naming_errors_zero()
		else:
		    naming_errors()
	elif len(images) == 0:
		no_tiffs = open("no_tiffs.txt", "a")
                print >>no_tiffs, folders
                no_tiffs.close()
                print "There are directories without tiffs"
                print "cat no_tiffs.txt to see these folders"
	total_tiffs += len(images)
    if naming_errors >= 1:
    	print ("There are %s mismatched identifiers." % (naming_errors))
    	print "cat naming_errors to see folders with problems"
    if total_negatives_slides >= 1:
	print ("There are %s TIFFs that appear to be negatives and/or slides." % (total_negatives_slides))
    if total_docs_prints >= 1:
	print ("There are %s TIFFs that appear to be documents and/or prints." % (total_docs_prints))
    if total_magicknumbered >= 1:
	print ("There are %s magicknumbered items" % (total_magicknumbered))
    print ("There are %s TIFFs" % (total_tiffs))

if __name__ == "__main__":
    main()
