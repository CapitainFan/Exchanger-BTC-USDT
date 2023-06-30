import emoji
import ccxt.async_support as ccxt
from aiogram import types, Dispatcher
from bot import dp, bot, TEXT
from keyboard import kb_client, button3, button4
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


exchange = ccxt.wavesexchange()
registerd = False


class Registration(StatesGroup):
    apikey = State()
    secret = State()


async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, TEXT, reply_markup=kb_client)


async def register(message: types.Message):
    global registerd
    if registerd:
        await bot.send_message(message.from_user.id, 'Вы уже вошли в аккаунт')
        return

    await message.answer('Введите Публичный ключ :')
    await Registration.apikey.set()


async def get_apykey(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await message.answer('Введите Приватный ключ :')
    await Registration.next()


async def get_secret(message: types.Message, state: FSMContext):
    data = await state.get_data()
    SECRET = message.text
    APIKEY = data.get('answer1')

    global registerd
    global exchange

    try:
        exchange = ccxt.wavesexchange({
            'enableRateLimit': True,
            'apiKey': APIKEY,
            'secret': SECRET,
        })
        await exchange.fetch_my_trades()
        yes = emoji.emojize(':check_mark_button:')
        result = f'Вход в аккаунт криптобирже waves.exchange удался {yes}'
        kb_client.add(button3).add(button4)
        registerd = True
    except:
        no = emoji.emojize(':cross_mark:')
        result = f'Вход в аккаунт криптобирже waves.exchange не удался {no} :\nДанные не подходят или аккаунта не существует\nили произошла ошибка в работе бота'

    await bot.send_message(message.from_user.id, result, reply_markup=kb_client)
    await state.finish()
    await exchange.close()


async def get_rate(message: types.Message):
    orderbook = await exchange.fetch_order_book('BTC-WXG/USDT-WXG')
    bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
    spread = (ask - bid) if (bid and ask) else None
    price = f'цена продажи: {bid}, цена покупки: {ask}, разброс: {spread}'

    stonks = emoji.emojize(':chart_increasing:')
    arrow = emoji.emojize(':right_arrow:')
    result = (f'Текущий курс {stonks}\nBTC-WXG/USDT-WXG\nна криптобирже waves.exchange {arrow}\n{price}')

    await bot.send_message(message.from_user.id, result)
    await exchange.close()


async def buy(message: types.Message):
    global registerd
    if not registerd:
        await bot.send_message(message.from_user.id, 'Вы не вошли в аккаунт')
        return

    markets = (await exchange.load_markets())['BTC-WXG/USDT-WXG']
    high = int(markets['info']['24h_high'])
    low = int(markets['info']['24h_low'])

    symbol = 'BTC-WXG/USDT-WXG'
    type = 'market'
    side = 'buy'
    amount = 1
    price = int(low + ((high - low)/2))
    params={
        'triggerPrice': price,
    }
    try:
        request = await exchange.create_order(symbol, type, side, amount, price, params)
        yes = emoji.emojize(':check_mark_button:')
        result = f'Ваш ордер был успешно отправлен {yes}'
    except:
        no = emoji.emojize(':cross_mark:')
        result = f'Покупка валютной пары BTC-WXG/USDT-WXG не удалась {no} :\nНедостаточно средств на балансе\nили произошла ошибка в работе бота'

    await bot.send_message(message.from_user.id, result)
    await exchange.close()


async def sell(message: types.Message):
    global registerd
    if not registerd:
        await bot.send_message(message.from_user.id, 'Вы не вошли в аккаунт')
        return

    markets = (await exchange.load_markets())['BTC-WXG/USDT-WXG']
    high = int(markets['info']['24h_high'])
    low = int(markets['info']['24h_low'])

    symbol = 'BTC-WXG/USDT-WXG'
    type = 'market'
    side = 'sell'
    amount = 1
    price = int(low + ((high - low)/2))
    params={
        'triggerPrice': price,
    }

    try:
        request = await exchange.create_order(symbol, type, side, amount, price, params)
        yes = emoji.emojize(':check_mark_button:')
        result = f'Ваш ордер был успешно отправлен {yes}'
    except:
        no = emoji.emojize(':cross_mark:')
        result = f'Продажа валютной пары BTC-WXG/USDT-WXG не удалась {no} :\nНедостаточно средств на балансе\nили произошла ошибка в работе бота'

    await bot.send_message(message.from_user.id, result)
    await exchange.close()


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(get_rate, commands=['Получить_текущий_курс_BTC/USDT'])
    dp.register_message_handler(buy, commands=['Купить_пару_BTC/USDT'])
    dp.register_message_handler(sell, commands=['Продать_пару_BTC/USDT'])
    dp.register_message_handler(register, commands=['Войти_в_аккаунт'])
    dp.register_message_handler(get_apykey, state=Registration.apikey)
    dp.register_message_handler(get_secret, state=Registration.secret)
