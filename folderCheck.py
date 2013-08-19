#!/c/Python2.7/python.exe
import os, fnmatch

#walk the current directory searching for a file type
def locate(pattern, root=os.curdir):
    for path, dirs, files in os.walk(root):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(filename + " ", path[2:])

#so I know where I am
print "creating all_found_files.txt"

#creates a text file, all_found_files.txt, with all of the *.tif files matched to their directories
all_found_files = open("all_found_files.txt", "w")
for images in locate("*.tif"):
    print >>all_found_files, images
all_found_files.close()

import string, sys

# clean up all_found_files.txt and check for spaces (and special characters?) in files
def find_space_errors(file):
    entries = {}
    naming_errors_count_space = -1 #start at -1 because the first will get counted twice
    for line in open("all_found_files.txt", "r").readlines():
	try:
	    left, right = line.split() #it breaks here because of spaces
	    try:
		entries[right[1:]].append(left)
	    except KeyError:
		entries[right[1:]] = [left]
	except ValueError:
	    while naming_errors_count_space == -1:
		print "A file or directory probably has a space in it; creating naming-errors_images.txt"
		#I haven't found any errors which would cause it to throw a ValueError other than extra spaces so far
		name_error = open("naming_errors_images.txt", "w")
		print >>name_error, "*****Items with a space in them*****\n"
		name_error.close()
		print "Someone screwed up! naming-errors_images.txt successfully created"
		naming_errors_count_space += 1
	    else:
		name_error = open("naming_errors_images.txt", "a")
		print >>name_error, line
		name_error.close()
		print "But your code is working! Error succesfully added"
		line.replace(" ", "Q") ## replace the spaces with a Q in the stream
		left, delim, right = line.partition("\\") #switch to separating by '\' instead of a space
		#as we've replaced all of the spaces with Q's
		try:
		    entries[right[:-1]].append(left) #added the slice because I was getting a new line on
		#the rights from these entries on the right
		except KeyError:
		    entries[right[:-1]] = [left[:-1]] #added the slice because I was getting a new line on
		#the right and the same thing with an extra space on the end of the lefts
		naming_errors_count_space += 1
    if naming_errors_count_space >= 1:
    	print ("There are %s space naming errors." % naming_errors_count_space)
    return entries

if __name__ == "__main__":
    if len(sys.argv) == 1:
    	result = find_space_errors(sys.stdin)
    else:
    	result = find_space_errors(open(sys.argv[1], "r"))
    total_tiffs = 0
    total_negatives_slides = 0
    total_docs_prints = 0
    total_magicknumbered = 0
    naming_errors_count_identifier = 0
    for rights, lefts in result.iteritems():
	if lefts[0] == "00010001.tif":
	    dirs_with_magicknumbered = open("dirs_with_magicknumbered.txt", "a")
	    print >>dirs_with_magicknumbered, rights
	    dirs_with_magicknumbered.close()
	    total_magicknumbered += 1
	elif lefts[0] == "000100fc.tif":
	    dirs_with_magicknumbered = open("dirs_with_magicknumbered.txt", "a")
	    print >>dirs_with_magicknumbered, rights
	    dirs_with_magicknumbered.close()
	    total_magicknumbered += 1
	elif lefts[0] == "000100tp.tif":
	    dirs_with_magicknumbered = open("dirs_with_magicknumbered.txt", "a")
	    print >>dirs_with_magicknumbered, rights
	    dirs_with_magicknumbered.close()
	    total_magicknumbered += 1
	elif len(lefts) >= 100:
	    for num in range(len(lefts)):
	    	if lefts[num] == (rights + "_%03d.tif" % (num + 1)):
	    	    dirs_with_docs_prints = open("dirs_with_docs_prints.txt", "a")
		    print >>dirs_with_docs_prints, rights
		    dirs_with_docs_prints.close()
		    total_docs_prints += 1
		elif naming_errors_count_identifier == 0:
		    name_error = open("naming_errors_images.txt", "a")
		    print >>name_error, "*****Folder and TIFF names do not match*****\n", rights, lefts
		    name_error.close()
		    naming_errors_count_identifier += 1
		else:
		    name_error = open("naming_errors_images.txt", "a")
		    print >>name_error, rights, lefts
		    naming_errors_count_identifier += 1
	elif len(lefts) >= 2:
	    for num in range(len(lefts)):
	    	if lefts[num] == (rights + "_%02d.tif" % (num + 1)):
	    	    dirs_with_docs_prints = open("dirs_with_docs_prints.txt", "a")
		    print >>dirs_with_docs_prints, rights
		    dirs_with_docs_prints.close()
		    total_docs_prints += 1
		elif naming_errors_count_identifier == 0:
		    name_error = open("naming_errors_images.txt", "a")
		    print >>name_error, "*****Folder and TIFF names do not match*****\n", rights, lefts
		    name_error.close()
		    naming_errors_count_identifier += 1
		else:
		    name_error = open("naming_errors_images.txt", "a")
		    print >>name_error, rights, lefts
		    naming_errors_count_identifier += 1
	if len(lefts) == 1:
	    if (rights + ".tif") == lefts[0]:
	    	negs_slides = open("negs_slides.txt", "a")
		print >>negs_slides, rights
		negs_slides.close()
		total_negatives_slides += 1
	    else:
		while naming_errors_count_identifier == 0:
		    name_error = open("naming_errors_images.txt", "a")
		    print >>name_error, "*****Folder and TIFF names do not match*****\n"
		    name_error.close()
		    naming_errors_count_identifier += 1
		else:
		    name_error = open("naming_errors_images.txt", "a")
		    print >>name_error, rights, lefts
		    name_error.close()
		    naming_errors_count_identifier += 1
	total_tiffs += len(lefts)
    if naming_errors_count_identifier >= 1:
    	print ("There are %s mismatched identifiers." % (naming_errors_count_identifier -1))
    if total_negatives_slides >= 1:
	print ("There are %s TIFFs that appear to be negatives and/or slides." % (total_negatives_slides))
    if total_docs_prints >= 1:
	print ("There are %s TIFFs that appear to be documents and/or prints." % (total_docs_prints))
    if total_magicknumbered >= 1:
	print ("There are %s magicknumbered items" % (total_magicknumbered))
    #creates a text file, numberOfTIFFs, with the number of TIFFs in the folder
    numberOfTIFFs = open("numberOfTIFFs.txt", "w")
    print >>numberOfTIFFs, total_tiffs
    numberOfTIFFs.close()
    print ("There are %s tiffs" % (total_tiffs))

#    for (rights, lefts) in result.items():
#	print >>sorted_num_of_tiffs, ("%02d '%s' %s" % (len(lefts), rights, lefts))
#	print ("%02d '%s' images > %s" % (len(lefts), rights, lefts))

#    sorted_num_of_tiffs = [x for x in result.iteritems()]
#    sorted_num_of_tiffs.sort(key=lambda x: x[0])
