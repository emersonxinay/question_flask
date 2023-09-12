from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cuestionario.db'
db = SQLAlchemy(app)

class Question(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(255), nullable=False)
  options = db.relationship('Option', backref='question', lazy=True)
  
class Option(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(255), nullable=False)
  question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

# rutas 
@app.route('/')
def index():
  questions = Question.query.all()
  return render_template('index.html', questions=questions)

@app.route('/formulario',  methods=['GET', 'POST'])
def formulario():
  if request.method == 'POST':
        question_text = request.form['question_text']
        # Crea una nueva pregunta en la base de datos
        new_question = Question(text=question_text)
        db.session.add(new_question)
        
        # Procesa las opciones enviadas desde el formulario
        for i in range(1, 6):  # Suponemos un máximo de 5 opciones
            option_text = request.form.get(f'option{i}')
            if option_text:
                new_option = Option(text=option_text, question=new_question)
                db.session.add(new_option)
        
        db.session.commit()
        return redirect(url_for('index'))
  else:
        # Si es un GET, muestra el formulario HTML
        return render_template('formulario.html')
# bloque para ejecutar 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
