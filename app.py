from flask import Flask, render_template, request, url_for,redirect
from flask_sqlalchemy import SQLAlchemy

# instncia do Flask
app = Flask(__name__)
# caminho do DB
app.config ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dbcliente"
# instancia do sqlalchemy
db = SQLAlchemy(app)

# crio a tabela cliente
class Cliente(db.Model):
    __tablename__ = "tbcliente"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(50), unique=True)
    Password = db.Column(db.String(120))
    Name = db.Column(db.String(50))
    Email = db.Column(db.String(100))
    
    def __init__(self, userName, Password, Name, Email):
        self.userName = userName
        self.Password = Password
        self.Name = Name
        self.Email = Email

users = [{'login':Cliente.query.with_entities(Cliente.Email), 'senha': Cliente.query.with_entities(Cliente.Password)}]


@app.route("/")
def index():
    #selecionar todos - select * from
    clientes = Cliente.query.all()
    return render_template("login.html", clientes=clientes)

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # crio um objeto cliente com os dados do formulario
        cliente = Cliente(request.form['userName'], request.form['Password'], request.form['Name'],request.form['Email'] )
        # adiciono o cliente (insert into)
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('add'))
    return render_template("add.html")
    
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    # select from
    cliente = Cliente.query.get(id) 
    if request.method == 'POST':
        cliente.userName = request.form['userName']
        cliente.Password = request.form['Password']
        cliente.Name = request.form['Name']
        cliente.Email = request.form['Password']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("edit.html", cliente = cliente)

@app.route("/delete/<int:id>")
def delete(id):
    cliente = Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/form_teste", methods=['PUT', 'POST'])
def form_teste():
   login = request.form["login"]
   senha = request.form["password"]
   for user in users:
        if user['login'] == login and user['senha'] == senha:
            return render_template("login_ok.html", login = login)
        return render_template("login.html", mensagem = "Login inválido.")



if __name__== "__main__":
    #cria Banco
    db.create_all()
    # executa a aplicação
    app.run(debug=True)