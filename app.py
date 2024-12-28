from flask import Flask
from data import db_session
from flask import render_template, request, redirect
from data.users import Article
from flask_login import LoginManager
import numpy as np
import pyaudio as pa
from data.login import LoginForm
import folium
# aaaaaaaaaaaa
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
        "Карлсруэ (Германия)": (49.026390, 8.397577, "Ханс Эрих Апостель"),
        "Ахен (Германская империя)": (50.778489, 6.108122, "Лео Блех"),
        "Берлин (Пруссия)": (52.508328, 13.396580, "Франц фон Блон"),
        "Здуньска-Воле (Польша)": (51.595244, 18.964774, "Эмиль Бонке"),
        "Франкфурт-на-Майне": (50.125308, 8.621684, "Вальтер Браунфельс"),
        "Кельн": (50.952644, 6.978126, "Макс Брух"),
        "Мёнхенгладбах": (51.177768, 6.450357, "Феликс Готгельф"),
        "Глазго (Шотландия)": (55.854805, -4.238791, "Эжен Д’Альбер"),
        "Кобург": (50.264992, 10.970739, "Феликс Дрезеке"),
        "Франкфурт": (50.125308, 18.964774, "Фридрих Зайц"),
        "Мангейм": (49.481235, 8.504562, "Гизелер Вольфганг Клебе"),
        "Штутгарт": (48.778080, 9.179251, "Хельмут Лахенман"),
        "Марль": (51.665727, 7.098815, "Маттиас Пинчер"),
        "Метцинген": (48.538062, 9.290804, "Рейнхард Фебель"),
        "Ханау": (50.135443, 8.911256, "Пауль Хиндемит"),
        "Окарп": (55.655297, 13.112232, "Ларс-Эрик Вильнер Ларссон"),
        "Уппсала": (59.845575, 17.640253, "Аллан Петтерссон"),
        "Гётеборг": (57.693145, 11.904532, "Эверт Тоб"),
        "Стокгольм": (59.333793, 17.980247, "Отто Эмануэль Ульсон"),
        "Фьезоле (Италия)": (43.807078, 11.292902, "Джаннотто Бастианелли"),
        "Онелья (Лигурия), Италия": (43.890097, 8.058022, "Лучано Берио"),
        "Джулианов": (40.853582, 14.245358, "Гаэтано Брага"),
        "Сесто-Фьорентино": (42.432571, -1.934066, "Ренато Броджи"),
        "Берлин": (52.508328, 13.396580, "Бенвенуто Ферруччо Бузони"),
        "Флоренци": (43.777141, 11.227714, "Сильвано Буссотти"),
        "Болонье (Италия)": (45.191410, 10.514439, "Чельсо Валли"),
        "Джузеппе Галиньяни": (44.297834, 11.881463, "Джузеппе Галиньяни"),
        "Мартино Станислао Луиджи Гастальдон": (45.069553, 7.683093, "Турин (Италия)"),
        "Джорджо Федерико Гедини": (44.380090, 7.544070, "Кунео"),
        "Сассари": (40.724998, 8.560976, "Луиджи Канепа, Луиджи Канепа"),
        "Пазин (Хорватия)": (45.237161, 13.939041, "Луиджи Даллапикколас"),
        "Риччоне": (44.003019, 12.654631, "Паоло Дзаваллоне"),
        "Атесса": (42.067931, 14.409316, "Антонио Ди Йорьо"),
        "Турин (Италия)": (45.069553, 7.683093, "Альфредо Казелла"),
        "Маддалони": (41.036053, 14.383105, "Альфонсо Кастальди"),
        "Лепороано": (41.175728, 14.220592, "Дамиано Козимо Ланца"),
        "Мачерата (Италия)": (43.297304, 13.446630, "Лино Ливиабелла"),
        "Венеция": (45.743987, 11.862635, "Джан Франческо Малипьеро, Клаудио Амброзини, Луиджи Ноно, Луиджи Руссоло"),
        "Палермо (Италия)": (38.132982, 13.350802, "Франко Маннино"),
        "Рим": (41.594478, 13.206266, "Луиджи Манчинелли"),
        "Монте-Урано": (43.201939, 13.667126, "Детто Мариано"),
        "Капуе": (41.103022, 14.216805, "Джузеппе Мартуччи"),
        "Перледо (Италия)": (46.015633, 9.288454, "Джино Негри"),
        "Монтебелло-Вичентино": (45.453771, 11.385671, "Арриго Педролло"),
        "Пьемонт": (45.275083, 7.920603, "Лоренцо Перози"),
        "Тортона": (44.893260, 8.867899, "Марциано Перози "),
        "Катания": (37.513349, 15.086092, "Джузеппе Перротта, Антонио Саваста"),
        "Страконице": (49.262493, 13.893191, "Рикардо Пик-Манджагалли"),
        "Неаполь": (39.583816, 15.797963, "Марио Пилати, Седжо Рендине, Витторио Монти, Якопо Наполи, Паскуале Каталано,"
                                          "Антонио Брага, Раффаэле Вивиани, Эмилия Губитози"),
        "Парма": (42.866751, 12.683142, "Ильдебрандо Пиццетти"),
        "Луго": (44.423171, 11.909496, "Франческо Балилла Прателла"),
        "Лукка": (43.841658, 10.496329, "Джакомо Пуччини"),
        "Майолати-Спонтини": (43.476271, 13.117461, "Армандо Пьеруччи"),
        "Милан": (45.478322, 9.156186, "Джулия Рекли, Марио Нашимбене, Марчелло Аббадо, Роберто Каччапалья"),
        "Александрия": (31.170302, 29.969439, "Витторио Риети "),
        "Санта-Маргерита-Лигуре": (44.306105, 9.245555, "Виктор де Сабата"),
        "Реджо-Калабрия": (38.102621, 15.660047, "Никола Сгро"),
        "Сантус": (-23.956294, -46.318390, "Альберто Теста"),
        "Корлеоне": (37.816070, 13.298422, "Франческо Паоло Наполи"),
        "Палермо": (38.132982, 13.350802, "Сальваторе Шаррино"),
        "Сардиния": (39.227030, 9.057746, "Бенедетто Юнк, Эмилио Боццано"),
        "Вустер": (42.389002, -71.864993, "Джон Кулидж Адамс"),
        "Белмонт": (37.510655, -122.292457, "Артур Бёрд"),
        "Париж": (48.858823, 2.347042, "Эдгар Варез, Жильбер Ами, Пьер Анри, Клод Баллиф, Пьер Бастьен, Ив Бодрие,"
                                       "Мел Бони, Луи-Шарль-Бонавантюр-Альфред Брюно, Эдгар Варез, Андре Жедальж, Жак Ибер,"
                                       "Франсуа Казадезюс "),
        "Санта-Барбара": (34.428986, -119.702088, "Дэвид Вудард"),
        "Одесса": (46.485206, 30.721705, "Луис Вольф Гильберт"),
        "Редвуд-Сити": (37.484874, -122.233042, "Скот Грешем-Ланкастер "),
        "Калифорния": (38.581285, -121.493639, "Хью Кэннон, Дэвид Хантсингер"),
        "Лос-Анджелес": (34.055863, -118.246139, "Ларри Мори"),
        "Кременчуг": (49.065499, 33.410241, "Лео Орнштейн"),
        "Бостон": (42.354371, -71.065489, "Сид Рамин"),
        "Манхэттен": (40.778226, -73.968323, "Кей Свифт"),
        "Неошо": (37.009698, -95.062894, "Джеймс Сильвестр Скотт"),
        "Ломоносов": (59.910740, 29.776466, "Игорь Фёдорович Стравинский"),
        "Нью-Йорк": (40.714627, -74.002863, "Братья Шерман, Сэмми Фейн"),
        "Лодзь": (51.776770, 19.454724, "Гражина Бацевич"),
        "Островцы": (55.591345, 37.992646, "Давид Бейгельман "),
        "Белосток": (53.132336, 23.159808, "Зигмунт Белостоцкий"),
        "Минск": (53.902284, 27.561831, "Юрий Давидович Бельзацкий "),
        "Вроцлав": (51.111252, 17.038346, "Павел Блащак"),
        "Хожув": (50.293823, 18.954219, "Эдвард Богуславский"),
        "Варшава": (52.232090, 21.007139, "Иоанна Бруздович, Моисей Самуилович Вайнберг, Генрик Вагхальтер,"
                                          "Ежи Васовский, Тадеуш Бэрд, Кшиштоф Бацулевский, Ярослав Игоревич Абрамов-Неверли,"
                                          "Симон Лакс, Пётр Мария Лашер де Песлен,  Анджей Чайковский, Стефан Рахонь, Альберик Маньяр,"
                                          "Тони Луи Александр Обен, Жермен Тайефер, Грегуар Этзель"),
        "Кишинёв": (47.024512, 28.832157, "Шмуэл Вайнберг, Юрий Алексеевич Алябов"),
        "Краков": (50.061971, 19.936742, "Адам Валяциньский, Мордехай Гебиртиг"),
        "Киев": (50.450441, 30.523550, "Константин Михайлович Виленский"),
        "Москва": (55.755864, 37.617698, "Казимеж Вилкомирский, Анатолий Александрович Герасимов, Анатолий Николаевич Александров,"
                                         "Левон Ашотович Амбарцумян"),
        "Жешув": (50.037457, 22.004853, "Станислав Вислоцкий"),
        "Львов": (49.839323, 24.029898, "Збигнев Вишневский"),
        "Вильнюс": (54.689388, 25.270894, "Войтех Гавронский, Гинтас Абарюс"),
        "Санкт-Петербург": (59.938784, 30.314997,  "Николай Тихонович Березовский, Александр Константинович Глазунов, "
                                                  "Марк Самойлович Самойлов, Николай Ильич Аладов, "
                                                  "Леонид Константинович Александров, Татьяна Владимировна Алёшина"),
        "Ленинград": (59.938676, 30.314494, "Александр Георгиевич Васильев"),
        "Пятигорск": (44.039802, 43.070643, "Павел Рихардович Зингер"),
        "Ярославль": (57.626559, 39.893813, "Ляпунов Сергей Михайлович, Алексеев Константин Сильвестрович"),
        "Свердловск": (56.838011, 60.597474, "Сергей Алексеевич Минин "),
        "Бышть": (50.131869, 15.913790, "Эдуард Францевич"),
        "Екатеринбург": (56.838011, 60.597474, "Геннадий Михайлович Перевалов"),
        "Варна (Болгария)": (43.208468, 27.908563, "Михаил Степанович Петухов"),
        "Слободской, Кировская область": (58.731325, 50.170657, "Михаил Карлович Штейнберг"),
        "Афины": (37.975534, 23.734855, "Жорж Апергис"),
        "Бордо": (44.844512, -0.578183, "Анри Барро"),
        "Висамбур": (49.034890, 7.951411, "Андре Блох"),
        "Вувр": (47.223528, 4.338926, "Шарль Борд"),
        "Понтиви": (48.066101, -2.965707, "Людовик Бурс"),
        "Тулуз": (43.579138, 1.503807, "Анри Бюссе"),
        "Лурд": (42.984069, 0.662229, "Софи Лаказ"),
        "Каркасоне (Лангедок)": (45.377958, -0.227417, "Поль Лакомб"),
        "Аббе": (45.665160, -0.195078, "Марсель Ландовски"),
        "Сфакс": (34.739874, 10.760110, "Кристьян Лоба"),
        "Фонтене-ле-Конт": (46.464129, -0.800201, "Лео Люге"),
        "Реймс": (49.261299, 4.031603, "Венсан Сегаль"),
        "Казахстан": (51.143964, 71.435819, "Жорж Цыпин"),
        "Бламон": (48.590168, 6.842288, "Флоран Шмитт"),
        "Трнава": (48.372540, 17.591609, "Ладислав Бурлас"),
        "Прага": (50.080345, 14.428974, "Карел Вайс, Петр Гапка, Вацлав Добиаш, Карел Коваржовиц"),
        "Вена": (48.206487, 16.363460, "Индржих Вацек"),
        "Горни Ровень": (50.023702, 15.988503, "Милош Вацек"),
        "Збраслав": (49.967762, 14.385432, "Яромир Вейвода"),
        "Млада-Болеслав": (50.414230, 14.907803, "Болеслав Вомачка"),
        "Врбице": (50.181098, 15.230397, "Сватоплук Гавелка"),
        "Лоуни": (37.937097, -82.274990, "Милан Кимличка"),
        "Либушина": (50.066927, 14.416074, "Зденек Лишка"),
        "Рыхнов-над-Кнежной": (50.162942, 16.285082, "Рудольф Рокль"),
        "Товачов": (49.432992, 17.288787, "Клемент Славицкий"),
        "Пльзень": (49.744810, 13.368459, "Эмиль Франтишек Буриан, Иржи Сухи, Олдрих Флосман"),
        "Писек": (49.309492, 14.151026, "Иржи Срнка"),
        "Банска-Бистриц": (48.736970, 19.140961, "Вилиам Фигуш-Бистри"),
        "Рокитно": (50.106201, 15.886796, "Отакар Шин"),
        "Рибница": (45.740697, 14.728903, "Боян Адамич"),
        "Штирия": (47.073472, 15.441267, "Блаж Арнич"),
        "Брно": (49.192469, 16.605124, "Эмерик Беран"),
        "Дубровник": (42.650663, 18.091091, " Благое Берса"),
        "Ясика": (43.622290, 21.295624, "Станислав Бинички"),
        "Котор": (42.425071, 18.768959, "Иван Брканович"),
        "Загреб": (45.808600, 15.978577, "Рудольф Бруччи, Юро Ткальчич"),
        "Вуковар": (45.343532, 19.011657, "Предраг Вукович"),
        "Шибеник": (43.740943, 15.895985, "Арсен Дедич"),
        "Хорватия": (45.808594, 15.978577, "Антун Добронич"),
        "Белград": (44.816245, 20.460469, "Миодраг «Мики» Евремович, Исидора Жебелян, Стеван Христич"),
        "Риека": (43.860498, 19.238796, "Миховил Логар"),
        "Вержей": (46.582667, 16.166288, "Славко Остерц"),
        "Сараево": (43.859867, 18.431301, "Нелле Карайлич"),
        "Фояна": (46.589121, 11.147230, "Радо Симонити"),
        "Сплит": (43.512724, 16.442386, "Иво Тиярдович"),
        "Вучья-Вас": (46.598818, 16.101457, "Драготин Цветко"),
        "Бекетовка": (54.085382, 46.868863, "Александра Пахмутова"),
        "село Семёновка": (52.796486, 51.207052, "Лев Ефимович Кербель"),
        "Маньчжурия": (49.591476, 117.446558, "Алексей Борисович Абаза"),
        "Шуша": (39.758503, 46.749477, "Ашраф Джалал оглы Аббасов, Сулейман Эйюб оглы Алесекров"),
        "Чон-Джар": (42.780120, 74.458533, "Мукаш Абдраев"),
        "Астрахань": (46.347614, 48.030178, "Рустам Абдрашитович Абдуллаев"),
        "Подгорный Байлар": (55.746583, 52.994529, "Азгар Ханифович Абдуллин"),
        "село Любичи": (55.030050, 39.224676, "Лев Моисеевич Фридман"),
        "Алматинская область": (43.854849, 77.061581, "Сергали Абжанов"),
        "село Подлесное": (54.315337, 47.600721, "Анатолий Тимофеевич Авдиевский"),
        "Магнитогорск": (53.407163, 58.980291, "Олег Георгиевич Аверин"),
        "Шафторка": (54.125603, 42.232982, "Александр Петрович Аверкин"),
        "Ленинакан": (47.308024, 39.651071, "Хачатур Мехакович (Христофор Михайлович) Аветисян"),
        "Кутол": (42.843865, 41.377848, "Нора Ирадионовна Аджинджал"),
        "Баку": (40.369546, 49.835073, "Васиф Зульфугар оглы Адыгёзалов, Таир Акпер, Агшин Аликули оглы Ализаде,"
                                       " Фирангиз Алиага кызы Ализаде"),
        "Торонто": (43.665208, -79.392710, "Ефим Самуилович Адлер"),
        "Уфа": (54.735152, 55.958736, "Сергей Сергеевич Аксаков"),
        "Репьёвка": (51.076304, 38.641050, "Александр Николаевич Аксаков"),
        "Цхинвал": (42.225084, 43.970862, "Феликс Шалвович Алборов"),
        "Леова": (46.479366, 28.257657, "Ион Христофорович Алдя-Теодорович"),
        "Азов": (47.112448, 39.423581, "Александр Алексеевич Александров"),
        "Плахино": (54.461258, 39.339113, "Александр Васильевич Александров"),
        "Бологое": (57.885636, 34.049590, "Борис Александрович Александров"),
        "Душанбе": (38.576271, 68.779716, "Геннадий Сергеевич Александров"),
        "Нуръял": (56.448936, 48.937782, "Виталий Михайлович Алексеев"),
        "Светловодск": (49.053255, 33.214480, "Юрий Васильевич Алексеев"),
        "Таллин": (59.437425, 24.745137, "Урмас Алендер"),
        "Гызыларбат": (38.980670, 56.275778, "Хыдыр Алланурович Аллануров"),
        "Харьков": (49.992167, 36.231202, "Юрий Борисович Алжнев"),
        "Карабулак": (43.305601, 44.909413, "Ахмат Аманбаев"),
        "Нальчик": (43.485259, 43.607081, "Ефрем Григорьевич Амирамов"),
        "Ереван": (40.177628, 44.512555, "Роберт Бабкенович Амирханян")

    }

    for city, (lat, lon, composer) in cities.items():
        folium.Marker(location=[lat, lon], popup=f"{city}\nРодился: {composer}").add_to(m)

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