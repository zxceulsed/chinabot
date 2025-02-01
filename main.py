# bot.py

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputFile
from keyboards import main_menu_keyboard, FAQ_keyboard, society_keyboard,otzivi_keyboard, raschit_keyboard,nazad_v_menu_keyboard, oform_keyboard,TOVAR_keyboard
import os
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramBadRequest
import sqlite3

API_TOKEN = '7220938510:AAG5hMlCREOXmgFJyXoc1cVZOm1RLBC5Cd4'
ADMIN_IDS = [7120064259,1085598151]
class OrderStates(StatesGroup):
    waiting_for_price_buttons = State()  # Ожидание ввода цены (из кнопок)
    waiting_for_photo = State()          # Ожидание фото товара
    waiting_for_link = State()           # Ожидание ссылки на товар
    waiting_for_price_link = State()     # Ожидание ввода цены (после ссылки)
    waiting_for_new_rate = State()
    waiting_for_delete_item = State()

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    button_data = {
        "Poizon": {
            "text": """
1. Выберите нужный товар на Poizon и нажмите на правую нижнюю кнопку
2. Выберите нужный размер и напишите цену, которая показана первой""",
            "photos": ["poizon_image1.jpg", "poizon_image2.jpg"],
        },
        "Taobao": {
            "text": """1. Выберите нужный товар на Taobao и нажмите на правую нижнюю кнопку
2. Выберите нужный цвет/размер и напишите цену (или общую сумму за нужное вам количество), которая показана сверху""",
            "photos": ["photo1_taobao.jpg", "photo2_taobao.jpg"],
        },
        "1688": {
            "text": """1. Выберите нужный товар на 1688 и нажмите на правую нижнюю кнопку (обращайте внимание на цену за определённое количество)
2. Выберите нужный цвет/размер и напишите цену (или общую сумму за нужное вам количество), которая показана снизу""",
            "photos": ["photo1_1688.jpg", "photo2_1688.jpg"],
        },
        "Pinduoduo": {
            "text": """1. Выберите нужный товар на Pinduoduo. В карточке товара снизу 2 кнопки (🔵 - одиночная покупка, 🟢 - парная покупка)
2. Выберите нужный цвет/размер и напишите цену (или общую сумму за нужное вам количество), которая показана сверху""",
            "photos": ["photo1_pinduoduo.jpg", "photo2_pinduoduo.jpg"],
        },
        "95": {
            "text": """
1. Выберите понравившийся товар на 95 и нажмите на обведённую кнопку
2. Выберите нужный размер и напишите цену, которая показана на зелёной кнопке снизу""",
            "photos": ["photo1_95.jpg", "photo2_95.jpg"],
        },
    }

    def create_db():
        # Подключаемся к базе данных (если она не существует, она будет создана)
        conn = sqlite3.connect('currency.db')
        cursor = conn.cursor()
        
        # Создаём таблицу для хранения курса валюты
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS currency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rate REAL
        )
        ''')

        # Создаём таблицу для хранения данных о заказах
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Уникальный идентификатор записи
            user_id INTEGER,                        -- ID пользователя
            link TEXT,                              -- Ссылка на товар
            price_yuan FLOAT,                       -- Цена в юанях
            price_byn FLOAT,                        -- Цена в BYN
            photo TEXT                              -- Ссылка на фото
        )
        ''')

        conn.commit()
        conn.close()

    # Вызов функции для создания таблиц
    create_db()



    @dp.message(F.text == "Изменить курс")
    async def handle_change_rate(message: Message, state: FSMContext):
        # Проверка, является ли пользователь администратором
        if message.from_user.id not in ADMIN_IDS:
            await message.answer("У вас нет прав для изменения курса.")
            return
        
        # Запрашиваем новый курс
        await message.answer("Пожалуйста, отправьте новый курс в формате числа.")
        await state.set_state(OrderStates.waiting_for_new_rate)


    @dp.message(OrderStates.waiting_for_new_rate)
    async def process_new_rate(message: Message, state: FSMContext):
        # Проверка, что сообщение — это число
        try:
            new_rate = float(message.text)
        except ValueError:
            await message.answer("Пожалуйста, введите правильное число.")
            return
        
        # Подключаемся к базе данных и обновляем курс
        conn = sqlite3.connect('currency.db')
        cursor = conn.cursor()
        
        # Проверяем, есть ли уже запись в таблице
        cursor.execute('SELECT * FROM currency WHERE id = 1')
        result = cursor.fetchone()
        
        if result is None:
            # Если записи нет, вставляем новый курс
            cursor.execute('INSERT INTO currency (rate) VALUES (?)', (new_rate,))
            await message.answer(f"Курс успешно установлен: {new_rate} BYN.")
        else:
            # Если курс уже есть, обновляем его
            cursor.execute('UPDATE currency SET rate = ? WHERE id = 1', (new_rate,))
            await message.answer(f"Курс успешно обновлён на: {new_rate} BYN.")
        
        conn.commit()
        conn.close()
        
        # Очищаем состояние после обработки
        await state.clear()

    @dp.message(CommandStart())
    async def cmd_start(message: Message):
        await message.answer("🔎 Главное меню",reply_markup=main_menu_keyboard())


    @dp.message(F.text == "❓Часто задаваемые вопросы")
    async def FAQ_cmd(message:Message):
        await message.answer("Выберите интересующий вопрос в меню.",reply_markup=FAQ_keyboard())


    @dp.message(F.text == "Кто мы?")
    async def first_question(message:Message):
        await message.answer("Мы являемся посредником в работе с Китаем. Через нас вы можете заказать любой товар, с любого китайского сайта 🇨🇳")

    @dp.message(F.text == "Как происходит расчёт?")
    async def second_question(message: Message):
        # Подключаемся к базе данных
        conn = sqlite3.connect('currency.db')
        cursor = conn.cursor()
        
        # Получаем курс из базы данных
        cursor.execute('SELECT rate FROM currency WHERE id = 1')
        result = cursor.fetchone()
        conn.close()

        if result is None or result[0] == 0:
            # Если курс не найден или равен 0
            await message.answer("Актуальный курс не установлен. Обратитесь к администратору.")
            return
        
        # Рассчитываем актуальный курс
        rate = float(result[0])
        actual_rate = 1 / rate
        
        # Формируем сообщение
        await message.answer(f"""Актуальный курс: 1¥ = {actual_rate:.2f} BYN
    Т.е. стоимость в ¥ • {actual_rate:.2f} BYN = стоимость вашей позиции в BYN

    + 5% комиссия выкупа (оплата товара, связь с продавцом и доставка по Китаю)""")


    @dp.message(F.text == "Стоимость и сроки доставки?")
    async def third_question(message:Message):
        await message.answer("""За доставку из Китая вы оплачиваете по прибытии заказа к нам на склад в Беларусь

🚀 Сроки доставки - 3.5-4 недели

💰 Наши тарифы:
До 5кг - 14$/кг
От 5кг до 15кг - 12$/кг
От 15 до 40кг - 10$/кг
От 40кг - менее 10$/кг (условия оговариваются индивидуально)
Примечание: заказ взвешивается вместе с упаковкой, в которую упаковывают китайские поставщики (то есть, кроссовки с Poizon взвешиваются вместе с коробкой бренда и коробкой Poizon)""")

    @dp.message(F.text == "Как узнать нужный размер?")
    async def four_question(message:Message):
        await message.answer("""Помощь в выборе размера оказывает наш менеджер каждому в индивидуальном порядке. Если у вас возникли трудности при выборе размера, лучше всего сразу пишите ему 👉 @frolovshop24""")

    @dp.message(F.text == "Вернуться в меню ⬅️️️")
    async def back_to_menu_iz_faq(message:Message):
        await message.answer("🔎 Главное меню",reply_markup=main_menu_keyboard())

    @dp.message(F.text == "📱 Наши соц.сети")
    async def five_cmd(message:Message):
        await message.answer("Наши соц.сети:",reply_markup=society_keyboard())


    @dp.message(F.text == "📌 Отзывы покупателей")
    async def four_button(message:Message):
        await message.answer("Посмотрите, что пишут о нас наши клиенты",reply_markup=otzivi_keyboard()) 

    @dp.message(F.text == "👨‍💻 Связаться с менеджером")
    async def manager_cmd(message:Message):
        await message.answer("""По всем вопросам вы можете обращаться к нашему менеджеру
👉 @frolovshop24

Также он может помочь вам найти желаемый товар или полностью сопроводить оформление заказа, если у вас возникают трудности""")


    @dp.message(F.text == "🛒 Рассчитать стоимость товара")
    async def first_cmd(message:Message):
        await message.answer("""Выберите площадку, с которой вы хотели бы оформить заказ
    ❗️На каждой площадке присутствует поиск по фото""",reply_markup=raschit_keyboard())
        await message.answer("Для того чтобы ознакомиться с инструкцией по установке приложений, нажмите на кнопку «Инструкция по установке приложений»")
        await message.answer("""Если у вас возникают трудности при поиске товара или расчёта стоимости - наш менеджер с радостью вам поможет
    👉@frolovshop24""")

    @dp.message(F.text == "Другая площадка")
    async def other_place(message:Message):
        await message.answer("""Для заказа с любой другой площадки свяжитесь с нашим менеджером
👨‍💻 @frolovshop24""",reply_markup=main_menu_keyboard())

    @dp.message(F.text == "Инструкция по установке приложений")
    async def instructions_cmd(message:Message):
        await message.answer("По вопросам установки и использования приложений китайских площадок временно обращайтесь к менеджеру за помощью 👉 @frolovshop24",reply_markup=main_menu_keyboard())

    @dp.message(F.text == "Вернуться назад⬅️️️")
    async def vernytsa_nazad(message:Message):
        await message.answer("🔎 Главное меню",reply_markup=main_menu_keyboard())


    @dp.message(F.text == '🔙 Назад в меню')
    async def nazad_v_menu_2(message: types.Message, state: FSMContext):
        await message.answer("Действие отменено",reply_markup=main_menu_keyboard())
        await state.clear()


    @dp.message(F.text.in_(button_data.keys()))
    async def handle_buttons(message: types.Message, state: FSMContext):
        button_name = message.text  # Получаем текст кнопки
        data = button_data[button_name]  # Берем данные из словаря

        await message.answer(
            "Введите стоимость товара в юанях (¥)\n"
            "❗️В случае, если вы хотите заказать несколько штук одной модели, вводите суммарное число",
            reply_markup=nazad_v_menu_keyboard()
        )

        # Отправляем медиагруппу с фотографиями и описанием
        media = []
        for index, photo_path in enumerate(data["photos"]):
            if index == 0:
                media.append(InputMediaPhoto(media=FSInputFile(photo_path), caption=data["text"]))
            else:
                media.append(InputMediaPhoto(media=FSInputFile(photo_path)))

        try:
            await bot.send_media_group(chat_id=message.chat.id, media=media)
        except TelegramBadRequest:
            await message.answer("Ошибка при отправке фотографий. Проверьте файлы.")

        # Устанавливаем состояние ожидания цены
        await state.set_state(OrderStates.waiting_for_price_buttons)

    @dp.message(OrderStates.waiting_for_price_buttons)
    async def calculate_price_buttons(message: types.Message, state: FSMContext):
        try:
            # Подключаемся к базе данных
            conn = sqlite3.connect('currency.db')
            cursor = conn.cursor()
            
            # Получаем коэффициент из базы данных
            cursor.execute('SELECT rate FROM currency WHERE id = 1')
            result = cursor.fetchone()
            conn.close()

            if result is None or result[0] == 0:
                await message.answer("Курс не установлен. Обратитесь к администратору.")
                return
            
            # Извлекаем коэффициент
            rate = float(result[0])

            # Преобразуем введенную цену
            price = float(message.text)
            final_price = (price + price * 0.17) / rate  # Используем коэффициент из базы данных

            # Формируем сообщение с итоговой стоимостью
            await message.answer(
                f"Итоговая стоимость: {final_price:.2f} BYN\n"
                "+ доставка из Китая (оплачивается по прибытии товара в Беларусь, чем больше вес, тем дешевле цена доставки за кг)\n"
                "+ услуги почты", 
                reply_markup=oform_keyboard()
            )
            await state.clear()
        except ValueError:
            await message.answer("Пожалуйста, введите корректное число (целое или дробное).")


    @dp.message(F.text== "Оформить заказ 📝")
    async def oform_cmd(message:Message,state:FSMContext):
        await message.answer("Отправьте фотографию товара",reply_markup=nazad_v_menu_keyboard())
        await state.set_state(OrderStates.waiting_for_photo)

    @dp.message(OrderStates.waiting_for_photo)
    async def process_photo(message: Message, state: FSMContext):
        # Проверяем, есть ли в сообщении фото
        if message.photo:
            # Получаем фото из сообщения (самая большая версия)
            photo = message.photo[-1]  # Это безопасно, так как мы уже проверили наличие фото
            
            # Сохраняем ссылку на фото в FSM
            photo_link = photo.file_id

            await state.update_data(photo=photo_link)  # Сохраняем ссылку на фото

            await message.answer("Теперь отправьте ссылку на товар.")
            await state.set_state(OrderStates.waiting_for_link)
        else:
            # Если фото нет, просим пользователя отправить фото
            await message.answer("Пожалуйста, отправьте фотографию товара.")



    # Хендлер для ссылки на товар
    @dp.message(OrderStates.waiting_for_link)
    async def process_link(message: types.Message, state: FSMContext):
        link = message.text  # Сохраняем ссылку
        await state.update_data(link=link)  # Сохраняем в FSM
        await message.answer("Пришлите цену товара в юанях (¥).")
        await state.set_state(OrderStates.waiting_for_price_link)

    def get_current_rate():
        conn = sqlite3.connect('currency.db')
        cursor = conn.cursor()
        cursor.execute('SELECT rate FROM currency WHERE id = 1')
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 1  # Возвращаем курс или 1, если курс не найден


    @dp.message(OrderStates.waiting_for_price_link)
    async def process_price(message: Message, state: FSMContext):
        try:
            price_yuan = float(message.text)
            rate = get_current_rate()  # Получаем актуальный курс из базы данных
            price_byn = (price_yuan + price_yuan * 0.17) / rate  # Расчет цены в BYN

            # Получаем данные FSM
            data = await state.get_data()
            link = data.get("link")
            photo = data.get("photo")
            user_id = message.from_user.id

            # Сохраняем данные товара в базу данных
            conn = sqlite3.connect('currency.db')
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO orders (user_id, link, price_yuan, price_byn, photo)
            VALUES (?, ?, ?, ?, ?)
            ''', (user_id, link, price_yuan, price_byn, photo))
            conn.commit()
            conn.close()

            # Получаем все товары пользователя из базы данных
            conn = sqlite3.connect('currency.db')
            cursor = conn.cursor()
            cursor.execute('SELECT link, price_byn, photo FROM orders WHERE user_id = ?', (user_id,))
            orders = cursor.fetchall()
            conn.close()

            # Формируем итоговое сообщение
            total_price = sum(order[1] for order in orders)  # Суммируем все цены в BYN
            items_list = "\n".join([f"{i+1}. {order[0]} | {order[1]:.2f} BYN" for i, order in enumerate(orders)])

            # Формируем список медиа с описанием только для первого фото
            media_group = []
            for index, order in enumerate(orders):
                if index == 0:
                    media_group.append(InputMediaPhoto(media=order[2], caption=(
                        f"🛒 Товаров: {len(orders)}\n"
                        f"{items_list}\n\n"
                        f"Итоговая сумма: {total_price:.2f} BYN\n\n"
                        "🚛 По прибытии товара в Беларусь вы оплачиваете за доставку Китай-Беларусь + за услуги почты до вас"
                    )))
                else:
                    media_group.append(InputMediaPhoto(media=order[2]))

            # Отправляем фото в одном сообщении
            try:
                await message.answer_media_group(media=media_group)
            except TelegramBadRequest:
                await message.answer("Ошибка при отправке фотографий. Проверьте файлы.")
            await message.answer(
                "Выберите нужную опцию:",
                reply_markup=TOVAR_keyboard()
            )
            # Завершаем процесс
            await state.clear()

        except ValueError:
            await message.answer("Пожалуйста, введите корректную цену товара.")


    @dp.message(F.text == "Отправить заявку менеджеру")
    async def zayavka_cmd(message: Message):
        user_id = message.from_user.id
        
        # Получаем товары пользователя из базы данных
        conn = sqlite3.connect('currency.db')
        cursor = conn.cursor()
        cursor.execute('SELECT link, price_yuan, price_byn, photo FROM orders WHERE user_id = ?', (user_id,))
        orders = cursor.fetchall()
        conn.close()

        if not orders:
            await message.answer("У вас нет товаров для отправки.")
            return

        # Формируем итоговое сообщение для администраторов
        total_price = sum(order[2] for order in orders)
        items_list = "\n".join([f"{i+1}. {order[0]} | {order[1]:.2f} ¥ | {order[2]:.2f} BYN" for i, order in enumerate(orders)])

        # Создаем кликабельную ссылку на пользователя
        user = message.from_user
        username = f"@{user.username}" if user.username else user.full_name
        user_link = f"[{username}](tg://user?id={user.id})"

        caption = (
            f"🛒 Пользователь {user_link} отправил заявку:\n\n"
            f"{items_list}\n\n"
            f"Итоговая сумма: {total_price:.2f} BYN\n"
        )

        # Отправляем товары администраторам
        for admin_id in ADMIN_IDS:
            try:
                media_group = []
                for index, order in enumerate(orders):
                    if index == 0:
                        media_group.append(InputMediaPhoto(
                            media=order[3],
                            caption=caption,
                            parse_mode="Markdown"
                        ))
                    else:
                        media_group.append(InputMediaPhoto(media=order[3]))

                await bot.send_media_group(chat_id=admin_id, media=media_group)

            except TelegramBadRequest:
                await bot.send_message(admin_id, f"Ошибка при отправке заявки от пользователя {user.id}. Проверьте данные.")

        await message.answer("✅ Ваша заявка успешно отправлена менеджеру!", reply_markup=main_menu_keyboard())
            
    @dp.message(F.text == "Удалить Товар")
    async def otmena_zakaza(message: Message, state: FSMContext):
        user_id = message.from_user.id
        
        # Получаем список товаров пользователя из базы данных
        conn = sqlite3.connect('currency.db')
        cursor = conn.cursor()
        cursor.execute('SELECT rowid, link, price_byn FROM orders WHERE user_id = ?', (user_id,))
        orders = cursor.fetchall()
        conn.close()

        if not orders:
            await message.answer("У вас нет товаров для удаления.")
            return

        # Сохраняем данные товаров в состояние
        items = {i + 1: order[0] for i, order in enumerate(orders)}  # Номер товара -> rowid из БД
        await state.update_data(items=items)

        # Формируем список товаров для вывода
        items_list = "\n".join([f"{i+1}. {order[1]} | {order[2]:.2f} BYN" for i, order in enumerate(orders)])
        await message.answer(
            f"Ваши товары:\n\n{items_list}\n\nВведите номер товара, который хотите удалить:"
        )

        # Устанавливаем состояние ожидания номера товара
        await state.set_state(OrderStates.waiting_for_delete_item)


    @dp.message(OrderStates.waiting_for_delete_item)
    async def process_delete_item(message: Message, state: FSMContext):
        try:
            # Получаем данные из состояния
            data = await state.get_data()
            items = data.get("items")

            # Парсим номер товара
            item_number = int(message.text)
            if item_number not in items:
                await message.answer("Неверный номер товара. Попробуйте снова.")
                return

            # Удаляем товар из базы данных
            rowid_to_delete = items[item_number]
            conn = sqlite3.connect('currency.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM orders WHERE rowid = ?', (rowid_to_delete,))
            conn.commit()
            conn.close()

            # Получаем обновленный список товаров
            conn = sqlite3.connect('currency.db')
            cursor = conn.cursor()
            cursor.execute('SELECT link, price_byn, photo FROM orders WHERE user_id = ?', (message.from_user.id,))
            updated_orders = cursor.fetchall()
            conn.close()

            if not updated_orders:
                await message.answer("У вас не осталось товаров.", reply_markup=main_menu_keyboard())
                await state.clear()
                return

            # Формируем список медиа с описанием только для первого фото
            media_group = []
            total_price = sum(order[1] for order in updated_orders)  # Суммируем все цены в BYN
            updated_items_list = "\n".join(
                [f"{i+1}. {order[0]} | {order[1]:.2f} BYN" for i, order in enumerate(updated_orders)]
            )

            for index, order in enumerate(updated_orders):
                if index == 0:
                    media_group.append(
                        InputMediaPhoto(
                            media=order[2],
                            caption=(
                                f"🛒 Ваши обновленные товары:\n\n"
                                f"{updated_items_list}\n\n"
                                f"Итоговая сумма: {total_price:.2f} BYN\n\n"
                                "🚛 По прибытии товара в Беларусь вы оплачиваете за доставку Китай-Беларусь + за услуги почты до вас."
                            )
                        )
                    )
                else:
                    media_group.append(InputMediaPhoto(media=order[2]))

            # Отправляем медиагруппу
            await message.answer_media_group(media=media_group)

            # Завершаем процесс
            await state.clear()

        except ValueError:
            await message.answer("Пожалуйста, введите корректный номер товара.")



    @dp.message(F.text == "Отменить заказ")
    async def otmena_zakaza(message: Message):
        try:
            # Подключаемся к базе данных
            conn = sqlite3.connect('currency.db')
            cursor = conn.cursor()

            # Получаем user_id пользователя
            user_id = message.from_user.id

            # Удаляем все товары пользователя из таблицы orders
            cursor.execute('DELETE FROM orders WHERE user_id = ?', (user_id,))
            conn.commit()

            # Закрываем соединение с базой данных
            conn.close()

            # Отправляем пользователю сообщение
            await message.answer("Ваш заказ отменен. Все товары удалены.",reply_markup=main_menu_keyboard())

        except sqlite3.Error as e:
            await message.answer(f"Ошибка базы данных: {e}")

    @dp.message(F.text == "Добавить товар")
    async def add_tovar(message:Message, state:FSMContext):
        await message.answer("Отправьте фотографию товара",reply_markup=nazad_v_menu_keyboard())
        await state.set_state(OrderStates.waiting_for_photo)


    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
