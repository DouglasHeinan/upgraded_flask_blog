from flask import Flask, render_template, request
import requests
import smtplib
import os


MY_EMAIL = os.environ["MY_EMAIL"]
PASSWORD = os.environ["PASSWORD"]


def main():
    app = Flask(__name__)

    response = requests.get("https://api.npoint.io/6b8db2690f3de5abfd7b")
    entries = response.json()
    entries = entries[::-1]

    @app.route("/")
    def blog_home():
        return render_template("index.html", entries=entries, author="Doug Heinan")

    @app.route("/about")
    def about_page():
        return render_template("about.html")

    @app.route("/contact", methods=["POST", "GET"])
    def contact():
        post = False
        if request.method == "POST":
            post = True
            user_name = request.form["name"]
            # user_email = request.form["email"]
            # user_phone = request.form["phone"]
            message = request.form["message"]
            with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(
                  from_addr=MY_EMAIL,
                  to_addrs=MY_EMAIL,
                  msg=f"Subject: {user_name} has contacted you!\n\n{message}"
                )
            return render_template("contact.html", post=post)
        return render_template("contact.html", post=post)

    @app.route("/post_<post_id>")
    def read_post(post_id):
        entry = [entry for entry in entries if entry["id"] == post_id][0]
        return render_template("post.html", entry=entry)

    app.run(debug=True)


if __name__ == "__main__":
    main()
