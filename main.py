from enum import Enum

import telebot
from telebot import types


class BotState(Enum):
    INIT = 0
    START = 1
    NEXT = 2
    CONSCIOUSNESS = 3
    HAVE_CONSCIOUSNESS = 3.1
    HAVE_BREATH = 3.11
    NO_BREATH = 3.12
    NO_CONSCIOUSNESS = 3.2
    BREATH = 4
    SIGNS_OF_LIFE = 5
    INJURY_WITH_BLEEDING = 6.1
    INJURY_WITHOUT_BLEEDING = 6.2
    HARD_BREATH = 6.3
    AMBULANCE = 7
    STOP = 8


API_TOKEN = "5704224565:AAGoAQSrhyNWBf498vlg6P53KvZqg3LIk4I"
bot = telebot.TeleBot(API_TOKEN)
bot_state = BotState.INIT


def send_image(image_id, chat_id):
    with open(f'images/{image_id}.png', 'rb') as img:
        bot.send_photo(chat_id, img)


def get_keyboard_from_list(options):
    keyboard = types.InlineKeyboardMarkup()
    for option in options:
        key = types.InlineKeyboardButton(text=option, callback_data=option)
        keyboard.add(key)
    return keyboard


@bot.message_handler(commands=['start'])
def handle_start_command(data):
    global bot_state
    message = ("Бот по оказанию первой медицинской помощи приветствует вас!\n"
               "Прежде, чем начать работу, обращаем ваше внимание, "
               "что данный бот не является официальным учебным пособием "
               "по оказанию первой медицинской помощи, ответственность "
               "за помощь пострадавшему лежит только на спасателе, "
               "не забывайте, что одним из главных принципов врачебной "
               "практики является принцип «не навреди».")

    keyboard = get_keyboard_from_list(['Начать работу'])
    bot.send_message(data.from_user.id, text=message, reply_markup=keyboard)
    bot_state = BotState.START


@bot.callback_query_handler(func=lambda _: bot_state == BotState.START)
def callback_start(call):
    global bot_state
    if call.data == "Начать работу":
        message = "Первое что нужно сделать – обеспечить безопасные условия для оказания первой медицинской помощи.\n" \
                  "Устраните факторы, которые могут навредить вам или усугубить положение пострадавшего."
        keyboard = get_keyboard_from_list(['Далее'])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.NEXT


@bot.callback_query_handler(func=lambda _: bot_state == BotState.NEXT)
def callback_next(call):
    global bot_state
    if call.data == "Далее":
        message = "Пострадавший в сознании?"
        keyboard = get_keyboard_from_list(["Да", "Нет"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.CONSCIOUSNESS


@bot.callback_query_handler(func=lambda _: bot_state == BotState.CONSCIOUSNESS)
def callback_consciousness(call):
    global bot_state
    if call.data == "Да":
        message = "Какие травмы есть у пострадавшего?"
        keyboard = get_keyboard_from_list(["Травма с кровотечением", "Травма без кровотечения",
                                           "Затруднение дыхания", "Ожоги", "Обморожения",
                                           "Отравление", "Другое"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.HAVE_CONSCIOUSNESS
    elif call.data == "Нет":
        message = "У пострадавшего есть дыхание?"
        keyboard = get_keyboard_from_list(["Да", "Нет"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.NO_CONSCIOUSNESS


def call_ambulance(call):
    send_image(10, call.message.chat.id)
    message = "Вызовите скорую помощь, если не сделали этого ранее, " \
              "наблюдайте за состоянием пострадавшего\n" \
              "Спасибо за обращение!\n\n" \
              "Чтобы начать сначала напишите /start"
    bot.send_message(call.message.chat.id, text=message)


@bot.callback_query_handler(func=lambda _: bot_state == BotState.NO_CONSCIOUSNESS)
def callback_no_consciousness(call):
    global bot_state
    if call.data == "Да":
        send_image(1, call.message.chat.id)
        message = "Необходимо запрокинуть голову пострадавшего с подъемом подбородка\n" \
                  "a.	При необходимости выдвинуть нижнюю челюсть\n" \
                  "b.	Определить наличие нормального дыхания с помощью слуха, зрения и осязания\n" \
                  "c.	Определить наличие кровообращения путем проверки пульса на магистральных артериях\n"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.AMBULANCE
    elif call.data == "Нет":
        message = 'a.	Необходимо вызвать скорую помощь по телефону 03/103/112, ' \
                  'привлекая помощника или с использованием громкой связи на телефоне'
        bot.send_message(call.message.chat.id, text=message)
        send_image(2, call.message.chat.id)
        send_image(3, call.message.chat.id)
        send_image(4, call.message.chat.id)
        message = 'b.	Провести сердечно-легочную реанимацию путем чередования давления руками ' \
                  'на грудину пострадавшего, искусственного дыхания “рот ко рту”/”рот к носу”\n' \
                  '     1.	Давление руками на грудину пострадавшего выполняется весом туловища ' \
                  'участника оказания ПМП на глубину 5-6 см с частотой 100-120 в минуту.\n' \
                  '     2.	После 30 надавливаний необходимо осуществить искусственное дыхание. ' \
                  'Зажмите нос пострадавшего и выполните 2 выдоха в рот пострадавшего. ' \
                  'Далее чередуйте 30 надавливаний на грудь-2 выдоха в рот'
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.NO_BREATH
    else:
        bot.send_message(call.message.chat.id, text=f'Unrecognised data: {call.data}')


@bot.callback_query_handler(func=lambda _: bot_state == BotState.NO_BREATH)
def callback_no_breath(call):
    global bot_state
    if call.data == "Готово":
        message = "Появились признаки жизни?"
        keyboard = get_keyboard_from_list(["Да", "Нет"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.SIGNS_OF_LIFE
    else:
        bot.send_message(call.message.chat.id, text=f'Unrecognised data: {call.data}')


@bot.callback_query_handler(func=lambda _: bot_state == BotState.SIGNS_OF_LIFE)
def callback_signs_of_life(call):
    global bot_state
    if call.data == "Да":
        send_image(5, call.message.chat.id)
        message = "1.	Расположите ближнюю руку пострадавшего под прямым углом к его телу"
        bot.send_message(call.message.chat.id, text=message)
        send_image(6, call.message.chat.id)
        message = "2.	Дальнюю руку пострадавшего приложить тыльной стороной ладони к " \
                  "противоположной щеке пострадавшего, придерживая ее рукой"
        bot.send_message(call.message.chat.id, text=message)
        send_image(7, call.message.chat.id)
        message = "3.	После этого согнуть дальнюю от себя ногу пострадавшего в колене, " \
                  "поставить ее с опорой на стопу, надавить на колено этой ноги " \
                  "на себя и повернуть пострадавшего"
        bot.send_message(call.message.chat.id, text=message)
        send_image(8, call.message.chat.id)
        message = "4.	После поворота пострадавшего набок слегка запрокинуть его голову " \
                  "для открытия дыхательных путей и подтянуть ногу, лежащую сверху, ближе к животу"
        bot.send_message(call.message.chat.id, text=message)
        send_image(9, call.message.chat.id)
        message = "5.	Необходимо наблюдать за состоянием пострадавшего до прибытия бригады " \
                  "скорой помощи, регулярно оценивая у него наличие дыхания"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Нет":
        message = "Повторять действия СЛР до приезда скорой помощи."
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.AMBULANCE
    elif call.data == 'Готово':
        bot_state = BotState.CONSCIOUSNESS
        message = "Пострадавший в сознании?"
        keyboard = get_keyboard_from_list(["Да", "Нет"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, text=f'Unrecognised data: {call.data}')


@bot.callback_query_handler(func=lambda _: bot_state == BotState.HAVE_CONSCIOUSNESS)
def callback_have_consciousness(call):
    global bot_state
    if call.data == "Травма с кровотечением":
        message = "В случае попадания в рану инородного тела, например осколок стекла/ножа, " \
                  "ни в коем случае не следует вынимать его из раны. Необходимо обложить " \
                  "инородный предмет салфетками или бинтами, наложив поверх них давящую повязку " \
                  "для остановки кровотечения. "
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.INJURY_WITH_BLEEDING
    elif call.data == "Травма без кровотечения":
        message = "Какие есть травмы?"
        keyboard = get_keyboard_from_list(["Травма шеи", "Травма груди", "Травма живота",
                                           "Травма таза", "Травма конечностей",
                                           "Травма позвоночника", "Остальных травм нет"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.INJURY_WITHOUT_BLEEDING
        pass
    elif call.data == "Затруднение дыхания":
        message = "Какие есть симптомы?"
        keyboard = get_keyboard_from_list(["Человек кашляет",
                                           "Человек хватается за горло",
                                           "Остальных травм нет", "Другое"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.HARD_BREATH
    elif call.data == "Ожоги":
        message = "a.	Приложить лед к ожоговой поверхности, затем ожоговую поверхность " \
                  "необходимо закрыть нетугой повязкой, дать пострадавшему теплое питье, " \
                  "обязательно вызвать бригаду скорой помощи\n" \
                  "b.	Запрещается вскрывать ожоговые пузыри, убирать с пораженной поверхности " \
                  "части обгоревшей одежды, наносить на пораженные участки жиры, мази\n" \
                  "c.	В случае химического ожога необходимо промыть ожоговую поверхность " \
                  "проточной водой в течение 20 минут, дождаться бригады скорой помощи"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Обморожения":
        send_image(28, call.message.chat.id)
        message = "a.	Пострадавшего необходимо укрыть теплоизолирующим материалом " \
                  "(вата, одежда,  одеяло) или наложить теплоизолирующую повязку, " \
                  "так как прогревание должно происходить изнутри с одновременным " \
                  "восстановлением кровообращения. \n" \
                  "b.	Необходимо  создать обездвиженность пораженного участка тела, " \
                  "переместить пострадавшего в теплое помещение, дать теплое питье\n" \
                  "c.	Поврежденные участки нельзя активно согревать, опускать в " \
                  "горячую воду, растирать, массировать, смазывать чем-либо"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Отравление":
        message = "a.	Прекратить поступление яда в организм " \
                  "пострадавшего(например, удалить из загазованной зоны)\n" \
                  "b.	Опросить пострадавшего, выяснить, какой вид отравляющего " \
                  "вещества был принят, в каком количестве и как давно\n" \
                  "c.	Если отравляющее вещество неизвестно, необходимо собрать " \
                  "небольшое количество рвотных масс для последующей медицинской экспертизы\n" \
                  "d.	Попытаться удалить яд (спровоцировать рвоту, смыть " \
                  "токсическое вещество с кожи и т.д.)\n" \
                  "e.	Чтобы вызвать рвоту, необходимо дать пострадавшему " \
                  "большое количество воды(около литра-полтора, в зависимости от " \
                  "комплекции пострадавшего) и надавить двумя пальцами на корень языка\n" \
                  "f.	После рвоты необходимо дать пострадавшему выпить еще " \
                  "5-6 стаканов воды, чтобы снизить концентрацию ядовитого вещества " \
                  "в желудке, при необходимости вызвать рвоту повторно\n" \
                  "g.	До прибытия скорой помощи необходимо " \
                  "контролировать состояние пострадавшего"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Другое":
        callback_ambulance(call)
    elif call.data == "Готово":
        message = "Какие травмы есть у пострадавшего?"
        keyboard = get_keyboard_from_list(["Травма с кровотечением", "Травма без кровотечения",
                                           "Затруднение дыхания", "Ожоги",
                                           "Обморожения", "Отравление", "Другое"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, text=f'Unrecognised data: {call.data}')


@bot.callback_query_handler(func=lambda _: bot_state == BotState.INJURY_WITH_BLEEDING)
def callback_injury_with_bleeding(call):
    global bot_state
    if call.data == "Голова":
        send_image(11, call.message.chat.id)
        message = "Наложить давящую повязку или жгут.\n" \
                  "a.	При наложении на рану желательно наложить стерильные " \
                  "салфетки из аптечки, бинт должен раскатываться по ходу движения, " \
                  "по окончании наложения повязку следует закрепить, завязав свободный " \
                  "конец бинта вокруг конечности. Повязка должна накладываться с усилием\n" \
                  "b.	Вызовите скорую помощь по телефону 03/103/112\n" \
                  "c.	Контролируйте состояние пострадавшего"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Глаз":
        message = "Наложить давящую повязку или жгут.\n" \
                  "a.	В случае травмы глаза, наложите жгут на оба глаза даже при " \
                  "повреждении только единственного, так как при оставлении здорового " \
                  "глаза открытым, он будет невольно следить за окружающим и приводить " \
                  "к движению пострадавшего глаза, что может усугубить его повреждение. " \
                  "Жгутом необходимо закрыть оба глаза и туго обмотать бинт вокруг головы"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Нос":
        message = "В случае травмы носа, зажмите пострадавшему нос в области крыльев " \
                  "носа на 15-20 мин, положите холод на переносицу. Недопустимо " \
                  "самостоятельное вправление носа. В случае, если кровотечение " \
                  "остановить не удалось, вызывайте скорую помощь по номеру 03/103/112"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data in ["Грудь", "Живот", "Спина"]:
        send_image(12, call.message.chat.id)
        message = "Осуществите прямое давление на рану\n" \
                  "a.	Закройте рану стерильной салфеткой или стерильным бинтом. " \
                  "При отсутствии подойдет любая подручная ткань.\n" \
                  "b.	С силой надавите на область раны так, чтобы кровотечение остановилось"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Шея":
        send_image(13, call.message.chat.id)
        message = "Прижмите сонную артерию в области между раной и сердцем на передней " \
                  "поверхности шеи снаружи от гортани четырьмя пальцами одновременно " \
                  "или одним большим пальцем"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Конечности":
        send_image(16, call.message.chat.id)
        message = "1. Осуществите максимальное сгибание конечности в суставе"
        bot.send_message(call.message.chat.id, text=message)
        send_image(15, call.message.chat.id)
        message = "2. Вложите 1-2 бинта или свернутую валиком одежду в область сустава."
        bot.send_message(call.message.chat.id, text=message)
        send_image(14, call.message.chat.id)
        message = "3. После сгибания зафиксируйте конечность руками или несколькими турами бинта, " \
                  "или подручными средствами (например брючным ремнем) "
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Остальных травм нет":
        message = "Какие травмы есть у пострадавшего?"
        keyboard = get_keyboard_from_list(["Травма с кровотечением", "Травма без кровотечения",
                                           "Затруднение дыхания", "Ожоги", "Обморожения",
                                           "Отравление", "Другое"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.HAVE_CONSCIOUSNESS
        pass
    elif call.data == "Готово":
        message = "Что травмировано?"
        keyboard = get_keyboard_from_list(["Голова", "Глаз", "Нос", "Грудь", "Живот",
                                           "Спина", "Шея", "Конечности", "Остальных травм нет"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, text=f'Unrecognised data: {call.data}')


@bot.callback_query_handler(func=lambda _: bot_state == BotState.INJURY_WITHOUT_BLEEDING)
def callback_injury_without_bleeding(call):
    global bot_state
    if call.data == "Травма шеи":
        send_image(17, call.message.chat.id)
        message = "1.	Необходимо вручную поддерживать голову в положении, ограничивающем движение" \
                  "2.	Дождаться приезда скорой помощи, контролируя состояние пострадавшего, " \
                  "оставаясь в положении, фиксирующем голову пострадавшегоёт" \
                  "3.	Фиксировать шею пострадавшего можно также подручными средствами, " \
                  "например курткой или свитером. Нужно обернуть их вокруг шеи, имитируя жесткий воротник"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Травма груди":
        send_image(18, call.message.chat.id)
        message = "i.	Посадите пострадавшего в полусидячее положение с наклоном " \
                  "в пораженную сторону и контролируйте его состояние до приезда скорой помощи"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Травма живота":
        send_image(19, call.message.chat.id)
        message = "i.	Положите холод на живот пострадавшего, придайте " \
                  "ему положение «лежа на спине»  с валиком под полусогнутыми " \
                  "разведенными в стороны ногами, контролируйте состояние " \
                  "пострадавшего до приезда скорой помощи"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Травма таза":
        send_image(20, call.message.chat.id)
        message = "i.	Придайте пострадавшему положение «лежа на спине» с валиком " \
                  "под полусогнутыми разведенными в стороны ногами, контролируйте состояние " \
                  "пострадавшего до приезда скорой помощи"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Травма конечностей":
        send_image(21, call.message.chat.id)
        send_image(22, call.message.chat.id)
        message = "i.	При подозрениях на перелом кости, необходимо иммобилизировать " \
                  "поврежденную кость, то есть обездвижить.  Дожидаясь приезда скорой помощи, " \
                  "необходимо сохранять обездвиженное положение пострадавшего в травмируемой " \
                  "области, контролировать его состояние"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        pass
    elif call.data == "Травма позвоночника":
        send_image(23, call.message.chat.id)
        message = "1.	Если пострадавшего необходимо переместить, необходимо это " \
                  "делать с помощью нескольких человек, особое внимание следует " \
                  "уделить фиксации шейного отдела позвоночника"
        bot.send_message(call.message.chat.id, text=message)
        send_image(24, call.message.chat.id)
        message = "2.	После перемещения пострадавшего необходимо расположить на ровной, " \
                  "жесткой горизонтальной поверхности, дождаться бригады скорой помощи, " \
                  "контролируя состояние пострадавшего"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        pass
    elif call.data == "Остальных травм нет":
        message = "Какие травмы есть у пострадавшего?"
        keyboard = get_keyboard_from_list(["Травма с кровотечением", "Травма без кровотечения",
                                           "Затруднение дыхания", "Ожоги", "Обморожения",
                                           "Отравление", "Другое"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.HAVE_CONSCIOUSNESS
    elif call.data == "Готово":
        message = "Какие есть травмы?"
        keyboard = get_keyboard_from_list(["Травма шеи", "Травма груди", "Травма живота",
                                           "Травма таза", "Травма конечностей",
                                           "Травма позвоночника", "Остальных травм нет"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, text=f'Unrecognised data: {call.data}')


@bot.callback_query_handler(func=lambda _: bot_state == BotState.HARD_BREATH)
def callback_hard_breath(call):
    global bot_state
    if call.data == "Человек кашляет":
        message = "Предложите пострадавшему откашляться"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Человек хватается за горло":
        send_image(25, call.message.chat.id)
        message = "1.	Вероятнее всего, в дыхательные пути попало инородное тело\n" \
                  "2.	Встаньте сбоку и немного сзади пострадавшего\n" \
                  "3.	Придерживая пострадавшего одной рукой, другой наклоните его вперед, " \
                  "чтобы в случае смещения инородного тела оно попало в рот пострадавшего, " \
                  "а не опустилось ниже в дыхательные пути\n" \
                  "4.	Нанесите 5 резких ударов основанием своей ладони между " \
                  "лопатками пострадавшего, проверяя после каждого удара, " \
                  "не удалось ли устранить нарушение проходимости"
        keyboard = get_keyboard_from_list(["Сделано, не помогло", "Помогло"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Сделано, не помогло":
        send_image(26, call.message.chat.id)
        message = "1.	Встаньте позади пострадавшего и обхватите его " \
                  "обеими руками на уровне верхней части живота"
        bot.send_message(call.message.chat.id, text=message)
        send_image(27, call.message.chat.id)
        message = "1.	Встаньте позади пострадавшего и обхватите его " \
                  "обеими руками на уровне верхней части живота\n" \
                  "2.	Сожмите кулак одной из рук и поместите его " \
                  "над пупком большим пальцем к себе\n" \
                  "3.	Обхватите кулак другой рукой и, слегка наклонив " \
                  "пострадавшего вперед, резко надавить на его живот " \
                  "в направлении внутрь и кверху"
        keyboard = get_keyboard_from_list(["Готово"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    elif call.data == "Остальных травм нет":
        message = "Какие травмы есть у пострадавшего?"
        keyboard = get_keyboard_from_list(["Травма с кровотечением", "Травма без кровотечения",
                                           "Затруднение дыхания", "Ожоги", "Обморожения",
                                           "Отравление", "Другое"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
        bot_state = BotState.HAVE_CONSCIOUSNESS
    elif call.data == "Другое":
        callback_ambulance(call)
    elif call.data == "Готово" or call.data == "Помогло":
        message = "Какие есть симптомы?"
        keyboard = get_keyboard_from_list(["Человек кашляет",
                                           "Человек хватается за горло",
                                           "Остальных травм нет", "Другое"])
        bot.send_message(call.message.chat.id, text=message, reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, text=f'Unrecognised data: {call.data}')


@bot.callback_query_handler(func=lambda _: bot_state == BotState.AMBULANCE)
def callback_ambulance(call):
    global bot_state
    if call.data in ["Готово", "Другое"]:
        call_ambulance(call)
        bot_state = BotState.STOP
    else:
        bot.send_message(call.message.chat.id, text=f'Unrecognised data: {call.data}')


@bot.message_handler(func=lambda _: True)
def get_text_init_messages(message):
    bot.send_message(message.from_user.id, "Для начала работы напиши /start")


def main() -> None:
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
