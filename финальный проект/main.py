from flask import Flask, render_template, request
from models import db, EnergySurvey


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
advice_varinty = ["""
            Освещение потребляет больше всего электроэнергии.
            Попробуйте использовать LED-лампы, так как они расходуют
            намного меньше электричества. Также рекомендуется выключать
            свет в комнатах, где никого нет.
            """,
            """
            Телевизор потребляет большое количество электроэнергии.
            Старайтесь выключать телевизор полностью, а не оставлять
            его в режиме ожидания. Уменьшение времени просмотра также
            поможет снизить расход энергии.
            """,
            """
            Компьютер работает слишком долго и расходует много энергии.
            Используйте режим сна или выключайте компьютер, когда он
            не используется. Также можно уменьшить яркость монитора,
            чтобы снизить потребление электричества.
            """,
            """
            Холодильник потребляет больше всего энергии в доме.
            Проверьте температуру охлаждения и не открывайте дверцу
            слишком часто. Также важно не ставить горячую еду внутрь,
            так как это увеличивает нагрузку на холодильник.
            """
]
with app.app_context():
    db.create_all()


def calculate_energy(lamp_count, lamp_hours, tv_hours, pc_hours, fridge_on):
    lamp_energy = round((lamp_count * 70 * lamp_hours) / 1000,2)

    tv_energy = round((200 * tv_hours) / 1000,2)

    pc_energy = round((300 * pc_hours) / 1000,2)

    if fridge_on == "1":
        fridge_energy = 1.50
    else:
        fridge_energy = 0

    total = round(lamp_energy + tv_energy + pc_energy + fridge_energy,2)
    total_month = round(total * 720)

    if total > 0 :
        lamp_percent = round((lamp_energy/total)*100)
        tv_percent = round((tv_energy/total)*100)
        pc_percent = round((pc_energy/total)*100)
        fridge_percent = round((fridge_energy/total)*100)
    else:
        lamp_percent = tv_percent = pc_percent = fridge_percent = 0

    max_energy = max(
        lamp_energy,
        tv_energy,
        pc_energy,
        fridge_energy
    )

    if max_energy == lamp_energy:
        advice = advice_varinty[0]

    elif max_energy == tv_energy:
        advice = advice_varinty[1]

    elif max_energy == pc_energy:
        advice = advice_varinty[2]

    elif max_energy == fridge_energy:
        advice = advice_varinty[3]

    return {
        "lamp_energy": lamp_energy,
        "tv_energy": tv_energy,
        "pc_energy": pc_energy,
        "fridge_energy": fridge_energy,
        "lamp_percent": lamp_percent,
        "tv_percent": tv_percent,
        "pc_percent": pc_percent,
        "fridge_percent": fridge_percent,
        "total": total,
        "total_month": total_month,
        "advice": advice
    }

@app.route("/", methods=["GET", "POST"])
def index():

    data = {
        "lamp_energy": 0, "tv_energy": 0, "pc_energy": 0, "fridge_energy": 0,
        "lamp_percent": 0, "tv_percent": 0, "pc_percent": 0, "fridge_percent": 0,
        "total": 0, "total_month": 0, "advice": "Начните заполнять данные"
    }
    comparison = None 
    
    if request.method == "POST":

        # получаем данные из формы
        lamp_hours = float(request.form.get("lamp_hours"))
        lamp_count = int(request.form.get("lamp_count"))

        tv_hours = float(request.form.get("tv_hours"))

        pc_hours = float(request.form.get("pc_hours"))

        fridge_on = request.form.get("fridge_on")

        data = calculate_energy(lamp_count, lamp_hours, tv_hours, pc_hours, fridge_on)
        
        new_survey = EnergySurvey(total_kwh_per_month=data["total_month"])
        db.session.add(new_survey)
        db.session.commit()

        comparison = new_survey.compare_with_average()

    return render_template(
        "index.html", **data, comparison=comparison
    )

app.run(debug=True)