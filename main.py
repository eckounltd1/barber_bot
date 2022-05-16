import telebot
import datetime
import sqlite3
from telebot import types
import numpy as np
import emoji

bot = telebot.TeleBot('5024613802:AAGe91Kyt6kWOuEyaYehDetxHoYDsaHtkf4')

user_id = ''
name = ''
username = ''
number = ''
service = ''
date = ''
time = ''
work_time = ''
work_date = ''
call_user_id = ''
to_chat_id = '1006827161'   # 1006827161
barber_id = 1006827161
dev_id = 191028786
markup_global = ''
lst_date = []
lst_time = []
lst_service = ['Комплекс', 'Стрижка', 'Борода']


#Команда старт и запись на стрижку

@bot.message_handler(commands=['start', 's'])
def start(message):
    # удаляем пустые ячейки
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute("DELETE FROM user_info WHERE id is NULL OR trim(id) = ''")
    cell = c.fetchall()
    db.commit()
    db.close()
    # удаляем пустые ячейки
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute("DELETE FROM datetime WHERE id is NULL OR trim(id) = ''")
    cell = c.fetchall()
    db.commit()
    db.close()
    if message.from_user.id != barber_id:
        global username
        global user_id
        global markup_global
        user_id = message.from_user.id
        username = f'@{message.from_user.username}'
        #клавиатура главная
        markup_global = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        but1 = types.KeyboardButton('Записаться на стрижку')
        but2 = types.KeyboardButton("Нет, запишусь попозже")
        but3 = types.KeyboardButton("Посмотреть доступное время для записи")
        but4 = types.KeyboardButton("Контакты и Геолокация")
        but5 = types.KeyboardButton('Мои записи')
        markup_global.add(but1, but2, but3, but4, but5)
        sticker = open('hello.jpeg', 'rb')
        smile = emoji.emojize(':smiling_face_with_sunglasses:')
        mess = f'<b>{message.from_user.first_name}</b>, салют!\n' \
               f'Давай запишу тебя на стрижку {smile}\n\n<b>Прайс на услуги:</b>\nКомплекс 1500₽\nСтрижка 1000₽\nБорода 700₽'
        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup_global)
        bot.send_message(message.chat.id, '<b>Геолокация:</b> СПб, метро Владимирская, Достоевская\nВладимирский проспект 13/9, Бьюти Коворкинг', parse_mode='html')
        bot.register_next_step_handler(message, first_que)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton('Создать время для записи')
        btn3 = types.KeyboardButton('Показать список записавшихся')
        btn4 = types.KeyboardButton('Свободное время для записи')
        btn5 = types.KeyboardButton('Записать на стрижку')
        btn6 = types.KeyboardButton('История посещений клиента')
        markup.add(btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, 'Выбери действие', reply_markup=markup)








#Просмотр и удаление существующего времени для записи

@bot.message_handler(func=lambda message: message.text == "Свободное время для записи")
def free_time(message):
    if message.from_user.id == barber_id and message.text == 'Свободное время для записи':
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("SELECT date FROM datetime GROUP BY date")
        lst_data = []
        for el in c.fetchall():
            lst_data.append(el)
        x = 0
        print(len(lst_data))
        print(lst_data)
        if len(lst_data) < 1:
            bot.send_message(message.from_user.id, "Записей нет!")

        else:
            while x <= (len(lst_data) - 1):
                print(x)
                t = f"'{lst_data[x][0]}'"
                print(t)
                db = sqlite3.connect('database.db')
                c = db.cursor()
                c.execute(
                    f"SELECT time,id FROM datetime WHERE date = {t} ORDER BY date ASC")
                lst = []
                for el in c.fetchall():
                    lst.append(el)
                f_lst = np.array(lst)

                u = str(f_lst).strip('[]')
                u2 = u.replace("[", "")
                u3 = u2.replace(']', "\n─── • ───")
                u4 = u3.replace("'", "")
                t2 = t.replace("'", "")

                if f_lst.size < 1:
                    bot.send_message(message.from_user.id, "Доступного для записи времени нет!")
                else:
                    bot.send_message(message.from_user.id,
                                     f'Список доступного времени\nдля записи на <b>{t2}:</b>\n\n{u4}\n\nВведи команду <b>/del2</b> чтобы удалить запись ',
                                     parse_mode='html')
                db.close()
                x += 1


        # db = sqlite3.connect('database.db')
        # c = db.cursor()
        # c.execute("SELECT id, time, date FROM datetime ORDER BY date ASC")
        # lst = []
        # for el in c.fetchall():
        #     lst.append(el)
        # f_lst = np.array(lst)
        # l = f_lst.tolist()
        # x = 0
        # rev_lst = []
        # for i in l:
        #     rev_lst.append(l[x][::-1])
        #     x += 1
        # final_lst = np.array(rev_lst)
        # u = str(final_lst).strip('[]')
        # u2 = u.replace("[", "")
        # u3 = u2.replace(']', "\n───── • ✤ • ─────")
        # u4 = u3.replace("'", " ")
        #
        # if f_lst.size < 1:
        #     bot.send_message(message.from_user.id, "Доступного для записи времени нет")
        # else:
        #     bot.send_message(message.from_user.id, f'<b>Список доступного времени для записи:</b>\n\n{u4}\n\nВведи команду /del2 чтобы удалить запись ',parse_mode= 'html')
        # db.close()

@bot.message_handler(commands=['del2'])
def del_r(message):
    if message.from_user.id == barber_id:
        bot.send_message(message.from_user.id, 'Введи номер записи для удаления\nДля удаления сразу нескольких записей\nвводи в формате <b>"1 2 3 4"</b>',parse_mode='html')
        bot.register_next_step_handler(message, del_r2)

@bot.message_handler(commands=['del2'])
def del_r2(message):
    x = message.text
    input_string = x.split()

    for el in input_string:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("DELETE FROM datetime WHERE id = ?", (el,))
        db.commit()

        bot.send_message(message.from_user.id, f"Запись под номером {el} удалена")
    # x = message.text
    # db = sqlite3.connect('database.db')
    # c = db.cursor()
    # c.execute("DELETE FROM datetime WHERE id = ?", (x,))
    # db.commit()
    #
    # bot.send_message(message.from_user.id, f"Запись под номером {x} удалена")

#Просмотр и удаление всех записей

@bot.message_handler(func=lambda message: message.text == "Показать список записавшихся")
def clients_list(message):
    if message.from_user.id == barber_id and message.text == 'Показать список записавшихся':
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("SELECT date FROM user_info GROUP BY date")
        lst_data = []
        for el in c.fetchall():
            lst_data.append(el)
        x = 0
        if len(lst_data) < 1:
            bot.send_message(message.from_user.id, "Записей нет!")

        else:
            while x <= (len(lst_data) - 1):
                print(x)
                t = f"'{lst_data[x][0]}'"
                print(t)
                db = sqlite3.connect('database.db')
                c = db.cursor()
                c.execute(f"SELECT time,name,service, username, number,id FROM user_info WHERE date = {t} ORDER BY time ASC")
                lst = []
                for el in c.fetchall():
                    lst.append(el)
                f_lst = np.array(lst)

                u = str(f_lst).strip('[]')
                u2 = u.replace("[", "")
                u3 = u2.replace(']', "\n──────── • ✤ • ────────")
                u4 = u3.replace("'", "")
                t2 = t.replace("'","")

                if f_lst.size < 1:
                    bot.send_message(message.from_user.id, "Записей нет!")
                else:
                    bot.send_message(message.from_user.id, f'<b>Список всех записей {t2}:</b>\n\n {u4}\n\nВведи команду <b>/del</b> чтобы удалить запись ', parse_mode='html')
                db.close()
                x += 1




        # db = sqlite3.connect('database.db')
        # c = db.cursor()
        # c.execute("SELECT date,time,name,username,service,number,id FROM user_info ORDER BY date ASC")
        # lst = []
        # for el in c.fetchall():
        #     lst.append(el)
        # f_lst = np.array(lst)
        #
        # u = str(f_lst).strip('[]')
        # u2 = u.replace("[", "")
        # u3 = u2.replace(']', "\n──────── • ✤ • ────────")
        # u4 = u3.replace("'", "")
        #
        # if f_lst.size < 1:
        #     bot.send_message(message.from_user.id, "Записей нет!")
        # else:
        #     bot.send_message(message.from_user.id, f'<b>Список всех записей:</b>\n\n {u4}\n\nВведи команду /del чтобы удалить запись ', parse_mode='html')
        # db.close()

@bot.message_handler(commands=['del'])
def del_reg(message):
    if message.from_user.id == barber_id:
        bot.send_message(message.from_user.id, 'Введи номер записи для удаления\nДля удаления сразу нескольких записей\nвводи в формате <b>"1 2 3 4"</b>',parse_mode='html')
        bot.register_next_step_handler(message, del_reg2)


@bot.message_handler(commands=['del'])
def del_reg2(message):
    x = message.text
    input_string = x.split()

    for el in input_string:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("SELECT user_id FROM user_info WHERE id = ?", (el,))
        l = c.fetchone()
        people_id = l[0]

        c.execute("SELECT * FROM user_info WHERE id = ?", (el,))
        l3 = c.fetchall()
        print(l3)

        c.execute("SELECT time, date FROM user_info WHERE id = ?", (el,))
        l2 = c.fetchall()

        u = str(l2).strip('[]')
        u2 = u.replace("[", "")
        u3 = u2.replace(']', "")
        u4 = u3.replace("'", "")
        u5 = u4.replace("(", "")
        u6 = u5.replace(")", "")
        c.execute("DELETE FROM user_info WHERE id = ?", (el,))
        db.commit()
        bot.send_message(message.from_user.id, f"Запись под номером {el} удалена")




        if l[0] != '':
            bot.send_message(people_id,
                             f"Никита отменил вашу запись на <b>{u6}</b>\nПо вопросам свяжись: <b>@legkoye_kasaniye, +79111516601 </b>!",
                             parse_mode='html')
        else:
            bot.send_message(barber_id,
                             f"Запись удалена, но пользователю не удалось отправить уведомление об отмене записи\nНе удалось сохранить ID пользователя\nНапиши ему сам {l3}")


#установка времени для записи

@bot.message_handler(func=lambda message: message.text == "Создать время для записи")
def set_date(message):
    if message.from_user.id == barber_id and message.text == 'Создать время для записи':
        bot.send_message(message.from_user.id, 'Введи дату в которую ты будешь работать: ')
        bot.register_next_step_handler(message, set_date2)
    else:
        bot.send_message(message.from_user.id, 'Не понимаю о чем ты')

@bot.message_handler(commands=['set2'])
def set_date2(message):
    global work_date
    work_date = message.text
    bot.send_message(message.from_user.id, 'Теперь введи время в которое будешь работать:\nВводи в формате "10:00 11:00 12:00"')
    bot.register_next_step_handler(message, set_time)

@bot.message_handler(commands=['set2'])
def set_time(message):
    global work_time
    work_time = message.text
    list_time = work_time.split()


    # db = sqlite3.connect('database.db')
    # c = db.cursor()
    # c.execute("SELECT id FROM datetime")
    # id_null = c.fetchall()
    # print(id_null[0][0])
    # print(id_null[-1][0])
    # print(id_null)
    # el = 1
    # if id_null[0][0] != 1:
    #     for el in range(id_null[-1][0]):
    #         print(el)
    #         db = sqlite3.connect('database.db')
    #         c = db.cursor()
    #         c.execute(f"
    #         db.commit()
    #         db.close()
    #         el += 1







    #БД сохраняем
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute("SELECT id FROM datetime")
    id = c.fetchall()
    print(id)

    if len(id) == 0:
        id3 = 1
    else:
        id2 = id[-1][0]
        id3 = id2 + 1
    for el in list_time:
        print(el)
        c.execute("INSERT INTO datetime VALUES (?, ?, ?)",
              (id3, work_date, el))
        id3 += 1
    db.commit()
    db.close()

    bot.send_message(message.from_user.id, 'Дата и время сохранены')

@bot.message_handler(func=lambda message: message.text == "История посещений клиента")
def client_history(message):
    if message.from_user.id == barber_id and message.text == 'История посещений клиента':
        bot.send_message(message.from_user.id, 'Введи номер телефона клиента\n\nВводи в формате <b>79993332211</b>', parse_mode='html')
        bot.register_next_step_handler(message, client_history2)

def client_history2(message):
    if message.from_user.id == barber_id:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute(f"SELECT username, service, name, time, date FROM user_info WHERE number = {message.text} ORDER BY date ASC")
        lst = []
        for el in c.fetchall():
            lst.append(el)
        f_lst = np.array(lst)
        l = f_lst.tolist()
        x = 0
        rev_lst = []
        for i in l:
            rev_lst.append(l[x][::-1])
            x += 1
        final_lst = np.array(rev_lst)
        u = str(final_lst).strip('[]')
        u2 = u.replace("[", "")
        u3 = u2.replace(']', "\n──────── • ✤ • ────────")
        u4 = u3.replace("'", " ")

        if f_lst.size < 1:
            bot.send_message(message.from_user.id, f"Нет информации о клиенте c номером {message.text}")
        else:
            bot.send_message(message.from_user.id,
                             f'<b>Список всех записей клиента с номером {message.text}:</b>\n{u4}\n\n',
                             parse_mode='html')
        db.close()





@bot.message_handler(func=lambda message: message.text == "Записать на стрижку")
def barber_reg(message):
    markup = types.InlineKeyboardMarkup()
    complex = types.InlineKeyboardButton("Комплекс", callback_data='Комплекс')
    strizhka = types.InlineKeyboardButton("Стрижка", callback_data='Стрижка')
    boroda = types.InlineKeyboardButton("Борода", callback_data='Борода')
    markup.add(complex, strizhka, boroda)
    if message.text == 'Записать на стрижку':
        bot.send_message(message.from_user.id, 'Напиши свое имя',
                         parse_mode='html')
        bot.register_next_step_handler(message, get_name)


@bot.message_handler()
def first_que(message):
    global call_user_id
    call_user_id = message.from_user.id

    if message.text == 'Записаться на стрижку':
        bot.send_message(message.chat.id, 'Напиши свое имя')
        bot.register_next_step_handler(message, get_name)
    elif message.text == 'Нет, запишусь попозже':
        bot.send_message(message.chat.id, 'Хорошо, не задерживайся\nЛюбая стрижка держится <b>2-3 недели</b>', parse_mode='html')
    elif message.text == 'Мои записи':
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute(f"SELECT service, time, date FROM user_info WHERE user_id = {message.from_user.id} ORDER BY date ASC")
        lst = []
        for el in c.fetchall():
            lst.append(el)
        f_lst = np.array(lst)
        l = f_lst.tolist()
        x = 0
        rev_lst = []
        for i in l:
            rev_lst.append(l[x][::-1])
            x += 1
        final_lst = np.array(rev_lst)
        u = str(final_lst).strip('[]')
        u2 = u.replace("[", "")
        u3 = u2.replace(']', "\n───── • ✤ • ─────")
        u4 = u3.replace("'", " ")

        if f_lst.size < 1:
            bot.send_message(message.from_user.id, "У тебя еще не было записей!")
        else:
            bot.send_message(message.from_user.id,
                             f'<b>Список всех твоих записей:\n</b>\n{u4}\n\n<b>Для отмены записи свяжись с Никитой:\n@legkoye_kasaniye\n+79111516601</b>',
                             parse_mode='html')
        db.close()


    elif message.text == 'Посмотреть доступное время для записи':
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("SELECT date FROM datetime GROUP BY date")
        lst_data = []
        for el in c.fetchall():
            lst_data.append(el)
        x = 0
        if len(lst_data) < 1:
            bot.send_message(message.from_user.id, "Записей нет!")

        else:
            while x <= (len(lst_data) - 1):
                print(x)
                t = f"'{lst_data[x][0]}'"
                print(t)
                db = sqlite3.connect('database.db')
                c = db.cursor()
                c.execute(
                    f"SELECT time FROM datetime WHERE date = {t} ORDER BY time ASC")
                lst = []
                for el in c.fetchall():
                    lst.append(el)
                f_lst = np.array(lst)

                u = str(f_lst).strip('[]')
                u2 = u.replace("[", "")
                u3 = u2.replace(']', "\n─ • ─")
                u4 = u3.replace("'", "")
                t2 = t.replace("'", "")

                if f_lst.size < 1:
                    bot.send_message(message.from_user.id, "Доступного для записи времени нет")
                else:
                    bot.send_message(message.from_user.id,
                                     f'Список доступного времени\nдля записи на <b>{t2}:</b>\n\n{u4}',
                                     parse_mode='html')
                db.close()
                x += 1



    elif message.text == 'Контакты и Геолокация':
        markup2 = types.InlineKeyboardMarkup()
        dgis = types.InlineKeyboardButton('2GIS', url= 'https://2gis.ru/spb/geo/70000001046953459')
        yandex = types.InlineKeyboardButton('Яндекс Карты', url= 'https://yandex.ru/maps/-/CCUF6LgbPC')
        tg_channel = types.InlineKeyboardButton('Telegram канал', url= 'https://t.me/successful_haircut')
        markup2.add(dgis, yandex, tg_channel)
        smile = emoji.emojize(':circled_M:')
        bot.send_message(message.chat.id, f'<b>Никита Барбер:</b> @legkoye_kasaniye, +79111516601\n\nВопросы и предложения по разработке бота: @Auuuauuausu\n\n<b>Геолокация:</b> СПб, {smile}Владимирская, Достоевская\nВладимирский проспект 13/9, Бьюти Коворкинг',parse_mode='html',reply_markup=markup2)
    else:
        bot.send_message(message.chat.id, 'Не понимаю тебя\n<b>Нажми /start</b>', parse_mode='html')

@bot.message_handler(content_types=['text'])
def get_name(message):
    if 'Записаться на стрижку' in message.text:
        bot.register_next_step_handler(message, start)
        bot.send_message(message.from_user.id, 'Для того чтобы начать заново\nНажми <b>/start</b>', parse_mode='html')
    elif '/' in message.text:
        bot.register_next_step_handler(message, start)
        bot.send_message(message.from_user.id, 'Для того чтобы начать заново\nНажми <b>/start</b>', parse_mode='html')
    else:
        global name
        name = message.text
        bot.send_message(message.from_user.id, 'Введи свой номер телефона\n\nВводи в формате <b>79993332211</b>',
                         parse_mode='html')
        bot.register_next_step_handler(message, get_number)

@bot.message_handler(content_types=['text'])
def get_number(message):
    if 'Записаться на стрижку' in message.text:
        bot.register_next_step_handler(message, start)
        bot.send_message(message.from_user.id, 'Для того чтобы начать заново\nНажми <b>/start</b>', parse_mode='html')
    elif '/' in message.text:
        bot.register_next_step_handler(message, start)
        bot.send_message(message.from_user.id, 'Для того чтобы начать заново\nНажми <b>/start</b>', parse_mode='html')
    else:
        if (len(message.text) == 11 and message.text[0] == '7'):
            global number
            number = message.text
            db = sqlite3.connect('database.db')
            c = db.cursor()
            c.execute("SELECT id FROM datetime ")
            total = c.fetchall()
            if len(total) == 0:
                i = 1
            else:
                i = total[-1][0]

            markup = types.InlineKeyboardMarkup()
            complex = types.InlineKeyboardButton("Комплекс", callback_data='Комплекс')
            strizhka = types.InlineKeyboardButton("Стрижка", callback_data='Стрижка')
            boroda = types.InlineKeyboardButton("Борода", callback_data='Борода')
            markup.add(complex, strizhka, boroda)
            bot.send_message(message.from_user.id, '<b>Выбери услугу</b>', parse_mode='html', reply_markup=markup)

        else:
            bot.send_message(message.from_user.id,
                             'Ты ввел номер телефона в неправильном формате\nВводи в формате <b>79993332211</b>',
                             parse_mode='html')
            bot.register_next_step_handler(message, get_number)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global lst_service
    global username
    if call.data in lst_service:
        global service
        global markup_date
        service = call.data
        global lst_date
        conn = sqlite3.connect('database.db')
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        lst = c.execute('SELECT date FROM datetime ORDER BY date ASC').fetchall()
        lst_date = []

        for el in lst:
            if el not in lst_date:
                lst_date.append(el)

        markup_date = types.InlineKeyboardMarkup()
        markup_date.row_width = 2
        back = types.InlineKeyboardButton('⏎', callback_data='back')
        for i in range(0, len(lst_date)):
            markup_date.add(types.InlineKeyboardButton(lst_date[i], callback_data=lst_date[i]))
        markup_date.add(back)
        if len(lst_date) < 1:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<b>Нет свободных дат для записи</b>',parse_mode='html')
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>Список доступных дат для записи:</b>",parse_mode='html', reply_markup=markup_date)
        conn.close()


    if call.data in lst_date:
        global date
        date = call.data
        global lst_time
        d = f"'{date}'"
        conn = sqlite3.connect('database.db')
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        lst = c.execute(f'SELECT time FROM datetime WHERE date = {str(d)} ORDER BY time ASC').fetchall()
        lst_time = []
        for el in lst:
            if el not in lst_time:
                lst_time.append(el)

        markup = types.InlineKeyboardMarkup()
        markup.row_width = 2
        back = types.InlineKeyboardButton('⏎', callback_data='back_to_date')
        for i in range(0, len(lst_time)):
            markup.add(types.InlineKeyboardButton(lst_time[i], callback_data=lst_time[i]))
        markup.add(back)
        if len(lst_time) < 1:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<b>Нет свободных дат для записи</b>',parse_mode='html')
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Список доступного времени для записи:</b>",parse_mode='html', reply_markup=markup)
        conn.close()

    if call.data in lst_time:
        global time
        time = call.data
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Да, все верно', callback_data='ok')
        btn2 = types.InlineKeyboardButton('Нет, начать заново', callback_data='no')
        markup.add(btn1,btn2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Вы хотите записаться на <b>{service} {date} в {time}?</b>", parse_mode='html',
                              reply_markup=markup)

    if call.data == 'ok':
        global name
        global number
        sticker = open('thanks.jpeg', 'rb')
        bot.send_sticker(call.message.chat.id, sticker)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Поздравляю, запись создана на <b>{service} {date} в {time}!</b>', parse_mode='html')
        bot.send_message(to_chat_id, f'К тебе записался {name} на {service} c номером {number} на {date} в {time}\nБудь готов!\nTELEGRAM: @{call.from_user.username}')

        # Cохраняем в БД записей
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("SELECT id FROM user_info")
        id = c.fetchall()
        lst = []
        if len(id) == 0 or id[-1][0] == lst:
            id3 = 1
        else:
            id2 = id[-1][0]
            id3 = id2 + 1
        c.execute("INSERT INTO user_info VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (id3, user_id, name, number, service, time, date, username))
        db.commit()
        db.close()

        # удаляем из БД доступного времени
        db = sqlite3.connect('database.db')
        c = db.cursor()
        t = f'"{time}"'
        c.execute(f"DELETE FROM datetime WHERE time = {str(t)}")
        db.commit()
        db.close()

    if call.data == 'no':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Хорошо, давай попробуем заново!',
                              parse_mode='html')
        bot.send_message(call.message.chat.id, 'Для того чтобы начать заново\nНажми <b>/start</b>', parse_mode='html')

    if call.data == 'back':
        markup = types.InlineKeyboardMarkup()
        complex = types.InlineKeyboardButton("Комплекс", callback_data='Комплекс')
        strizhka = types.InlineKeyboardButton("Стрижка", callback_data='Стрижка')
        boroda = types.InlineKeyboardButton("Борода", callback_data='Борода')
        markup.add(complex, strizhka, boroda)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<b>Выбери услугу</b>', parse_mode='html', reply_markup=markup)

    if call.data == 'back_to_date':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="<b>Список доступных дат для записи:</b>",parse_mode='html', reply_markup=markup_date)



















#RUN bot



bot.polling(none_stop=True, interval=0)