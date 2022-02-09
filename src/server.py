import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from user import get, verify, User
from config import Config
from flask import Flask, config, jsonify, make_response, abort, request, g, url_for
from flask_login import LoginManager, login_required, current_user
from flask_httpauth import HTTPBasicAuth
from database import Database
from mav import movingAverages
from bestStocksDaily import bestStocksDaily
from monthlyBestStocks import monthlyBestPerformingStocks
import views
import numpy as np

def create_app():
    app = Flask(__name__, template_folder = '../templates', static_url_path = '/static')
    app.config.from_object(Config)
    app._static_folder = "../static"
    auth = HTTPBasicAuth()
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.config['db'] = Database()

    @login_manager.user_loader
    def load_user(user_id):
        return get(user_id)

    ## VIEWS
    app.add_url_rule("/", view_func=views.home_page, methods=["GET"])
    app.add_url_rule("/info", view_func=views.info_page, methods=["GET"])
    app.add_url_rule("/about", view_func=views.about_page, methods=["GET"])
    app.add_url_rule("/adviceToUser", view_func=views.adviceToUser_page, methods=["GET"])
    app.add_url_rule("/advice", view_func=views.advice_page, methods=["GET"])
    app.add_url_rule("/contact", view_func=views.contact_page, methods=["GET"])
    app.add_url_rule("/post", view_func=views.post_page, methods=["GET"])
    app.add_url_rule("/register", view_func=views.register_page, methods=["GET", "POST"])
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])

    '''
    #### USER AUTH

    @auth.verify_password
    def verify_password(username, password):
        print("verify")
        user = User.verify_auth_token(username)
        print("verify", user)
        if user is None:
            print("verify in")
            if verify(username, password):
                print("verifyin")
                g.user = get(username)
                return True
            else:
                print("verifyin false")
                return False
        else:
            g.user = user
            return True


    #### ERROR HANDLERS

    @auth.error_handler
    def unauthorized():
        return make_response(jsonify({'error': 'Unauthorized access'}), 403)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    '''
    #### ROUTES

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({'people': app.config['db'].get_index()})


    '''
    ## USER ENDPOINTS

    @app.route('/api/v1.0/user/register', methods = ['POST']) # register new user
    def new_user():
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            abort(404) # missing arguments
        user = app.config['db'].register(username, password)
        if user is None:
            abort(404)

        return jsonify({ 'username': user.username }), 201

    @app.route('/api/v1.0/user/token') # get auth token for user
    @auth.login_required
    def get_auth_token():
        token = g.user.generate_auth_token(600)
        return jsonify({ 'token': token, 'duration': 600 })

    '''
    ## STOCK VISUALIZATION ENDPOINTS

    @app.route('/api/v1.0/viewer/stocks/names', methods=['GET'])
    def get_stock_names():
        stocks = app.config['db'].get_stock_names()
        return jsonify({'response': stocks})

    @app.route('/api/v1.0/viewer/stocks/info', methods=['GET'])
    def get_stock_list():
        stocks = app.config['db'].get_stock_list()
        return jsonify({'response': stocks})

    @app.route('/api/v1.0/viewer/stocks/<stock_code>', methods=['GET'])
    def get_stock(stock_code):
        stock = app.config['db'].get_stock(stock_code)
        if stock is None:
            abort(404)
        return jsonify({'response': stock})

    ## Mav Results XU30 Stocks

    @app.route('/api/v1.0/viewer/mavResult/XU30', methods=['GET'])
    def getMavResultsXU30():
        XU30Lists = []
        XU30 = ['AKBNK', 'ARCLK', 'ASELS', 'BIMAS', 'DOHOL', 'EKGYO', 'EREGL', 'FROTO', 'GARAN', 'GUBRF',
            'HALKB', 'ISCTR', 'KCHOL', 'KOZAA', 'KOZAL', 'KRDMD', 'PETKM', 'PGSUS', 'SAHOL', 'SASA',
            'SISE', 'TAVHL', 'TCELL', 'THYAO', 'TKFEN', 'TOASO', 'TTKOM', 'TUPRS', 'VESTL', 'YKBNK']
        for item in XU30:
            returnList = movingAverages(item + '.csv')
            returnList.insert(0, item)
            XU30Lists.append(returnList)
        return jsonify({'stockList': XU30Lists})

    ## Mav Results Nasdaq Stocks

    @app.route('/api/v1.0/viewer/mavResult/Nasdaq', methods=['GET'])
    def getMavResultsStocksNasdaq():
        nasdaqList = []
        nasdaq = ['AAPL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'NVDA', 'GOOG', 'GOOGL', 'AVGO', 'ADBE',
                'NFLX', 'CSCO', 'COST', 'PEP', 'CMCSA', 'PYPL', 'INTC', 'QCOM', 'TXN', 'INTU',
                'AMD', 'HON', 'AMAT', 'TMUS', 'SBUX', 'AMGN', 'ISRG', 'CHTR', 'MU', 'ADP']
        for item in nasdaq:
            returnList = movingAverages(item + '.csv')
            returnList.insert(0, item)
            nasdaqList.append(returnList)
        return jsonify({'stockList': nasdaqList})

    ## Mav Results Nasdaq Cryptos

    @app.route('/api/v1.0/viewer/mavResult/Cryptos', methods=['GET'])
    def getMavResultsStocksCryptos():
        cryptosList = []
        cryptos = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'LUNAUSDT', 'DOTUSDT', 'AVAXUSDT', 'DOGEUSDT',
            'SHIBUSDT', 'MATICUSDT', 'EOSUSDT', 'LINKUSDT', 'UNIUSDT', 'ALGOUSDT', 'LTCUSDT', 'NEARUSDT', 'ATOMUSDT', 'TRXUSDT',
            'FTMUSDT', 'XLMUSDT', 'ICPUSDT', 'VETUSDT', 'FTTUSDT', 'MANAUSDT', 'HBARUSDT', 'FILUSDT', 'AXSUSDT', 'SANDUSDT']
        for item in cryptos:
            returnList = movingAverages(item + '.csv')
            returnList.insert(0, item)
            cryptosList.append(returnList)
        return jsonify({'stockList': cryptosList})


    ## Mav Results Nasdaq Pairs

    @app.route('/api/v1.0/viewer/mavResult/Pairs', methods=['GET'])
    def getMavResultsStocksPairs():
        pairsList = []
        pairs = ['EURUSD', 'USDJPY', 'GBPUSD', 'AUDUSD', 'USDCAD', 'USDCHF', 'GBPAUD',
                'EURGBP', 'GBPJPY', 'GBPZAR', 'USDZAR', 'EURAUD', 'EURCAD']
        for item in pairs:
            returnList = movingAverages(item + '.csv')
            returnList.insert(0, item)
            pairsList.append(returnList)
        return jsonify({'stockList': pairsList})


    ## STOCK MANAGEMENT ENDPOINTS

    @app.route('/api/v1.0/username', methods=['GET'])
    @login_required
    def get_username():
        return jsonify({'user': current_user.username})

    @app.route('/api/v1.0/manager/', methods=['GET'])
    @login_required
    def get_portfolio():
        stocks = app.config['db'].get_owned_stocks(current_user.username)
        return jsonify({'response': stocks})

    @app.route('/api/v1.0/manager/buy/<stock_code>:<int:amount>', methods=['POST'])
    @login_required
    def buy_stock(stock_code, amount):
        status = app.config['db'].buy_stock(current_user.username, stock_code, amount)
        return jsonify({'response': status})

    @app.route('/api/v1.0/manager/sell/<stock_code>:<int:amount>', methods=['POST'])
    @login_required
    def sell_stock(stock_code, amount):
        status = app.config['db'].sell_stock(current_user.username, stock_code, amount)
        return jsonify({'response': status})

    @app.route('/api/v1.0/manager/advice', methods=['GET'])
    def personalStockAdvice():
        XU30 = ['AKBNK', 'ARCLK', 'ASELS', 'BIMAS', 'DOHOL', 'EKGYO', 'EREGL', 'FROTO', 'GARAN', 'GUBRF',
                'HALKB', 'ISCTR', 'KCHOL', 'KOZAA', 'KOZAL', 'KRDMD', 'PETKM', 'PGSUS', 'SAHOL', 'SASA',
                'SISE', 'TAVHL', 'TCELL', 'THYAO', 'TKFEN', 'TOASO', 'TTKOM', 'TUPRS', 'VESTL', 'YKBNK']

        cryptos = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'LUNAUSDT', 'DOTUSDT', 'AVAXUSDT', 'DOGEUSDT',
                'SHIBUSDT', 'MATICUSDT', 'EOSUSDT', 'LINKUSDT', 'UNIUSDT', 'ALGOUSDT', 'LTCUSDT', 'NEARUSDT', 'ATOMUSDT', 'TRXUSDT',
                'FTMUSDT', 'XLMUSDT', 'ICPUSDT', 'VETUSDT', 'FTTUSDT', 'MANAUSDT', 'HBARUSDT', 'FILUSDT', 'AXSUSDT', 'SANDUSDT']

        nasdaq = ['AAPL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'NVDA', 'GOOG', 'GOOGL', 'AVGO', 'ADBE',
                'NFLX', 'CSCO', 'COST', 'PEP', 'CMCSA', 'PYPL', 'INTC', 'QCOM', 'TXN', 'INTU',
                'AMD', 'HON', 'AMAT', 'TMUS', 'SBUX', 'AMGN', 'ISRG', 'CHTR', 'MU', 'ADP']

        pairs = ['EURUSD', 'USDJPY', 'GBPUSD', 'AUDUSD', 'USDCAD', 'USDCHF', 'GBPAUD',
                'EURGBP', 'GBPJPY', 'GBPZAR', 'USDZAR', 'EURAUD', 'EURCAD']


        scoresArray = np.zeros(4)
        myList = app.config['db'].get_owned_stocks(current_user.username)['CODE']
        if len(myList) == 0:
            myList = ['BTCUSDT', 'ETHUSDT'] 
        for stock in myList:
            for item in XU30:
                if item == stock:
                    scoresArray[0] += 1
            for item in cryptos:
                if item == stock:
                    scoresArray[1] += 1
            for item in nasdaq:
                if item == stock:
                    scoresArray[2] += 1
            for item in pairs:
                if item == stock:
                    scoresArray[3] += 1
        maxIteration = max(scoresArray)
        index = None
        for i in range(4):
            if scoresArray[i] == maxIteration:
                index = i
                break
        if index == 0:
            cat = "XU30"
            mb, ma, mw = monthlyBestPerformingStocks(XU30, 1)
            bl = bestStocksDaily(XU30)
        elif index == 1:
            cat = "CRYPTO"
            mb, ma, mw = monthlyBestPerformingStocks(cryptos, 1)
            bl = bestStocksDaily(cryptos)
        elif index == 2:
            cat = "NASDAQ"
            mb, ma, mw = monthlyBestPerformingStocks(nasdaq, 1)
            bl = bestStocksDaily(nasdaq)
        elif index == 3:
            cat = "CURRENCY"
            mb, ma, mw = monthlyBestPerformingStocks(pairs, 1)
            bl = bestStocksDaily(pairs)
        return jsonify({'cat': cat, # cat - kullanıcı için seçilen kategori
                        'month_best': mb, # bunları almasını öneriyoruz, bir liste, her elemanı için stock[0] -> isim, stock[1] -> difference from mean (güvenilirlik değeri)
                        'month_avg': ma, #bunlar ortalama performans gösterecek
                        'month_worst': mw, # bunlardan uzak durmalı
                        'daily_best': bl, # önümüzdeki beş günde en çok kazanç getirebilecek hisseler, liste, her elemanı o güne ait en iyi hisse isimlerini içeren başka bir hisse
                        })
    return app

#### MAIN

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)