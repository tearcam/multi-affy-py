
import csv, os, glob
import sys
import numpy

#running this will import the example.cel file
# It is the way for testing



class affycel:

    def _int_(self, filename, version, header, intensityCells, intensity, maskscells, masks, outlierCells, outliers, modifiedCells, modified):
        self.filename = filename
        self.version = version
        self.header = {}
        self.intensityCells = intensityCells
        self.intensity = intensity
        self.masksCells = maskscells
        self.masks = masks
        self.outliersCells = outlierCells
        self.outliers = outliers
        self.modifiedCells = modifiedCells
        self.modified = modified
        self.custom = {} # plan to allow a custom section to be added to the CEL file
        
    def read_cel(self, filename):
        reader = csv.reader(open(filename, "U"),delimiter='\t')
        self.filename = os.path.split(filename)[1]        
        
        def read_selector(areader):
            for row in areader:
                if row:
                    if any(("[CEL]" in row, "[HEADER]" in row, "[INTENSITY]" in row, "[MASKS]" in row, "[OUTLIERS]" in row, "[MODIFIED]" in row)):
                        rsel[row[0]](row, areader)
                    else: print '*****something went wrong*******'

        def Rcel(row, areader):
            if '[CEL]' in row: #row passed in should contain '[CEL]'
                for row in areader: #Skips '[CEL]' row that was passed in
                    if row: # skips blank rows
                        #print 'cell', row
                        if not any(("[HEADER]" in row, "[INTENSITY]" in row, "[MASKS]" in row, "[OUTLIERS]" in row, "[MODIFIED]" in row)):
                            self.version = int(row[0].partition('=')[2])
                            #print self.version
                            #self.version = row
                        else: 
                            rsel[row[0]](row, areader) # Go to correct section
                    
        def Rheader(row, areader):
            if '[HEADER]' in row: #row passed in should contain '[HEADER]'
                self.header = {} #self.header is a dictionary
                for row in reader: # skips the section heading row
                    if row: #skips blank rows
                        if not any(("[CEL]" in row, "[INTENSITY]" in row, "[MASKS]" in row, "[OUTLIERS]" in row, "[MODIFIED]" in row)):
                            self.header[str(row[0].partition('=')[0])] = str(row[0].partition('=')[2])
                        else:
                            rsel[row[0]](row, areader) # Go to correct section
                
        def Rintensity(row, areader):
            #print 'start intencity', row 
            data = []
            if "[INTENSITY]" in row: #row passed in should contain '[INTENSITY]'
                row = areader.next() # moves to the row after "[INTENSITY]"
                self.intensityCells = int(row[0].partition('=')[2]) #gets the number of intensities
                areader.next() #skips the colmn headings
                for row in reader:
                    if row: 
                        if not any(("[CEL]" in row, "[HEADER]" in row, "[MASKS]" in row, "[OUTLIERS]" in row, "[MODIFIED]" in row)):
                            data.append(tuple(row))
                        else:
                            self.intensity = numpy.array(data, [('x',int),('y',int),('mean',numpy.float64),('stdv',numpy.float64),('npixcels',int)])
                            rsel[row[0]](row, areader)
            
        def Rmasks(row, areader):
            data = []
            maskstype = [('x', int), ('y', int)]
            if "[MASKS]" in row:
                            row = areader.next() # moves to the row after "[INTENSITY]"
                            self.masksCells = int(row[0].partition('=')[2]) #gets the number of intensities
                            areader.next() #skips the colmn headings
            for row in reader:
                if row:
                    if not any(("[CEL]" in row, "[HEADER]" in row, "[INTESITY]" in row, "[OUTLIERS]" in row, "[MODIFIED]" in row)):
                        
                        data.append(tuple(row))
                    else:
                        self.masks = numpy.array(data, [('x',int),('y',int)])
                        rsel[row[0]](row, areader)
            
        def Routliers(row, areader):
            data = []
            if "[OUTLIERS]" in row:
                            row = areader.next() # moves to the row after "[INTENSITY]"
                            self.outliersCells = int(row[0].partition('=')[2]) #gets the number of intensities
                            areader.next() #skips the colmn headings
            for row in reader:
                if row:
                    if not any(("[CEL]" in row, "[HEADER]" in row, "[INTESITY]" in row, "[MASKS]" in row, "[MODIFIED]" in row)):
                        data.append(tuple(row))
                    else:
                        self.outliers = numpy.array(data, [('x', int), ('y', int)])
                        rsel[row[0]](row, areader)
            
        def Rmodified(row, areader):
            data = []
            if "[MODIFIED]" in row:
                            row = areader.next() # moves to the row after "[INTENSITY]"
                            self.modifiedCells = int(row[0].partition('=')[2]) #gets the number of intensities
                            areader.next() #skips the colmn headings
            for row in reader:
                if row:
                    if not any(("[CEL]" in row, "[HEADER]" in row, "[INTESITY]" in row, "[MASKS]" in row, "[OUTLIERS]" in row)):
                        print 'modified1'
                        data.append(tuple(row))
                    #else, there is no else statment when there are now more rows continue on to convert data to array
            self.modified = numpy.array(data, [('x', int), ('y', int), ('origmean', numpy.float64)] )
            #rsel[row[0]](row, areader)  This should be the last item in the file
            
        rsel = {}
        rsel['[CEL]'] = Rcel
        rsel['[HEADER]']= Rheader
        rsel['[INTENSITY]']= Rintensity
        rsel['[MASKS]']= Rmasks
        rsel['[OUTLIERS]']= Routliers
        rsel['[MODIFIED]']= Rmodified
        
        read_selector(reader)
        
if __name__ == "__main__": 
        a = affycel()
        a.read_cel('example.CEL')
        testlist = (a.filename, a.version, a.header.items(), a.intensityCells, a.intensity[:5], a.masksCells, a.masks, a.outliersCells, a.outliers[:5], a.modifiedCells, a.modified[:5])
        for test in testlist:
            print 'Test', test
