import pymysql

host = '119.91.198.219'
user = 'youthrefuel'
password = 'dsq171007'
database = 'estrain'
port = 3306
db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)


class MysqlSetData(object):
    def __init__(self):
        self.db = db
        self.cursor = self.db.cursor()

    def set_user(self):
        user_account = "18897941661"
        user_password = "dsq171007"
        user_email = "2576210620@qq.com"
        UserAccount = "UserAccount"
        UserPassword = "UserPassword"
        UserEmail = "UserEmail"
        values = (user_account, user_password, user_email)
        where = "%s='%s'" % (UserAccount, values[0])
        self.user_ID = self.return_table_ID('user', where, values, *(UserAccount, UserPassword, UserEmail))
        print(self.user_ID)

    def set_station(self):
        from_station = "萍乡北"
        to_station = "醴陵东"
        date_station = "2023-05-12"
        table = "station"
        UserID = "UserID"
        FromStation = "FromStation"
        ToStation = "ToStation"
        DateStation = "DateStation"
        values = (self.user_ID, from_station, to_station, date_station)
        where = f"{UserID}=%s and {FromStation}='%s' and {ToStation}='%s' and {DateStation}='%s'" % values
        self.station_ID = self.return_table_ID(table, where, values, *(UserID, FromStation, ToStation, DateStation))
        print(self.station_ID)

    def set_train(self):
        train = 'G1342'
        state = 'static'
        table = 'train'
        values = (self.station_ID, train, state)
        StationID = "StationID"
        Train = "Train"
        State = "State"
        where = f"{StationID}=%s and {Train}='%s' and {State}='%s'" % values
        # self.train_ID = self.insert_into(table, values, *(StationID, Train, State))
        self.train_ID = self.return_table_ID(table, where, values, *(StationID, Train, State))
        print(self.train_ID)

    def set_user_name(self):
        user_name = '邓少青'
        table = "user_name"
        UserID = "UserID"
        TrainID = "TrainID"
        UserName = "UserName"
        values = (self.user_ID, self.train_ID, user_name)
        where = f"{UserID}=%s and {TrainID}=%s and {UserName}='%s'" % values
        self.user_name_ID = self.return_table_ID(table, where, values, *(UserID, TrainID, UserName))
        print(self.user_name_ID)

    def set_login_data(self):
        seat_type = '二等座'
        ticket_type = '成人票'
        seat = 'D'
        table = "login_data"
        UserNameID = "UserNameID"
        SeatType = "SeatType"
        TicketType = "TicketType"
        Seat = "Seat"
        values = (self.user_name_ID, seat_type, ticket_type, seat)
        where = f"{UserNameID}=%s and {SeatType}='%s' and {TicketType}='%s' and {Seat}='%s'" % values
        self.login_data_ID = self.return_table_ID(table, where, values, *(UserNameID, SeatType, TicketType, Seat))
        print(self.login_data_ID)

    def set_train_data(self, station_data, td_int):
        table = "train_data"
        TrainID = "TrainID"
        station_data = [["软卧票价81.5元剩3", "硬卧票价55元剩有", "硬座票价9元剩有"], [6, 8, 10]]
        station_data = str(station_data).replace("'", '"')
        StationData = "StationData"
        TdInt = "TdInt"
        values = (self.train_ID, station_data, td_int)
        where = f"{TrainID}=%s and {StationData}='%s' and {TdInt}=%s" % values
        self.train_data_ID = self.return_table_ID(table, where, values, *(TrainID, StationData, TdInt))
        print(self.train_data_ID)

    def return_table_ID(self, table, where, values, *args):
        sql = f"select {table}.ID from {table} where {where}"
        print(sql)
        select_bool = self.cursor.execute(sql)
        if select_bool:
            return self.cursor.fetchone()[0]
        else:
            return self.insert_into(table, values, *args)

    def insert_into(self, table, values, *args):
        args = str(args).replace("'", "")
        sql = f"insert into {table}{args} values {values};"
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.cursor.execute('select last_insert_id()')
        except:
            self.db.rollback()
            self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def mysql_close(self):
        self.cursor.close()
        self.db.close()


class MysqlUpdateDate(object):
    def __init__(self):
        self.db = db
        self.cursor = self.db.cursor()

    def update_train_state(self, ID, old_state, new_state):
        table = 'train'
        old_data = f"state='{old_state}'"
        new_data = f"state='{new_state}'"
        self.update(table, old_data, new_data, "ID=%s" % ID)

    def update(self, table, old_data, new_data, where):
        sql = "update %s set %s where %s and %s" % (table, new_data, where, old_data)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()


class MysqlGetData(object):
    def __init__(self):
        self.db = db
        self.cursor = self.db.cursor()

    def get_train_id(self, add_text=None, add_tables=None, add_where=None):
        return_text = "train.ID"
        return_text = self.add_text(return_text, add_text)
        tables = "user, station, train"
        tables = self.add_text(tables, add_tables)
        where = "station.UserID=user.ID and train.StationID=station.ID"
        where = self.add_text(where, add_where)
        return self.get_select_data(return_text, tables, where)

    @staticmethod
    def add_text(text, add_text=None, add_where=None):
        if add_where:
            return text + " and %s" % add_where
        if add_text:
            return text + "," + add_text
        else:
            return text

    def get_train_id_all_data(self, train_id):
        train_id = f"train.ID={train_id}"
        return self.get_all_data(f"{train_id}")[0]

    def get_train(self, ID, *args):
        tables = "train"
        return_text = "Train"
        if args:
            return_text = "%s" % args
        where = "train.ID=%s" % ID
        return self.get_select_data(return_text, tables, where)

    def get_station(self, ID):
        tables = "station"
        return_text = "FromStation, ToStation, DateStation"
        where = "station.ID=%s" % ID
        return self.get_select_data(return_text, tables, where)[0]

    def get_user_name(self, ID):
        tables = "user_name, login_data"
        return_text = "TicketType, SeatType, UserName"
        where = "user_name.ID=login_data.UserNameID and user_name.ID=%s" % ID
        return self.get_select_data(return_text, tables, where)[0]

    def get_user(self, ID):
        tables = "user"
        return_text = "UserAccount, UserPassword, UserEmail"
        where = "user.ID=%s" % ID
        return self.get_select_data(return_text, tables, where)[0]

    def get_seat(self, ID):
        tables = "login_data"
        return_text = "Seat"
        where = "login_data.ID=%s" % ID
        return self.get_select_data(return_text, tables, where)[0]

    def get_all_data(self, *args):
        all_text = "train.ID"
        all_from = "user_name, user, login_data, train, station"
        all_where = "station.UserID=user.ID and train.StationID=station.ID and train.ID=user_name.TrainID and user_name.ID=login_data.UserNameID"
        if len(args):
            all_where = all_where + " and %s" % args[0]
        all_data = self.get_select_data(all_text, all_from, all_where)
        return all_data

    def get_select_data(self, return_text, tables, where):
        sql = f"select {return_text} from {tables} where {where}"
        print(sql)
        self.cursor.execute(sql)
        text = self.cursor.fetchall()
        return text


class MysqlDeleteData(object):
    def __init__(self):
        self.db = db
        self.cursor = self.db.cursor()

    def delete_user(self):
        table = 'user'
        where = "UserAccount='18897941661' and UserPassword='dsq171007' and UserEmail='2576210620@qq.com';"
        self.delete_data(table, where)

    def delete_login_data(self, user_name):
        table = 'login_data'
        where = f"UserName='{user_name}' and SeatType='二等座' and TicketType='成人票' and Seat='D';"
        self.delete_data(table, where)

    def delete_user_name(self):
        table = 'user_name'
        where = f"UserAccount='18897941661' and UserName='邓少青';"
        self.delete_data(table, where)

    def delete_train(self):
        table = 'train'
        where = f"ID=2 and Train='G645' and State='static';"
        self.delete_data(table, where)

    def delete_data(self, table, where):
        sql = f"delete from {table} where {where}"
        # print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()


if __name__ == '__main__':
    set_mysql = MysqlSetData()
    set_mysql.set_user()
    set_mysql.set_station()
    set_mysql.set_train()
    set_mysql.set_user_name()
    set_mysql.set_login_data()
    set_mysql.set_train_data(None, 10)
    # set_mysql.mysql_close()

    get_mysql = MysqlGetData()
    print(get_mysql.get_all_data())
    print(get_mysql.get_user_name(14))
    print(get_mysql.get_train(1, "State"))
    print(get_mysql.get_seat(26))

    delete_mysql = MysqlDeleteData()
    # delete_mysql.delete_login_data('邓少青')
    # delete_mysql.delete_user()

    update_mysql = MysqlUpdateDate()
    # update_mysql.update_train_state('active', 'static')
