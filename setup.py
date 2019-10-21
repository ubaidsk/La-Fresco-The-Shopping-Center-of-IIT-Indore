#!/usr/bin/python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)


sh = client.open("LaFrescoDatabase")
print("Opened Spreadsheet")

@app.route("/")
def Home():
    worksheet_list =sh.worksheet("All Sheets").get_all_records()
    print("Got all worksheets")
    dictionary_of_items={}
    for sheet_name in worksheet_list:
        sheet=sh.worksheet(sheet_name.get("name"))
        array_of_items=[]
        all_categories = sheet.get_all_records()
        # print(all_categories)
        for category in all_categories:
            array_of_items.append(category)
        dictionary_of_items[sheet_name.get("name")]=array_of_items
    print("\n\n Dictionary of Items passed is\n")
    # print(dictionary_of_items)
    print("\n\n heading_names passed is\n")
    # print(worksheet_list)
    return render_template('home.html', dictionary_of_items=dictionary_of_items, heading_names=worksheet_list)

@app.route('/items/<int:category_id>/<int:item_category_id>')
def ShowItems(category_id, item_category_id):
    worksheet_list =sh.worksheet("All Sheets").get_all_records()
    print("Got all worksheets")
    dictionary_of_items={}
    for sheet_name in worksheet_list:
        sheet=sh.worksheet(sheet_name.get("name"))
        array_of_items=[]
        all_categories = sheet.get_all_records()
        # print(all_categories)
        for category in all_categories:
            array_of_items.append(category)
        dictionary_of_items[sheet_name.get("name")]=array_of_items
    required_worksheet=sh.get_worksheet(category_id+1)
    # print("required worksheet is",required_worksheet)
    needed_items=[]
    print("entering into for loop")
    for row in required_worksheet.get_all_records():
        # print(row)
        if row.get("category_id")==item_category_id:
            needed_items.append(row)
    # print("needed_items are ", needed_items)
    for row in sh.get_worksheet(category_id).get_all_records():
        if row.get("id")==item_category_id:
            item_title=row.get("name")
            break
    return render_template('MenuItem.html', item_title=item_title, needed_items=needed_items, dictionary_of_items=dictionary_of_items, heading_names=worksheet_list)
