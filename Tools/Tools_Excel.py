
import sys

# so that we are able to import the file and folder which are in the parent_folder
# # Be Careful, AFAIK, if you added this, then it is going to be the parent_folder, the folder which is considered by default by Some importation of file_reading... Hope you dear Reader understand what I mean
# # I mean when Reading the xl_file in def__read_one_cell_from_xl
sys.path.append("..")

from .Print_Color import Print_Color

try:
    import xlrd
except Exception:
    print ("xlrd is NOT installed")
    input()
    os.system("pip install xlrd")

class Tools_Excel:
    
    def __init__(
        self
        , path_file_xl = 'Main_py.xlsx'
    ):
        pass

    @staticmethod
    def read_one_cell_from_xl(
        xl_file = "Main_py.xlsx"
        , sheet_index = 0
        , y = 1 ###n noho ireo val ireo dia B2 no voavaky
        , x = 1
        , give_default_value_if_void = 1
    ):
        workbook_read = xlrd.open_workbook(xl_file)
        sheet_read = workbook_read.sheet_by_index(sheet_index)
        res = ""

        try:
            res = sheet_read.cell_value(y, x)
            # print ('res: ',res)
            if isinstance(res, float):
                res = '{:.0f}'.format(res)
            if ((give_default_value_if_void == 1) and (len(res) == 0)):
                res = 'Erreur dans "xl_file": ' + str(xl_file)+', "sheet_index": ' + str(sheet_index) + ", x = " + str(x) + ", y = " + str(y)
                res += '\n- Contenu du cellule vide'
            return res
        except IndexError:
            msg = "Valeur manquant pour fichier(" + str(xl_file) + "), tab_index("+ str(sheet_index) +")" + ", y = " + str(y) + ", x = " + str(x)
            Print_Color.print_green(
                txt = msg
            )
            return False
            pass

        pass


    @staticmethod
    def read_one_col_of_sheet_xl(
        xl_file = "Main_py.xlsx"
        , sheet_index_to_read = 1
        , x = 0
        , from_y = 2
    ):
        workbook_read = xlrd.open_workbook(xl_file)
        sheet_read = workbook_read.sheet_by_index(sheet_index_to_read)
        res = []
        for i in range(from_y, sheet_read.nrows):
            data = Tools_Excel.read_one_cell_from_xl(
                xl_file = xl_file
                , sheet_index = sheet_index_to_read
                , x = x
                , y = i
            )
            res.append(data)
        return res

        pass

