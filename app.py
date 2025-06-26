from flask import Flask, flash, render_template, redirect, url_for,flash
from forms import SignupForm, LoginForm
from chips import chipsData,findMaxThreeDiscount
from users import user_data,addUser,validateUser

app = Flask(__name__)
app.config["SECRET_KEY"] = "15bb914121bfb88e90cd224850b5e614"

@app.route("/")
@app.route("/home")
def home():
    discounted = findMaxThreeDiscount(chipsData)
    return render_template("home.html",title="Home",chips = discounted)

@app.route("/about")
def about():
    return render_template("about.html",title="About")

@app.route("/contact") 
def contact():
    return render_template("contact.html",title="contact")


@app.route("/favourites") 
def favourites():
    return render_template("favourites.html",title="favourites",chipsData = chipsData)


@app.route("/products")
def products():
    return render_template("products.html",title="products",chips = chipsData)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if validateUser(form.email.data,form.password.data):
            flash('Login successfull!','success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password','error')

    return render_template('login.html', title="Login", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if addUser(form.username.data,form.email.data,form.gender.data,form.dob.data,form.password.data):
            flash(f'Signup successful! Welcome {form.username.data}!','success')
            return redirect(url_for('home'))
        else:
            flash(f'Email already exists !!','error')
    else:
        flash(f'Some error occured !!','error')

    return render_template('signup.html', title="Signup", form=form)

@app.route("/product/<id>")
def ProductDetail(id):
    print(f"The chip id is {type(id)}")
    chip = chipsData.get(int(id))
    print(chip)
    if not chip:
        return redirect(url_for('products'))
    return render_template('product_detail.html',title=f"CrunchCart - {chip['name']}",chipDet = chip)



if __name__ == "__main__":
    app.run(debug=True)