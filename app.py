from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cuestionario.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Question(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(255), nullable=False)
  options = db.relationship('Option', backref='question', lazy=True)
  
class Option(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(255), nullable=False)
  is_correct = db.Column(db.Boolean, default=False)
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
        for i in range(1, 6):
            option_text = request.form.get(f'option{i}')
            if option_text:
                new_option = Option(text=option_text, question=new_question)
                db.session.add(new_option)
                
        # Procesa las opciones marcadas como respuestas correctas
        correct_option_ids = request.form.getlist("correct_option")
        for option in new_question.options:
            if str(option.id) in correct_option_ids:
                option.is_correct = True

        db.session.commit()
        return redirect(url_for('index'))
  else:
        # Si es un GET, muestra el formulario HTML
      questions = Question.query.all()
      return render_template('formulario.html', questions=questions)
    

@app.route('/calificar', methods=['POST'])
def calificar():
    if request.method == 'POST':
        questions = Question.query.all()
        total_questions = len(questions)
        correct_answers = 0
        incorrect_answers = 0

        for question in questions:
            selected_option_id = request.form.get(f'question{question.id}')
            if selected_option_id:
                selected_option = Option.query.get(selected_option_id)
                if selected_option.is_correct:
                    correct_answers += 1
                else:
                    incorrect_answers += 1

        flash(f'Respuestas correctas: {correct_answers}', 'success')
        flash(f'Respuestas incorrectas: {incorrect_answers}', 'danger')

        return redirect(url_for('index'))

# bloque para ejecutar 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
