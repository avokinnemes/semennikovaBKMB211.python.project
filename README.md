# semennikovaBKMB211.python.project
Проект “Бот-помощник по оказанию первой медицинской помощи”
Для начала, мной была создана электронная, более сжатая и структурированная версия пособия по оказанию Первой медицинской помощи по материалам печатного пособия, официально утвержденного МЧС РФ. На базе моего документа будет строиться структура бота, вопросы и варианты ответа.
Для создания бота была использована библиотека telebot ( установлена через pip install pyTelegramBotAPI).
С помощью BotFather было создано имя бота, были получены уникальный токен(пароль доступа к боту) а также ссылка на сам бот.
Class BotState(Enum) = класс состояния бота
    Состояния бота:
    INIT = 0 #ожидание от пользователя команды /start для запуска дальнейших действий
    START = 1 #приветствие с единственной клавишей для продолжения
    NEXT = 2 #бот предлагает устранить факторы, которые могут помешать оказывать ПМП, единственная клавиша для продолжения
    CONSCIOUSNESS = 3 #бот спрашивает о наличии  сознания у пострадавшего, два варианта ответа, имеется и отсутствует, соответственно
    HAVE_CONSCIOUSNESS = 3.1 #сознание есть, а есть ли дыхание?
    HAVE_BREATH = 3.11 #есть, соответствующая инструкция
    NO_BREATH = 3.12 #нет, соответствующая инструкция
    NO_CONSCIOUSNESS = 3.2 #инструкция при условии ответа пользователя, что сознания нет
    BREATH = 4 #сознания нет, а есть ли дыхание? если есть, соответствующая инструкция, если нет иная инструкция
    SIGNS_OF_LIFE = 5 #в случае, если пользователь отметил, что дыхания нет, бот предложит произвести определенные действия, после проведения пользователем необходимых операций, бот спросит у него, появились ли у пострадавшего признаки жизни, если да, что направит его в меню, которое выясняет, что произошло с пострадавшим(главное меню с вариантами различных травм), если нет, то предложит альтернативный путь
    INJURY_WITH_BLEEDING = 6.1 #главное меню, травма с кровотечением
    INJURY_WITHOUT_BLEEDING = 6.2 #травма без кровотечения
    HARD_BREATH = 6.3 #затрудненное дыхание
    AMBULANCE = 7 #все пути сводятся к пункту вызова скорой помощи
    STOP = 8 #бот говорит до свидания и заканчивает свою работу
    
1. Создаем бота и задаем его начальное состояние
API_TOKEN = “token”
bot = telebot.Telebot(API_TOKEN)
bot_state = BotState.INIT 

2. Запуск бота(бот опрашивает телеграмм на предмет, нет ли новых сообщений от пользователя)
def main() -> None
    bot.polling(none_stop = True, interval = 0) 
if __name__ == "__main__":
    main()
    
@bot.message_handler(func=lambda_: True) #обработчик сообщений от пользователя, 
def get_text_init_messages(message): #любое текстовое сообщение будет перенаправлять бота сюда, в состояние инит, бот будет предлагать вызвать его с помощью команды /start.
  bot.send_message(message.from_user.id, “……. /start”

@bot.message_handler(commands =[‘start’]) #обработчик команды старт, если была получена комманда старт, поприветствуй пользователя
def handle_start_command(data): 
    global bot_state
    message =( “Приветствие”) #задаем сообщение
    Keyboard = get_keyboard_from_list([‘Начать работу”]) #задаем клавиатуру для ответа пользователя, функция принимает на обработку список из клавиш и создает клавиатуру
    bot.send_message(data.from_user.id, text=message, reply_markup=keyboard) #бот обрабатывает сообщение от пользователя, выкидывает ему сообщение(приветствие) и клавиатуру для ответа
    bot_state= BotState.START #переводим бота в следующее состояние
    
@bot.callback_query_handler(func=lambda_: bot_state ==BotState.START) #обработчик полученного ответа от пользователя
	def callback_start(call):
    global bot_state
if call.data == “Начать работу”: #если был получен ответ "начать работу"(с клавиатуры)
    message =( “Следующее сообщение”) #задаем следующее сообщение
    Keyboard = get_keyboard_from_list([‘Далее”]) #задаем следующую клавиатуру
    bot.send_message(call.message.chat.id,  text=message, reply_markup=keyboard) #бот обрабатывает сообщение от пользователя, выкидывает ему следующее сообщение и следующую клавиатуру для ответа
    bot_state= BotState.NEXT #переводим бота в следующее состояние
  
Все остальные состояния обрабатываются аналогично, за исключением ветвлений в некоторых. Но там отличие лишь в цикле if ... /else ...

Прикрепление картинки:
def send_image(image_id, chat_id): 
	    with open(f’images/{image_id}.png’, ‘rb’) as img: 
	        bot.send_photo(chat_id, img)  
          
Создание клавиатуры:
def get_keyboard_from_list(options):
    keyboard = types.InlineKeyboardMarkup()
    for option in options:
        key = types.InlineKeyboardButton(text=option, callback_data=option)
        keyboard.add(key)
    return keyboard
