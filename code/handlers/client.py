import emoji
import asyncio
import config
import requests
import ccxt.async_support as ccxt
from aiogram import types, Dispatcher
from bot import dp, bot, TEXT
from keyboard import kb_client
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType


exchange = ccxt.wavesexchange()

price = None
title = None
deskription = None


@dp.message_handler(commands=['Подтвердить_платёж'])
async def payment(message: types.Message):
    global price
    if price is None:
        await message.answer('Вы не выбрали опирацию')
        print(price)
        return

    await bot.send_invoice(message.chat.id,
                           title=title,
                           description=deskription,
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="usd",
                           photo_url="https://tradesanta.com/blog/wp-content/uploads/2022/08/usdt-btc-1.png",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[price],
                           start_parameter="buyOrderBTCUSDT",
                           payload="invoice-payload")


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    global price
    global title
    global deskription
    print("SUCCESSFUL PAYMENT:")
    print(f'{message.from_user.first_name} = {message.from_user.url}')
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    price = None
    title = None
    deskription = None

    await bot.send_message(message.chat.id,
                           f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!",
                           reply_markup=kb_client)


class Buy(StatesGroup):
    amount = State()
    price = State()


class Sell(StatesGroup):
    amount = State()
    price = State()


async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, TEXT, reply_markup=kb_client)


async def get_rate(message: types.Message):
    global exchange
    orderbook = await exchange.fetch_order_book('BTC-WXG/USDT-WXG')
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    spread = (ask - bid) if (bid and ask) else None
    price = f'цена продажи: {bid}, цена покупки: {ask}, разброс: {spread}'

    stonks = emoji.emojize(':chart_increasing:')
    arrow = emoji.emojize(':right_arrow:')
    result = (f'Текущий курс {stonks}\nBTC-WXG/USDT-WXG\nна криптобирже waves.exchange {arrow}\n{price}')

    await bot.send_message(message.from_user.id, result)
    await exchange.close()


async def buy(message: types.Message):
    await message.answer('Введите сколько вы хотите купить BTC:')
    await Buy.amount.set()


async def get_amount(message: types.Message, state: FSMContext):
    try:
        answer = float(message.text)
        await state.update_data(amount=answer)
        await message.answer('Введите по какой цене вы хотите купить BTC:')
        await Buy.next()
    except:
        await bot.send_message(message.from_user.id, 'Вы ввели не число!\nНачните с начала!', reply_markup=kb_client)
        await state.finish()


async def get_price(message: types.Message, state: FSMContext):
    global exchange
    global price
    global title
    global deskription

    try:
        data = await state.get_data()

        priceforone = float(message.text)
        amount = data.get('amount')
        symbol = 'BTC-WXG/USDT-WXG'
        type = 'limit'
        side = 'buy'

        price = amount * priceforone
        title = 'Кокупка BTC-WXG/USDT-WXG'
        deskription = 'Обмен USDT-WXG на BTC-WXG на криптобирже waves.exchange'

        yes = emoji.emojize(':check_mark_button:')
        result = f'{yes}Готово!\nОплатите что бы разместить ордер на покупку криптовалютной пары BTC-WXG/USDT-WXG\nПриблизительная стоимость $ {round(price, 2)}'
        price = int(price*100)
        price = types.LabeledPrice(label="Покупка BTC-WXG/USDT-WXG", amount=price)

        await bot.send_message(message.from_user.id, result, reply_markup=kb_client)
        await state.finish()
        await exchange.close()
    except:
        await bot.send_message(message.from_user.id, 'Вы ввели не число!\nНачните с начала!', reply_markup=kb_client)
        await state.finish()
        await exchange.close()


async def sell(message: types.Message):
    await message.answer('Введите сколько вы хотите купить USDT:')
    await Sell.amount.set()


async def get_amount2(message: types.Message, state: FSMContext):
    try:
        answer = float(message.text)
        await state.update_data(amount2=answer)
        await message.answer('Введите по какой цене вы хотите купить USDT:')
        await Sell.next()
    except:
        await bot.send_message(message.from_user.id, 'Вы ввели не число!\nНачните с начала!', reply_markup=kb_client)
        await state.finish()


async def get_price2(message: types.Message, state: FSMContext):
    global exchange
    global price
    global title
    global deskription

    try:
        data = await state.get_data()
        priceforone = float(message.text)
        amount = data.get('amount2')

        symbol = 'BTC-WXG/USDT-WXG'
        type = 'limit'
        side = 'sell'

        exchange2 = ccxt.kraken()
        r = await exchange2.fetch_ticker('BTC/USD')
        await exchange2.close()

        price = r['high'] * amount * (1/priceforone)
        title = 'Продажа BTC-WXG/USDT-WXG'
        deskription = 'Обмен BTC-WXG на USDT-WXG на криптобирже waves.exchange'

        yes = emoji.emojize(':check_mark_button:')
        result = f'{yes}Готово!\nОплатите что бы разместить ордер на продажу криптовалютной пары BTC-WXG/USDT-WXG\nПриблизительная стоимость $ {round(price, 2)}'
        price = int(price*100)
        price = types.LabeledPrice(label="Продажа BTC-WXG/USDT-WXG", amount=price)

        await bot.send_message(message.from_user.id, result, reply_markup=kb_client)
        await state.finish()
        await exchange.close()
    except:
        await bot.send_message(message.from_user.id, 'Вы ввели не число!\nНачните с начала!', reply_markup=kb_client)
        await state.finish()
        await exchange.close()


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(get_rate, commands=['Получить_текущий_курс_BTC/USDT'])
    dp.register_message_handler(buy, commands=['Вырбать_цену_для_покупки_пары_BTC/USDT'])
    dp.register_message_handler(sell, commands=['Выбрать_цену_для_продажи_пары_BTC/USDT'])
    dp.register_message_handler(get_amount, state=Buy.amount)
    dp.register_message_handler(get_price, state=Buy.price)
    dp.register_message_handler(get_amount2, state=Sell.amount)
    dp.register_message_handler(get_price2, state=Sell.price)
