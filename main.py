from flask import Flask, render_template, session, url_for, request
import json
import os
import os.path

app = Flask(__name__) # Flask Init


@app.route('/') # Provide Home Page
def main_page():
    return """Main Page <br>
           <a href="./register"><button>Register</button></a>
           <a href="./login"><button>Login</button></a>
           """


@app.route("/register", methods=["POST", "GET"]) # Provide register page, and connect methods
def register():
    if request.method == "POST": 
        username = request.form["username"]
        userpassword = request.form["password"]
        path_to_user = "./profiles/" + str(username)
        if not os.path.exists(path_to_user): # check exist, or not user in database
            with open(path_to_user, "w") as file: # Open file with user account data, and writing data.
                data = {}
                data[username] = []
                data[username].append({
                    "name": username,
                    "password": userpassword
                })
                json.dump(data, file) 
            return render_template("profile.html", name=username) # Render profile page with user current name
        else: # if account already exist, showing message about this
            return """
            Этот аккаунт уже существует.
            """
    else:
        return render_template("register.html") # Create HTML Body for localhost:8080/register


@app.route('/login',  methods=["POST", "GET"]) # Provide login page, and connect methods
def login():
    if request.method == "POST":
        username = request.form["username"]
        userpassword = request.form["password"]
        path_to_user = "./profiles/" + str(username)
        try:
            f = open(path_to_user, "r") # Open file with user data, if ile exists.
            userdata = json.loads(f.read()) # Convert data from file in json.
            for i in userdata[str(username)]: # search data in json
                if userpassword in i["password"]: # if entered password by user 
                                                  # common with password 
                                                  # in file, render profile page 
                    return render_template("profile.html", name=i["name"]) # render profile page
                else: # if password wrong, render info about this
                    return """Неверный пароль 
                            <br>
                            <a href="/"><button>To Home Page</button></a>
                            <a href="/register"><button>Register</button></a>"""
        except FileNotFoundError: # if user file not found (user not exists), render info about this
            return """Ваш профиль не был найден в списке
                <br>
                <a href="/"><button>To Home Page</button></a>
                <a href="/register"><button>Register</button></a>"""
    else:
        return render_template("login.html") # render page for localhost:8080/login


if __name__ == "__main__": # run server
    app.run(debug=True, port=8080)
