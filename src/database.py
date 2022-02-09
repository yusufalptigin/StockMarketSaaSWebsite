from user import User
import psycopg2 as dbapi2
import os

class Database:
    def __init__(self):
        self.conn = dbapi2.connect(os.environ['DATABASE_URL'], sslmode='require')
        self.users = {
            'test': 'test'
        }

        self.stocks = {
            'DARDL.IS': 3.0400,
            'MGROS.IS': 42.74,
            'KOZAL.IS': 124.70,
            'ASELS.IS': 23.02,
            'PNSUT.IS': 18.22
        }

        self.ownership = {
            'test': {
                'DARDL.IS': 5,
                'KOZAL.IS': 3,
                }
        }
        pass


    # VISUALIZATION
    
    def get_stock_names(self):
        with self.conn.cursor() as curr:
            curr.execute("SELECT STOCKCODE\
                          FROM STOCK;")
            rows = curr.fetchall()
            return list(rows)

    def get_stock_list(self):
        with self.conn.cursor() as curr:
            curr.execute("SELECT STOCKCODE, STOCKNAME, CURRPRICE, CHANGE\
                          FROM STOCK;")
            rows = curr.fetchall()
            result_dict = {
                'CODE': list(),
                'NAME': list(),
                'PRICE': list(),
                'CHANGE': list(),
            }
            for row in rows:
                result_dict['CODE'].append(row[0])
                result_dict['NAME'].append(row[1])
                result_dict['PRICE'].append(row[2])
                result_dict['CHANGE'].append(row[3])
            return result_dict

    def get_stock(self, stock_id):
        with self.conn.cursor() as curr:
            curr.execute("SELECT STOCKCODE, STOCKNAME, CURRPRICE, CHANGE\
                          FROM STOCK where STOCKCODE=%s;", (stock_id,))
            row = curr.fetchone()
            result_dict = {
                'CODE': row[0],
                'NAME': row[1],
                'PRICE': row[2],
                'CHANGE': row[3],
            }
            return result_dict

    # MANAGER

    def get_owned_stocks(self, user_id):
        with self.conn.cursor() as curr:
            curr.execute("SELECT STOCKCODE, QUANTITY, COST\
                          FROM OWNERSHIP WHERE USERNAME=%s ORDER BY STOCKCODE", (user_id,))
            rows = curr.fetchall()
            if len(rows) == 0:
                return {
                'CODE': None,
                'QUANTITY': None,
                'PROFIT': None,
                }

            stocks = tuple([row[0] for row in rows])
            curr.execute("SELECT CURRPRICE FROM STOCK WHERE STOCKCODE IN %s ORDER BY STOCKCODE", (stocks,))
            curr_prices = curr.fetchall()

            result_dict = {
                'CODE': stocks,
                'QUANTITY': [int(row[1]) for row in rows],
                'PROFIT': [int(row[1])*(float(row[2]) - float(price[0])) for row, price in zip(rows, curr_prices)],
            }
            return result_dict

    def buy_stock(self, user_id, stock_id, amount):
        with self.conn.cursor() as curr:
            curr.execute("SELECT TRANSACTION_ID, QUANTITY, COST\
                          FROM OWNERSHIP WHERE USERNAME=%s AND STOCKCODE=%s", (user_id, stock_id,))
            row = curr.fetchone()
            if row is None:
                curr.execute("SELECT CURRPRICE FROM STOCK WHERE STOCKCODE=%s", (stock_id,))
                cost = curr.fetchone()[0]
                curr.execute("INSERT INTO ownership (USERNAME, STOCKCODE, QUANTITY, COST)\
                              VALUES (%s, %s, %s, %s)", (user_id, stock_id, amount, cost))
                self.conn.commit()
            else:
                id, quantity, curr_cost = row
                curr.execute("SELECT CURRPRICE FROM STOCK WHERE STOCKCODE=%s", (stock_id,))
                cost = curr.fetchone()[0]
                curr.execute("UPDATE ownership \
                              SET quantity=%s, \
                                  cost=%s      \
                              WHERE transaction_id=%s", (quantity + amount, (quantity*curr_cost + amount*cost)/(quantity + amount), id))
                self.conn.commit()
            return True

    def sell_stock(self, user_id, stock_id, amount):
        with self.conn.cursor() as curr:
            curr.execute("SELECT TRANSACTION_ID, QUANTITY, COST\
                          FROM OWNERSHIP WHERE USERNAME=%s AND STOCKCODE=%s", (user_id, stock_id,))
            row = curr.fetchone()
            if row is None:
                return {'error': "Stock not in portfolio"}
            else:
                id, quantity, curr_cost = row
                if quantity < amount:
                    return {'error': "Stock amount smaller than amount to sell"}
                curr.execute("SELECT CURRPRICE FROM STOCK WHERE STOCKCODE=%s", (stock_id,))
                cost = curr.fetchone()[0]
                if quantity - amount > 0:
                    curr.execute("UPDATE ownership \
                                SET quantity=%s, \
                                    cost=%s      \
                                WHERE transaction_id=%s", (quantity - amount, (quantity*curr_cost - amount*cost)/(quantity - amount), id))
                else:
                    curr.execute("DELETE FROM ownership \
                                WHERE transaction_id=%s", (id, ))
                self.conn.commit()
            return True
    # USER

    def get_user(self, user_id):
        with self.conn.cursor() as curr:
            curr.execute("SELECT username, password FROM USERS WHERE username=%s;", (user_id,))
            row = curr.fetchone()
            if row is not None:
                return User(username=row[0],
                            password=row[1])
            else:
                return None
    
    def register(self, username, password):
        if self.get_user(username) is None:
            with self.conn.cursor() as curr:
                curr.execute("INSERT INTO users (username, password) VALUES (%s,%s) RETURNING username;",
                             (username, password))
                if username == curr.fetchone()[0]:
                    self.conn.commit()
                    return User(username, password)
                else:
                    return None
        else:
            return None
    
    def verify_user(self, username, password):
        with self.conn.cursor() as curr:
            curr.execute("SELECT password FROM USERS WHERE username=%s;", (username,))
            row = curr.fetchone()
            if row is not None:
                if row[0] == password:
                    return True
        return False
