from flask import Flask,render_template,url_for

app = Flask (__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",title="Home")

@app.route("/about")
def about():
    return render_template("about.html",title="About")

@app.route("/contact")
def contact():
    return render_template("contact.html",title="contact")


@app.route("/favourites")
def favourites():
    return render_template("favourites.html",title="favourites")


@app.route("/products")
def products():
    return render_template("products.html",title="products")


if __name__ == "__main__":
    app.run(debug=True)