from flask import Flask,render_template,url_for,redirect,request,flash, jsonify
from todo.models import Todo,User
from todo import app,db
from todo.forms import RegisterForm,LoginForm
from flask_login import login_user, logout_user, login_required,current_user

@app.route('/home',methods=['GET'])
def home():
	user = current_user
	try:
		todo = []
		todos = Todo.query.all()
		for task in todos:
			print(task.user)
			if task.user==user.username:
				print(task)
				todo.append(task)

		return render_template("index.html",todo=todo)
	except Exception as e:
		print(e)
@app.route('/',methods=['POST','GET'])
@login_required
def create_todo():
	user = current_user
	if request.method == "POST":
		contents = request.form["content"]
		todo = Todo(content = contents)
		todo.user=user.username
		try:
			db.session.add(todo)
			# db.session.add(todo)
			db.session.commit()
			return redirect(url_for("create_todo"))
		except Exception as e:
			print(f'27-------{e}')
	else:
		my_task = []
		todo = Todo.query.all()
		for task in todo:
			if task.user==user.username:
				my_task.append(task)
		return render_template("index.html",my_task=my_task)
@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
	task = Todo.query.get_or_404(id)
	if request.method == "POST":
		data = request.form['data']
		task.content = data
		try:
			db.session.commit()
			return redirect(url_for('create_todo'))
		except Exception as e:
			print(e)
	else:
		return render_template('update.html',task=task)

@app.route('/delete/<int:id>')
def delet(id):
	task = Todo.query.get_or_404(id)
	try:
		db.session.delete(task)
		db.session.commit()
		return redirect(url_for('create_todo'))
	except Exception as e:
		print(e)

@app.route("/register",methods=["POST","GET"])
def register_page():
	form = RegisterForm()
	if form.validate_on_submit():
		user_create = User(username=form.username.data,
						email_address=form.email_address.data,
						password=form.password.data)
		db.session.add(user_create)
		db.session.commit()
		return redirect(url_for('home'))
	if form.errors!={}:
		for err_msg in form.errors.values():
			flash(f'There was an error with creating a user: {err_msg}', category='danger')
	return render_template("register.html",form=form)

@app.route("/login",methods=["POST","GET"])
def login_page():
	form = LoginForm()
	if form.validate_on_submit():
		logging_user = User.query.filter_by(username=form.username.data).first()
		if logging_user and logging_user.check_password(logging_password=form.password.data):
			login_user(logging_user)
			flash(f"{logging_user.username} logged succesfully..")
			return redirect(url_for("create_todo"))
		else:
			flash('Username and password are not match! Please try again', category='danger')
	return render_template("login.html",form=form)
@app.route("/logout")
def logout_page():
	logout_user()
	flash("You Have Logged Out..")
	return render_template("home.html")