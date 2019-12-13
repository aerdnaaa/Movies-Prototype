from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", title="Dashboard")


@app.route("/promotion")
def promotion():
    return render_template("promotion.html", title="Promotion")

@app.route("/booking")
def booking():
    return render_template("booking.html", title="Booking")

@app.route("/rent")
def rent():
    return render_template("rent.html", title="Renting")

@app.route("/composeMail")
def composeMail():
    return render_template("compose.html", title="Compose Mail")

@app.route("/readMail")
def readMail():
    return render_template("read-mail.html", title="Read Mail")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html", title="Calendar")

@app.route("/mailbox")
def mailbox():
    return render_template("mailbox.html", title="Mailbox")

@app.route("/movieTheatre")
def movieTheatre():
    return render_template("movie theatre.html", title="Movie Theatre")

@app.route("/movies")
def movies():
    return render_template("movies.html", title="Movies")

if __name__ == "__main__":
    app.run(debug=True)
    