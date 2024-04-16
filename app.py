from flask import Flask
from data import db_session
from flask import render_template, request, redirect
from data.users import Article
from flask_login import LoginManager
import numpy as np
import pyaudio as pa
from data.login import LoginForm
import folium

# частота дискретизации
sample_rate = 44100
# 16-ти битный звук (2 ** 16 -- максимальное значение для int16)
s_16bit = 2 ** 16
freq_array = np.array([261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88])


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/map')
def map():
    m = folium.Map(location=[20, 0], zoom_start=2)

    cities = {
        "Балтимор (США)": (39.2904, -76.6122, "Филип Гласс"),
        "Наро-Фоминск (Московская область)": (55.3877, 36.7226, "Кирилл Рихтер"),
        "Франкфурт-на-Майне (Германия)": (50.1109, 8.6821, "Ханс Циммер"),
        "Нью-Йорк (США)": (40.7128, -74.0060, "Джон Уильямс"),
        "Милан": (45.4642, 9.1900, "Роберто Каччапалья")
    }

    for city, (lat, lon, composer) in cities.items():
        folium.Marker(location=[lat, lon], popup=f"{city}\nЖил: {composer}").add_to(m)

    m.save('templates/map.html')
    return render_template('map.html')

def generate_sample(freq, duration, volume):
    # амплитуда
    amplitude = np.round(s_16bit * volume)
    # длительность генерируемого звука в сэмплах
    total_samples = np.round(sample_rate * duration)
    # частоте дискретизации (пересчитанная)
    w = 2.0 * np.pi * freq / sample_rate
    # массив сэмплов
    k = np.arange(0, total_samples)
    # массив значений функции (с округлением)
    return np.round(amplitude * np.sin(k * w))


def generate_tones(duration):
    tones = []
    for freq in freq_array:
        tone = np.array(generate_sample(freq, duration, 1.0), dtype=np.int16)
        tones.append(tone)
    return tones


@app.route('/piano_music')
def piano_music():
    return render_template('piano.html')


@app.route('/play_tone/<int:index>')
def play_tone(index):
    duration_tone = 1/64.0
    tones = generate_tones(duration_tone)
    p = pa.PyAudio()
    stream = p.open(format=p.get_format_from_width(width=2),
                    channels=2, rate=sample_rate, output=True)
    stream.write(tones[index])
    stream.stop_stream()
    stream.close()
    p.terminate()
    return ''


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Article).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == '73946323804236637' and form.email.data == 'fhien45dgioaskpgh@yandex.ru':
            return redirect("/create-article")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/password/<int:id>', methods=['GET', 'POST'])
def password(id):
    form = LoginForm()
    db_sess = db_session.create_session()
    article = db_sess.query(Article).get(id)
    if form.validate_on_submit():
        if form.password.data == '73946323804236637' and form.email.data == 'fhien45dgioaskpgh@yandex.ru':
            return render_template('delite.html', article=article)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/password_up/<int:id>', methods=['GET', 'POST'])
def password_up(id):
    form = LoginForm()
    db_sess = db_session.create_session()
    article = db_sess.query(Article).get(id)
    if form.validate_on_submit():
        if form.password.data == '73946323804236637' and form.email.data == 'fhien45dgioaskpgh@yandex.ru':
            return render_template('delite.html', article=article)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/instruments')
def index():
    return render_template('index.html')


@app.route('/balalaika')
def balalaika():
    return render_template('instruments/balalaika.html')


@app.route('/domra')
def domra():
    return render_template('instruments/domra.html')


@app.route('/banjo')
def banjo():
    return render_template('instruments/banjo.html')


@app.route('/arfa')
def arfa():
    return render_template('instruments/arfa.html')


@app.route('/psaltery')
def psaltery():
    return render_template('instruments/psaltery.html')


@app.route('/guitar')
def guitar():
    return render_template('instruments/guitar.html')


@app.route('/lute')
def lute():
    return render_template('instruments/lute.html')


@app.route('/mandolin')
def mandolin():
    return render_template('instruments/mandolin.html')


@app.route('/djembe')
def djembe():
    return render_template('instruments/djembe.html')


@app.route('/xylophone')
def xylophone():
    return render_template('instruments/xylophone.html')


@app.route('/tom-tom')
def tom_tom():
    return render_template('instruments/tom-tom.html')


@app.route('/tambourine')
def tambourine():
    return render_template('instruments/tambourine.html')


@app.route('/plates')
def plates():
    return render_template('instruments/xylophone.html')


@app.route('/maraca')
def maraca():
    return render_template('instruments/maraca.html')


@app.route('/timpani')
def timpani():
    return render_template('instruments/timpani.html')


@app.route('/grand_piano')
def grand_piano():
    return render_template('instruments/grand_piano.html')


@app.route('/piano')
def piano():
    return render_template('instruments/piano.html')


@app.route('/synthesizer')
def synthesizer():
    return render_template('instruments/synthesizer.html')


@app.route('/organ')
def organ():
    return render_template('instruments/organ.html')


@app.route('/accordion')
def accordion():
    return render_template('instruments/accordion.html')


@app.route('/harpichord')
def harpichord():
    return render_template('instruments/harpichord.html')


@app.route('/accodion_garmon')
def accodion_garmon():
    return render_template('instruments/accodion_garmon.html')


@app.route('/bayan')
def bayan():
    return render_template('instruments/bayan.html')


@app.route('/flute')
def flute():
    return render_template('instruments/flute.html')


@app.route('/clarinet')
def clarinet():
    return render_template('instruments/clarinet.html')


@app.route('/bassoon')
def bassoon():
    return render_template('instruments/bassoon.html')


@app.route('/truba')
def truba():
    return render_template('instruments/truba.html')


@app.route('/saxophone')
def saxophone():
    return render_template('instruments/saxophone.html')


@app.route('/french_horm')
def french_horm():
    return render_template('instruments/french_horm.html')


@app.route('/composers')
def composers():
    return render_template('composers.html')


@app.route('/ambrioso')
def ambrioso():
    return render_template('composers/15/ambrioso.html')


@app.route('/anchieta')
def anchieta():
    return render_template('composers/15/anchieta.html')


@app.route('/daniil')
def daniil():
    return render_template('composers/15/daniil.html')


@app.route('/domenico')
def domenico():
    return render_template('composers/15/domenico.html')


@app.route('/virdung')
def virdung():
    return render_template('composers/15/virdung.html')


@app.route('/zavish')
def zavish():
    return render_template('composers/15/zavish.html')


@app.route('/cristobal')
def cristobal():
    return render_template('composers/16/cristobal.html')


@app.route('/giovanni')
def giovanni():
    return render_template('composers/16/giovanni.html')


@app.route('/tallis')
def tallis():
    return render_template('composers/16/tallis.html')


@app.route('/thomas')
def thomas():
    return render_template('composers/16/thomas.html')


@app.route('/william')
def william():
    return render_template('composers/16/wiliam.html')


@app.route('/antonio')
def antonio():
    return render_template('composers/17/antonio.html')


@app.route('/ditrih')
def ditrih():
    return render_template('composers/17/ditrih.html')


@app.route('/gaspar')
def gaspar():
    return render_template('composers/17/gaspar.html')


@app.route('/giuseppe')
def giuseppe():
    return render_template('composers/17/giuseppe.html')


@app.route('/henry')
def henry():
    return render_template('composers/17/henry.html')


@app.route('/bah')
def bah():
    return render_template('composers/18/bah.html')


@app.route('/beethoven')
def beethoven():
    return render_template('composers/18/beethoven.html')


@app.route('/haydn')
def haydn():
    return render_template('composers/18/haydn.html')


@app.route('/mozart')
def mozart():
    return render_template('composers/18/mozart.html')


@app.route('/vivaldi')
def vivaldi():
    return render_template('composers/18/vivaldi.html')


@app.route('/shopen')
def shopen():
    return render_template('composers/19/shopen.html')


@app.route('/shtraus')
def shtraus():
    return render_template('composers/19/shtraus.html')


@app.route('/tchaikovsky')
def tchaikovsky():
    return render_template('composers/19/tchaikovsky.html')


@app.route('/verdi')
def verdi():
    return render_template('composers/19/verdi.html')


@app.route('/warner')
def warner():
    return render_template('composers/19/warner.html')


@app.route('/glazunov')
def glazunov():
    return render_template('composers/20/glazunov.html')


@app.route('/prokofiev')
def prokofiev():
    return render_template('composers/20/prokofiev.html')


@app.route('/rachmaninoff')
def rachmaninoff():
    return render_template('composers/20/rachmaninoff.html')


@app.route('/scriabin')
def scriabin():
    return render_template('composers/20/scriabin.html')


@app.route('/shostakovich')
def shostakovich():
    return render_template('composers/20/shostakovich.html')


@app.route('/glass')
def glass():
    return render_template('composers/21/glass.html')


@app.route('/richter')
def richter():
    return render_template('composers/21/richter.html')


@app.route('/roberto')
def roberto():
    return render_template('composers/21/roberto.html')


@app.route('/williams')
def williams():
    return render_template('composers/21/williams.html')


@app.route('/zimmer')
def zimmer():
    return render_template('composers/21/zimmer.html')


@app.route('/')
@app.route('/posts')
def posts():
    db_sess = db_session.create_session()
    articles = db_sess.query(Article).order_by(Article.date.desc()).all() #сортировка по дате всех записей
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    db_sess = db_session.create_session()
    article = db_sess.query(Article).get(id)
    return render_template('post_detail.html', article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            db_sess = db_session.create_session()
            db_sess.add(article)
            db_sess.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create-article.html')


@app.route('/posts/<int:id>/del')
def post_delete(id):
    db_sess = db_session.create_session()
    article = db_sess.query(Article).get(id)
    try:
        db_sess.delete(article)
        db_sess.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    db_sess = db_session.create_session()
    article = db_sess.query(Article).get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db_sess.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template('post_update.html', article=article)


def main():
    db_session.global_init("db/blogs.db")
    app.run(debug=True)


if __name__ == '__main__':
    main()