from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  #path to db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    #Show all todos    
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list = todo_list) #passing var to the html

@app.route("/add", methods=["POST"])
def add():
   #Add new item
   title =  request.form.get("title") #get title for the input
   new_todo = Todo(title = title, complete = False)
   db.session.add(new_todo)
   db.session.commit()
   return redirect(url_for("index")) # reload tye index page

@app.route("/update/<int:todo_id>")
def update(todo_id):
   #Update item
   todoToUpdate = Todo.query.filter_by(id = todo_id).first()
   todoToUpdate.complete = not todoToUpdate.complete
   db.session.commit()
   return redirect(url_for("index")) # reload tye index page

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
   #Delete item
   todoToUpdate = Todo.query.filter_by(id = todo_id).first()
   db.session.delete(todoToUpdate)
   db.session.commit()
   return redirect(url_for("index")) # reload tye index page



if __name__ == '__main__':
    db.create_all()

   
    app.run(debug=True)