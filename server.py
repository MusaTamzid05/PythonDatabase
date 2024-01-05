from flask import Flask
from flask import request
from flask import flash
from werkzeug.utils import secure_filename
from flask import render_template

import os

from simple_database.database import Database
from simple_database.database import Table

current_database = None



DATABASE_DIR_PATH = os.path.join(os.getcwd(), "databases")

app = Flask(__name__)
app.secret_key = "this is the world best secret key"

def get_database_list():
    return os.listdir(DATABASE_DIR_PATH)



@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        print(request.files)
        uploaded_file = request.files["file"]

        if uploaded_file.filename.endswith("sql") == False:
            flash("Only sqlite file")
        else:
            filename = secure_filename(uploaded_file.filename)

            if os.path.isdir(DATABASE_DIR_PATH) == False:
                os.mkdir(DATABASE_DIR_PATH)

            uploaded_path = os.path.join(DATABASE_DIR_PATH, filename)
            uploaded_file.save(uploaded_path)


            

    database_list = get_database_list()
    context = {"database_list" : database_list}
    context["title"] = "Upload"
    return render_template("home.html", context=context)

@app.route("/database/<database_name>", methods=["GET"])
def show_database(database_name):
    global current_database
    database_path = os.path.join(DATABASE_DIR_PATH, database_name)

    database_list = get_database_list()
    current_database = Database(path=database_path)
    current_database.connect()
    table_names = current_database.get_table_names()

    context = {
            "title" : f"Database : {database_name}",
            "database_list" : database_list,
            "table_names" : table_names
            }

    return render_template("show_database.html", context=context)




@app.route("/table/<table_name>/<offset>", methods=["GET"])
def show_table(table_name, offset):
    database_list = get_database_list()
    print(f"Offset {offset}")
    context = {"database_list" : database_list}
    context["table_name"] = table_name

    return render_template("show_table.html", context=context)


