from flask import Flask, flash, render_template, redirect, url_for
from forms import SignupForm, LoginForm
from chips import chipsData

app = Flask(__name__)
app.config["SECRET_KEY"] = "15bb914121bfb88e90cd224850b5e614"

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",title="Home",chips = chipsData)

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
    return render_template("products.html",title="products",chips = chipsData)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login successfull!')
        return redirect(url_for('home'))
    return render_template('login.html', title="Login", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash(f'Signup successful! Welcome {form.username.data}!')
        return redirect(url_for('home'))
    return render_template('signup.html', title="Signup", form=form)



if __name__ == "__main__":
    app.run(debug=True)