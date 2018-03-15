import pyexcel
import optparse
import ast
import sys

################################################################################
# parse_arguments
#
#  Setup and validate the command-line arguements for the script
#
#  Returns :
#  structure of the command-line args
#
################################################################################
def parse_arguments(show_help=False):
    """ Option parser - Setup command-line options"""

    usage_text = "Usage: %prog --file excel_sheet.xlsx  --tag_col nn  [--get_tags] [--debug] [--help]"
    description_text = "Alpha Ori Automation."
    version_text = "%prog  v1.1.1 February 2018"
    epilog_text = "(c) 2018 Alpha Ori Ltd"

    # create option parser object
    parser = optparse.OptionParser(usage=usage_text,
                                   version=version_text,
                                   description=description_text,
                                   epilog=epilog_text)

    # general parameters
    general_opts = optparse.OptionGroup(parser, 'General Parameters', 'Running options :',)


    general_opts.add_option("--file", action="store",
                            dest="file", default=None,
                            help="The Excel file of TAGS.")

    general_opts.add_option("--max_output", action="store",
                            dest="max_output", default=50, type=int,
                            help="The maximum values to output.")

    general_opts.add_option("--tag_col", action="store",
                            dest="tag_col", default=0, type=int,
                            help="The column that contains the TAG Info.  Use : --get_tags to display columns -> Look for 'Tag Name in DB'. Then use : --tag_col nn ")

    general_opts.add_option("--sheet", action="store",
                            dest="sheet_num", default=1, type=int,
                            help="The TAB Sheet that contains the TAG Info.  Default = 1.")

    general_opts.add_option("--debug", action="store_true", dest="debug_flag",
                            default=False, help="Run script in debug mode - increased screen output. DEFAULT = False.")

    general_opts.add_option("--get_tags", action="store_true", dest="tag_flag",
                            default=False, help="Run Show All Column Headings -  DEFAULT = False.")


    parser.add_option_group(general_opts)                                       # add general options

    (options, args) = parser.parse_args()


# Quick Error Checks on values :

    if not options.file:                                                        # if filename is not given
        show_help = True
        print('\n\n** Error : File not given.  Use: --file excelFile.xlsx\n\n')

    if show_help:                                                               # if --help on cmd-line, show help exit
        parser.print_help()
        sys.exit()


    return options                                                              # send back all of the options




class TagSheets():

    def __init__(self, config_info):
        """
        Read a column from an Excel Spreadsheet and output column values (tags)

        :param config_info:  command-line arguments as instance
        """

        self.debug = config_info.debug_flag
        self.max_output = config_info.max_output                                # use to limit amount of output
        self.tag_file = config_info.file
        self.tag_col = config_info.tag_col
        self.sheet_num = config_info.sheet_num

        if self.debug:
            config_dict = ast.literal_eval(str(config_info))                    # convert config_info from instance to dict to print
          #  self.util_lib.DumpData(config_dict, "\n ** setUpClass - Running Parameters in config_info **\n")
            print("\n ** __init__ - Running Parameters in config_info **\n")
            print config_dict
            print


    def open_sheet(self):

        return_value = False

        try:
            self.book = pyexcel.get_book(file_name=self.tag_file)
        except Exception, error_message:
            print("\n** ERROR : %s \n\n") % (error_message)
            return return_value

        self.all_sheet_names = self.book.sheet_names()

        if self.debug:
            print("\n\nALL Sheet Names (tabs) = %s \n\n") %  self.all_sheet_names

        return_value = True

        return return_value


    def close_sheet(self):
        pass


    def iterate_all_sheets(self):

        target_text = "Tag Name in DB"
        save_dict = {}

        for sheet_index in range(self.book.number_of_sheets()):
            sheet = self.book.sheet_by_index(sheet_index)
            header_list = [header for header in sheet.row_at(1)]

            print
            print("=" * 40)
            print("Sheet %s  =  %s") % (sheet_index, self.all_sheet_names[ sheet_index])
            print("=" * 40)
            print

            for col_num, current_col in enumerate(header_list):
                print("%d)  %s") % (col_num, current_col)

                if target_text in current_col:
                    save_dict[sheet_index] = col_num

            print

#       print save_dict

        if save_dict:
            for key, value in save_dict.iteritems():
                print("\n\nSuggested Command-line : --sheet %s  --tag_col %s\n\n") % (key, value)


    def get_all_tags(self):

        sheet = self.book.sheet_by_index(self.sheet_num)                        # get the sheet num
        header_list = [header for header in sheet.row_at(1)]

        #print sheet.number_of_rows()

        row_id = 0                                                              # start at row 0

        cell_set = set()

        for current_row in sheet.rows():                                        # iterate through all rows
            cell_value = sheet[row_id, self.tag_col]

            if self.debug:
                print("Cell[%s,%s]  = %s") % (row_id, self.tag_col, cell_value)

            if cell_value and row_id > 1:                                       # we only want data values after row 2 (zero based)
                cell_set.add(cell_value)                                        # add unique values to the set only

            row_id += 1


        row_id = 1

        if not len(cell_set):                                                   # check to see if any data came back from col
            print("\n** NO TAG DATA FOUND in Col = %s **\n") % self.tag_col
            return

        for current_cell in sorted(cell_set):                                   # dump out all of the unique values
            print("%s") % (current_cell)
            row_id += 1


def main():

    config_info = parse_arguments()                                             # Get configuration arguments - exit on value validation failure

    tagObj = TagSheets(config_info)
#    tagObj.config_info = config_info                                            # assign the cmd-line values to the class

    if not tagObj.open_sheet():
        sys.exit()

    if config_info.tag_flag:                                                    # show all of the tag headings per TAB
        tagObj.iterate_all_sheets()

    elif config_info.tag_col > 0:                                               # read & output all tags
        tagObj.get_all_tags()

    else:
        print("\n** Nothing To Do...  Specify: --get_tags  OR --col_num nn --sheet n \n")

    tagObj.close_sheet()



if __name__ == "__main__":
    main()
