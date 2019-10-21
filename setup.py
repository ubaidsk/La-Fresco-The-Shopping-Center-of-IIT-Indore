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
    worksheet_list = sh.worksheets()
    all_sheet_list=worksheet_list[0].get_all_records()
    print("Got all worksheets")
    dictionary_of_items={}
    for row in all_sheet_list:
        sheet=worksheet_list[row.get("id")]
        array_of_items=[]
        all_categories = sheet.get_all_records()
        for category in all_categories:
            array_of_items.append(category)
        dictionary_of_items[row.get("name")]=array_of_items
    print("\n\n Dictionary of Items passed is\n")
    # print(dictionary_of_items)
    print("\n\n heading_names passed is\n")
    # print(worksheet_list)
    return render_template('home.html', dictionary_of_items=dictionary_of_items, heading_names=all_sheet_list)

@app.route('/items/<int:category_id>/<int:item_category_id>')
def ShowItems(category_id, item_category_id):
    worksheet_list = sh.worksheets()
    all_sheet_list=worksheet_list[0].get_all_records()
    print("Got all worksheets")
    dictionary_of_items={}
    for row in all_sheet_list:
        sheet=worksheet_list[row.get("id")]
        array_of_items=[]
        all_categories = sheet.get_all_records()
        for category in all_categories:
            array_of_items.append(category)
        dictionary_of_items[row.get("name")]=array_of_items
    required_worksheet=worksheet_list[category_id+1]
    needed_items=[]
    print("entering into for loop")
    for row in required_worksheet.get_all_records():
        if row.get("category_id")==item_category_id:
            needed_items.append(row)
    for row in worksheet_list[category_id].get_all_records():
        if row.get("id")==item_category_id:
            item_title=row.get("name")
            break
    return render_template('MenuItem.html', item_title=item_title, needed_items=needed_items, dictionary_of_items=dictionary_of_items, heading_names=all_sheet_list)
