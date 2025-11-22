import connection
import gspread
from google.oauth2.service_account import Credentials


scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes) 
client = gspread.authorize(creds)

sheet_id = "19M_3bFODY65vMkwxtDRW74TyBPKGga4uw2Y_4RVhtjk"
sheet = client.open_by_key(sheet_id)

# defining sheets
Mainsheet = sheet.sheet1
Secondarysheet = sheet.worksheet("Secondary")

def to_int(value, default=0):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default

# user input
def update_sheets(category, generalised):
    if connection.is_connected():
        # Read (Main sheet)
        General_Trash = to_int(Mainsheet.cell(2, 2).value)   # row 2, col 2
        Paper_Trash   = to_int(Mainsheet.cell(2, 3).value)   # row 3, col 2
        Plastic_Trash = to_int(Mainsheet.cell(2, 4).value)   # row 4, col 2

        # write (Main sheet)
        if generalised == b'A':
            Paper_Trash += 1
            Mainsheet.update_cell(2, 3, str(Paper_Trash))
        elif generalised == b'B':
            Plastic_Trash += 1
            Mainsheet.update_cell(2, 4, str(Plastic_Trash))
        else:
            General_Trash += 1
            Mainsheet.update_cell(2, 2, str(General_Trash))

        category_list = Mainsheet.row_values(1)
        value_list = Mainsheet.row_values(2)
        print("Main sheets")
        print(category_list)
        print(value_list)


        # Read (Secondary sheet)
        Battery = to_int(Secondarysheet.cell(2, 2).value)  # column 2
        Biological     = to_int(Secondarysheet.cell(2, 3).value)  # column 3
        Brown_glass     = to_int(Secondarysheet.cell(2, 4).value)  # column 4
        Cardboard     = to_int(Secondarysheet.cell(2, 5).value)  # column 5
        Clothes   = to_int(Secondarysheet.cell(2, 6).value)  # column 6
        Green_glass   = to_int(Secondarysheet.cell(2, 7).value)  # column 7
        Metal   = to_int(Secondarysheet.cell(2, 8).value)  # column 8
        Paper   = to_int(Secondarysheet.cell(2, 9).value)  # column 9
        Plastic   = to_int(Secondarysheet.cell(2, 10).value)  # column 10
        Shoes   = to_int(Secondarysheet.cell(2, 11).value)  # column 11
        Trash   = to_int(Secondarysheet.cell(2, 12).value)  # column 12
        White_glass   = to_int(Secondarysheet.cell(2, 13).value)  # column 13

        # write (Secondary sheet)
        if category == "battery":
            Battery += 1
            Secondarysheet.update_cell(2, 2, str(Battery))
        elif category == "biological":
            Biological += 1
            Secondarysheet.update_cell(2, 3, str(Biological))
        elif category == "brown-glass":
            Brown_glass += 1
            Secondarysheet.update_cell(2, 4, str(Brown_glass))
        elif category == "cardboard":
            Cardboard += 1
            Secondarysheet.update_cell(2, 5, str(Cardboard))
        elif category == "clothes":
            Clothes += 1
            Secondarysheet.update_cell(2, 6, str(Clothes))
        elif category == "green-glass":
            Green_glass += 1
            Secondarysheet.update_cell(2, 7, str(Green_glass))
        elif category == "metal":
            Metal += 1
            Secondarysheet.update_cell(2, 8, str(Metal))
        elif category == "paper":
            Paper += 1
            Secondarysheet.update_cell(2, 9, str(Paper))
        elif category == "plastic":
            Plastic += 1
            Secondarysheet.update_cell(2, 10, str(Plastic))
        elif category == "shoes":
            Shoes += 1
            Secondarysheet.update_cell(2, 11, str(Shoes))
        elif category == "trash":
            Trash += 1
            Secondarysheet.update_cell(2, 12, str(Trash))
        else:
            White_glass += 1
            Secondarysheet.update_cell(2, 13, str(White_glass))

        category_list2 = Secondarysheet.row_values(1)
        value_list2 = Secondarysheet.row_values(2)
        print("Secondary sheets")
        print(category_list2)
        print(value_list2)
    else:
        print("No connection")
