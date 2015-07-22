This is a brief set of instruction for use and planned features

# Introduction #

methods/attributes of affycel class
affycel.readcell(): read/import cell file
affycel.version: the version number of the affy cel file, should be 3
affycel.filename: the name of the affy cel file used for this instance of the affcel class
affycel.header: this is a python dictionary of all rows in the header section.
> affcel.header.items() fill return a list of key,value pairs
affycel.intensity: (mask, outliers, modified) are all python record arrays using the same labels
> as found in the cel fine (x, y, mean, stdv, npixcels)
Future Dev
affycel.export(): export intensity (mask....) to simple csv with or without headers
affycel.cdf(): relate the CEL file to corresponding cdf file "affycdf" class

affycdf class



# Details #

Add your content here.  Format your content with:
  * Text in **bold** or _italic_
  * Headings, paragraphs, and lists
  * Automatic links to other wiki pages