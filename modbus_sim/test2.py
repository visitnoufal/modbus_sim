import pyexcel
book = pyexcel.get_book(file_name="/opt/simulator/Dietlin.xlsx")
all_sheet_names = book.sheet_names()
