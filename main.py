from flask import Flask, render_template, session, url_for, request
import json
import os
import os.path

app = Flask(__name__)


@app.route('/')
def main_page():
    return """Main Page <br>
           <a href="./register"><button>Register</button></a>
           <a href="./login"><button>Login</button></a>
           """


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        userpassword = request.form["password"]
        path_to_user = "./profiles/" + str(username)
        with open(path_to_user, "w") as file:
            data = {}
            data[username] = []
            data[username].append({
                "name": username,
                "password": userpassword
            })
            json.dump(data, file)
        return render_template("profile.html", name=username)
    else:
        return render_template("register.html")


@app.route('/login',  methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        userpassword = request.form["password"]
        path_to_user = "./profiles/" + str(username)
        try:
            f = open(path_to_user, "r")
            userdata = json.loads(f.read())
            for i in userdata[str(username)]:
                if userpassword in i["password"]:
                    return render_template("profile.html", name=i["name"])
                else:
                    return """Неверный пароль
                            <br>
                            <a href="/"><button>To Home Page</button></a>
                            <a href="/register"><button>Register</button></a>"""
        except FileNotFoundError:
            return """Ваш профиль не был найден в списке
                <br>
                <a href="/"><button>To Home Page</button></a>
                <a href="/register"><button>Register</button></a>"""
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
