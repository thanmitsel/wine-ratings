import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import streamlit as st

# Tutorial
# https://www.youtube.com/watch?v=zCEJurLGFRk
# https://console.cloud.google.com/iam-admin/serviceaccounts/details/117679126517683902041;edit=true?inv=1&invt=AbrljQ&project=ad-listings-453213
# https://www.youtube.com/watch?v=HwxrXnYVIlU
# https://www.youtube.com/watch?v=HKoOBiAaHGg
# https://docs.google.com/spreadsheets/d/1HaIwBSvLNg6lYp8hx_J5Io1sH4oQYi8b4chNCO-SdkI/edit?gid=923478754#gid=923478754

class GoogleSheets:
    def __init__(self, aplatform):
        self.platform = aplatform
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file"
            ]
        # self.creds = Credentials.from_service_account_file('..\keys\google-sheet-credentials.json', scopes=self.scopes)
        self.creds = Credentials.from_service_account_info(st.secrets["google_api"], scopes=self.scopes)
        self.client = gspread.authorize(self.creds)
        # gumtree https://docs.google.com/spreadsheets/d/1HaIwBSvLNg6lYp8hx_J5Io1sH4oQYi8b4chNCO-SdkI/edit?gid=0#gid=0
        # cargr https://docs.google.com/spreadsheets/d/1BN0wqDROPtHDeKsdsiIeNMQOjvKLV6H9v2xnDKw2--I/edit?gid=1938232139#gid=1938232139
        self.sheet_id =  st.secrets[self.platform+'_'+'sheet_id']  # from url after d before edit
        self.sheet = self.client.open_by_key(self.sheet_id)

    def check_sheet(self):
        values_list = self.sheet.sheet1.row_values(1)
        print(values_list)

    def read_clean_df(self, data_path):
        self.data_path = data_path
        full_path = os.path.join(data_path, f'{self.platform}.csv')
        df = pd.read_csv(full_path)
        return df
    
    def load_clean(self):
        # Select the specific worksheet by name (e.g., 'Sheet1')
        worksheet = self.sheet.worksheet('clean')
        data = worksheet.get_all_records()  # Fetch all rows of data as a list of dictionaries
        return pd.DataFrame(data)

    def upload_clean(self, adf):
        worksheet = self.sheet.worksheet('clean')
        set_with_dataframe(worksheet, adf)
        
        
if __name__ == "__main__":
    # Call and Download Websites
    data_path = 'C:\\Users\\Thanasis\\Documents\\Programming Projects\\wine-ratings\\data\\'
    aplatform = 'wine_ratings'
    sheet_obj = GoogleSheets(aplatform)
    # df = sheet_obj.read_clean_df(data_path)
    # sheet_obj.upload_clean(df)
    df_load = sheet_obj.load_clean()
    print(df_load)