from flask import Flask, render_template, request, make_response, session
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import EmailField, BooleanField
from wtforms.validators import DataRequired
from data import db_session
from data.jobs import Jobs
from data.users import User
from jobs_api import blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum'


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class JobsForm(FlaskForm):
    title = StringField('Название работы')
    team_leader = StringField('ID руководителя')
    work_size = StringField('Продолжительность')
    collaborators = StringField('Участники')
    finished = BooleanField('Завершена')
    submit = SubmitField('Добавить')



@app.route('/')
def main():
    return render_template('base.html')


@app.route('/index/<title>')
def index(title):
    return render_template('base.html',
                           title=title)


@app.route('/promotion')
def promotion():
    return ('Человечество вырастает из детства.<br><br>'
            'Человечеству мала одна планета.<br><br>'
            'Мы сделаем обитаемыми безжизненные пока планеты.<br><br>'
            'И начнем с Марса!<br><br>'
            'Присоединяйся!')


@app.route('/image_mars')
def image_mars():
    return render_template('image_mars.html')


@app.route('/promotion_image')
def promotion_image():
    return render_template('promotion_image.html')


@app.route('/astronaut_selection')
def astronaut_selection():
    return render_template('astronaut_selection.html')

@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    form = JobsForm()
    if form. validate_on_submit():
        sess = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.finished
        current_user.jobs.append(job)
        sess.merge(current_user)
        sess.commit()
        return redirect(' /')
    return render_template('jobs.html', form=form)


@app.route('/answer', methods=['POST'])
@app.route('/auto_answer', methods=['POST'])
def answer():
    context = {
        'title': 'Анкета',
        'surname': request.form['surname'],
        'name': request.form['name'],
        'education': request.form['education'],
        'profession': ', '.join(request.form.getlist('profession')),
        'gender': request.form['gender'],
        'motivation': request.form['motivation'],
        'ready': request.form.get('ready', '') == 'Готов'
    }
    return render_template('auto_answer.html',
                           **context)


@app.route('/training/<prof>')
def training(prof):
    context = {
        'prof': prof
    }
    return render_template('training.html',
                           **context)


@app.route('/list_prof/<lst>')
def list_prof(lst):
    context = {
        'list': lst,
        'profs': ['', '', '', '', '']
    }
    return render_template('list_prof.html' ,
                           **context)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)
@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")

if __name__ == '__main__':
    db_session.global_init('database/mars_explorer.db')
    app.register_blueprint(blueprint)
    app.run(host='127.0.0.1', port=8080)
