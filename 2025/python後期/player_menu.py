from flask import Flask, render_template
app = Flask(__name__)

player = "勇者"

@app.route("/")
def menu():
  return render_template('menu.html', player = player)

# あるく
@app.route("/walk")
def walk():
  massage = player + "は荒野を歩いていた"
  return render_template("action.html", player = player, massage = massage)

# @app.route('/result', methods = ["Post"])
# def result():
#   massage = "This is paiza"
#   article = request.form["article"]
#   name = request.form['name']
#   return render_template("form.html", massage = massage, article = article, name = name)