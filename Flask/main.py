from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def disney_movies():
    return render_template("index.html")

@app.route("/princess/")
def disney_princess():
    return render_template("main.html")

@app.route("/princess/stories/")
def princess_stories():
    return render_template("stories.html")

if __name__ == "__main__":
    app.run()