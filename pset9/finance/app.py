import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@app.route("/index")
@login_required
def index():
    """Show portfolio of stocks"""
    # get user cash total
    result = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
    cash = result[0]["cash"]

    # pull all the transctions
    portfolio = db.execute("SELECT stock, quantity FROM portfolio WHERE user_id=?", session["user_id"])

    total = cash

    # determin current stock price, stock total value, and grand total
    for stock in portfolio:
        price = lookup(stock['stock'])['price']
        sto_total = stock['quantity'] * price
        stock.update({'price': price, 'total': sto_total})
        total += sto_total

    return render_template("index.html", stocks=portfolio, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # ensure stock symbol and number of shares were submitted
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide stock symbol", 400)
        elif not shares:
            return apology("must provide number of shares", 400)

        # ensure the number of share was a positive integer
        try:
            shares = int(shares)
        except:
            return apology("shares must be a positive integer", 400)

        # ensure number of shares is valid
        if int(shares) <= 0:
            return apology("must provide valid number of shares", 400)

        # pull quote from yahoo finance
        quote = lookup(symbol)

        # check if the stock name valid
        if quote == None:
            return apology("stock symbol not valid", 400)

        # total cost
        cost = int(shares) * quote['price']

        # check if user has enough cash for transaction
        result = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if cost > result[0]["cash"]:
            return apology("you do not have enough cash", 400)

        # update cash amount in users database
        db.execute("UPDATE users SET cash=cash-? WHERE id=?", cost, session["user_id"])

        # add transaction to transaction database
        # db.execute("CREATE TABLE transactions (user_id TEXT, stock TEXT, quantity INTEGER, price INTEGER, boughtsold TEXT, date TEXT)")
        add_transaction = db.execute(
            "INSERT INTO transactions (user_id, stock, quantity, price, boughtsold, date) VALUES (:user_id, :stock, :quantity, :price, :boughtsold, :date)",
            user_id=session["user_id"], stock=quote["symbol"], quantity=int(request.form.get("shares")), price=quote['price'], boughtsold='bought', date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # pull number of shares ofsymbol in portfolio
        # db.execute("CREATE TABLE portfolio (user_id TEXT, stock TEXT, quantity INTEGER)")
        curr_portfolio = db.execute("SELECT quantity FROM portfolio WHERE stock=? AND user_id=?",
                                    quote['symbol'], session["user_id"])

        # add current protfolio to protfolio database
        if not curr_portfolio:
            db.execute("INSERT INTO portfolio (stock, quantity, user_id) VALUES (?, ?, ?)",
                        quote['symbol'], int(shares), session["user_id"])

        # if symbol is already in portfolio, update quantity and total
        else:
            db.execute("UPDATE portfolio SET quantity=quantity+? WHERE stock=? AND user_id=?",
                       shares, quote['symbol'], session["user_id"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # pull transactions
    transactions = db.execute(
        "SELECT stock, quantity, price, boughtsold, date FROM transactions WHERE user_id=?",
        session["user_id"])

    if not transactions:
        return apology("you do not have transactions on record")

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide stock symbol")

        # pull quote from yahoo finance
        quote = lookup(symbol)

        # check if the stock name valid
        if quote == None:
            return apology("stock symbol not valid")

        else:
            return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("confirmation")

        # make sure username was subnmitted
        if not username:
            return apology("must provide username", 400)

        # ensure password were submitted
        elif not password:
            return apology("must provide password", 400)

        # ensure password and password confirmation match
        elif password != password_confirm:
            return apology("password and password confirmation must match", 400)

        # hash password
        hash = generate_password_hash(password)

        # add user to database
        try:
            new_user_id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        except:
            return apology("username has been registered", 400)

        # create a session
        session["user_id"] = new_user_id

        # redirect user to homepage
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        stock = request.form.get("symbol")
        shares = request.form.get("shares")

        if (not shares) or (not stock):
            return apology("must select stock and provide number of shares")

        # ensure number of shares is valid
        quantity = db.execute("SELECT quantity FROM portfolio WHERE stock=? and user_id = ?", stock, session["user_id"])

        if (int(shares) <= 0):
            return apology("must provide valid number of shares")

        if (int(shares) > quantity[0]["quantity"]):
            return apology("must sell shares no more than you currently hold")

         # pull quote from yahoo finance
        quote = lookup(stock)

        # check if the stock name valid
        if quote == None:
            return apology("stock symbol not valid")

        # total cost
        income = int(shares) * quote['price']

        # update cash amount in users database
        db.execute("UPDATE users SET cash=cash+? WHERE id=?", income, session["user_id"])

        # add transaction to transaction database
        add_transaction = db.execute(
            "INSERT INTO transactions (user_id, stock, quantity, price, boughtsold, date) VALUES (:user_id, :stock, :quantity, :price, :boughtsold, :date)",
            user_id=session["user_id"],
            stock=quote["symbol"],
            quantity=int(request.form.get("shares")),
            price=quote['price'],
            boughtsold='sold',
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # update quantity and total
        db.execute("UPDATE portfolio SET quantity=quantity-? WHERE stock=? AND user_id=?",
                    shares, quote['symbol'], session["user_id"])

        return redirect("/")

    else:
        portfolio = db.execute("SELECT stock FROM portfolio")

        return render_template("sell.html", stocks=portfolio)


@app.route("/changepw", methods=["GET", "POST"])
@login_required
def changepw():
    """change password"""

    if request.method == "POST":

        current_password = request.form.get("current_password", 400)

        if not current_password:
            return apology("must provide your current password", 400)

        # Query database for username
        rows = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], current_password):
            return apology("invalid password", 400)

        return redirect("newpw")

    else:
        return render_template("changepw.html")


@app.route("/newpw", methods=["GET", "POST"])
@login_required
def newpw():
    """new password"""

    if request.method == "POST":

        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # ensure password were submitted
        if not new_password or not confirm_password:
            return apology("must provide password", 400)

        # ensure password and password confirmation match
        elif new_password != confirm_password:
            return apology("password and password confirmation must match", 400)

        hash_new = generate_password_hash(new_password)

        # update user to database
        db.execute("UPDATE users SET hash=? WHERE id=?", hash_new, session["user_id"])

        return apology("your password has been successfully changed", 200)

    else:
        return render_template("newpw.html")