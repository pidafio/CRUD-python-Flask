from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from basedatos import db
from form import PersonaForm
from models import Personas

app = Flask(__name__)
USER_DB = 'postgres'
PASS_DB = 'miletic5'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate()
migrate.init_app(app, db)
app.config['SECRET_KEY']='contraseña'

@app.route('/')
def inicio():
    personas=Personas.query.order_by('id')
    total_personas=Personas.query.count()
    app.logger.debug(f'personas:{personas}')
    app.logger.debug(f'total de personas:{total_personas}')
    return render_template('index.html', personas=personas, total_personas=total_personas)
@app.route('/ver/<int:id>')
def ver_detalle(id):
    persona=Personas.query.get_or_404(id)
    app.logger.debug((f'ver persona:{persona}'))
    return render_template('detalle.html', persona=persona)
@app.route('/agregar', methods=['GET','POST'])
def agregar():
    persona=Personas()
    formu =PersonaForm(obj=persona)
    if request.method =='POST':
        if formu.validate_on_submit():
            formu.populate_obj(persona)
            app.logger.debug(f'persona a insertar: {persona}')
            db.session.add(persona)
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('agregar.html',formu=formu)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    persona=Personas.query.get_or_404(id)
    formu=PersonaForm(obj=persona)
    if request.method=='POST':
        if formu.validate_on_submit():
            formu.populate_obj(persona)
            app.logger.debug(f'se modificara:{ persona }')
            db.session.add(persona)
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('editar.html', formu=formu)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona=Personas.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('inicio'))