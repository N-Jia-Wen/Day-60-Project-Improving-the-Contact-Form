from flask import Flask, render_template, request
import smtplib
import requests
import os

MY_EMAIL = os.environ["MY_EMAIL"]
MY_PASSWORD = os.environ["MY_PASSWORD"]


posts = requests.get("https://api.npoint.io/6d9316b546b857979fcb").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    message_status = "Contact Me"
    if request.method == "POST":

        message_status = "Successfully sent message!"
        name = request.form.get("name")
        email = request.form.get("email")
        phone_no = request.form.get("phone")
        message = request.form.get("message")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=f"Subject: New Message \n\n"
                                    f"Name: {name}\n"
                                    f"Email: {email}\n"
                                    f"Phone Number: {phone_no}\n"
                                    f"Message: {message}")

    return render_template("contact.html", message_status=message_status)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
