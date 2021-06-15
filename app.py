from flask import Flask, request, render_template, flash, redirect, url_for,  send_file

import json
import os
import datetime
app = Flask(__name__)

app.secret_key = "123456"


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("home.html", title="Home")


@app.route('/modify_json', methods=["GET", "POST"])
def modify_json():

    # build a list of available jsons for the select field
    items =[]
    for file in os.listdir("json_templates"):
        items.append(file)

    # when the data is filled out we get a post request
    if request.method == "POST":
        if "template_select" in request.form:
            choosen_template = request.form["template_select"]
            # open the json which we want to have displayed
            with open(f'json_templates/{choosen_template}') as f:
                json_loaded = json.load(f)
            return render_template("json_forms_2.html", json=json_loaded, items=items)

        else:
            # template to write on
            with open(f'json_templates/{request.form["template_name"]}.json', "w") as d:
                dump_data = {}
                for key, value in request.form.items():
                    if key == "template_name":
                        break
                    dump_data[key] = value
                json.dump(dump_data, d)
            flash("Template Created", "success")
            return redirect(url_for("template_overview"))


    return render_template("json_forms_1.html",  items=items)

@app.route("/template_overview", methods=["GET"])
def template_overview():
    items=[]
    for file in os.listdir("json_templates"):
        items.append([file, datetime.date.fromtimestamp(os.path.getctime(f"json_templates/{file}"))])

    return render_template("template_overview.html", items=items)

@app.route("/return_template/<name>", methods=["GET"])
def return_template(name):
    return send_file(f"json_templates/{name}", as_attachment=False)

@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/creat_template", methods=["GET", "POST"])
def creat_template():
    if request.method == "POST":
        keys = request.form.getlist('keys')
        with open(f'json_templates/{request.form["template_name"]}.json', "w") as d:
            dump_data = {}
            for key in keys:
                if key == "template_name":
                    break
                dump_data[key] = ""
            json.dump(dump_data, d)
        flash("Template Created", "success")
        return redirect(url_for("template_overview"))

    return render_template("creat_template.html")
if __name__ == '__main__':
    app.run(debug=True)
