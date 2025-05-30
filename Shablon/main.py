from flask import Flask, render_template,request

app = Flask(__name__)

@app.route("/")
def shop():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/about/catalog/")
def catalog():
    return render_template("catalog.html")

@app.route("/about/catalog/contacts/")
def contacts():
    return render_template("contacts.html")

if __name__ == "__main__":
    app.run()