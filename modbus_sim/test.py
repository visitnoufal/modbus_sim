import pyexcel
import optparse
import ast
import sys

def open_sheet(self, file):
    self.tag_file=file
    return_value = False
    try:
        self.book = pyexcel.get_book(file_name=self.tag_file)
    except Exception, error_message:
	print("\n** ERROR : %s \n\n") % (error_message)
	return return_value
    self.all_sheet_names = self.book.sheet_names()
#    if self.debug:
#        print("\n\nALL Sheet Names (tabs) = %s \n\n") %  self.all_sheet_names
    return_value = True
    return return_value

def close_sheet(self):
    pass

def get_all_tags(self, sheet, col):
    self.sheet_num=sheet
    self.tag_col = col
    sheet = self.book.sheet_by_index(self.sheet_num) # get the sheet num
    header_list = [header for header in sheet.row_at(1)]
    sheet_list = list(set(sheet))
    #print sheet.number_of_rows()

    row_id = 0                                                              # start at row 0
    cell_set = set()

    for current_row in sheet.rows():                                        # iterate through all rows
         cell_value = sheet[row_id, self.tag_col]

#		if self.debug:
	 print("Cell[%s,%s]  = %s") % (row_id, self.tag_col, cell_value)
 	 if cell_value and row_id > 1:                                       # we only want data values after row 2 (zero based)
	     cell_set.add(cell_value)                                        # add unique values to the set only
 	 row_id += 1
 	 row_id = 1




if not open_sheet("/opt/simulator/Dietlin.xlsx"):
    sys.exit()

if self.tag_col > 0:                                               # read & output all tags
    get_all_tags(1,75)

self.close_sheet()

