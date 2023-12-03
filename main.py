import os
import smtplib

from flask import Flask, render_template, request
import requests

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)

my_email = os.environ.get("email", "Couldn't find email address")
password = os.environ.get("password", "Couldn't find password")


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'GET':
        return render_template("contact.html")
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        print(name)
        print(email)
        print(phone)
        print(message)

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            # Secure connection with Transport Layer Security
            connection.starttls()
            # Login to account
            connection.login(user=my_email, password=password)
            # Send email
            connection.sendmail(from_addr=email, to_addrs=my_email, msg=f"Subject:New Message\n\n{message}")

        return render_template("contact.html", post_successful=True)


# @app.route("/form-entry", methods=["POST"])
# def received_data():
#     name = request.form['name']
#     email = request.form['email']
#     phone = request.form['phone']
#     message = request.form['message']
#     print(name)
#     print(email)
#     print(phone)
#     print(message)
#     return f"<h1>Successfully sent your message</h1>"
#

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
