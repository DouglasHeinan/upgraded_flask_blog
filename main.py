from flask import Flask, render_template
import requests


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

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route("/post_<post_id>")
    def read_post(post_id):
        entry = [entry for entry in entries if entry["id"] == post_id][0]
        return render_template("post.html", entry=entry)

    app.run()


if __name__ == "__main__":
    main()
