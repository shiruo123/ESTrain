import pymysql


class Mysql(object):
    def __init__(self):
        host = '119.91.198.219'
        user = 'youthrefuel'
        password = 'dsq171007'
        database = 'estrain'
        port = 3306
        self.db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
        self.cursor = self.db.cursor()


class MysqlSetData(Mysql):
    def __init__(self):
        super().__init__()

    def set_user(self, user_account, user_password, user_email):
        UserAccount = "UserAccount"
        UserPassword = "UserPassword"
        UserEmail = "UserEmail"
        values = (user_account, user_password, user_email)
        where = "%s='%s'" % (UserAccount, values[0])
        self.user_ID = self.return_table_ID('user', where, values, *(UserAccount, UserPassword, UserEmail))
        print(self.user_ID)

    def set_station(self, from_station, to_station, date_station):
        table = "station"
        UserID = "UserID"
        FromStation = "FromStation"
        ToStation = "ToStation"
        DateStation = "DateStation"
        values = (self.user_ID, from_station, to_station, date_station)
        where = f"{UserID}=%s and {FromStation}='%s' and {ToStation}='%s' and {DateStation}='%s'" % values
        self.station_ID = self.return_table_ID(table, where, values, *(UserID, FromStation, ToStation, DateStation))
        print(self.station_ID)

    def set_train(self, train):
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
        return self.train_ID

    def set_user_name(self, user_name):
        table = "user_name"
        UserID = "UserID"
        TrainID = "TrainID"
        UserName = "UserName"
        values = (self.user_ID, self.train_ID, user_name)
        where = f"{UserID}=%s and {TrainID}=%s and {UserName}='%s'" % values
        self.user_name_ID = self.return_table_ID(table, where, values, *(UserID, TrainID, UserName))
        print(self.user_name_ID)

    def set_login_data(self, seat_type, ticket_type, seat):
        table = "login_data"
        UserNameID = "UserNameID"
        SeatType = "SeatType"
        TicketType = "TicketType"
        Seat = "Seat"
        values = (self.user_name_ID, seat_type, ticket_type, seat)
        where = f"{UserNameID}=%s and {SeatType}='%s' and {TicketType}='%s' and {Seat}='%s'" % values
        self.login_data_ID = self.return_table_ID(table, where, values, *(UserNameID, SeatType, TicketType, Seat))
        print(self.login_data_ID)

    def set_train_data(self, train_id, station_data, td_int):
        table = "train_data"
        TrainID = "TrainID"
        station_data = str(station_data).replace("'", '"')
        StationData = "StationData"
        TdInt = "TdInt"
        values = (train_id, station_data, td_int)
        print(values)
        where = f"{TrainID}=%s" % (train_id, )
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


class MysqlUpdateDate(Mysql):
    def __init__(self):
        super(MysqlUpdateDate, self).__init__()

    def update_train_state(self, ID, new_state):
        table = 'train'
        new_data = f"state='{new_state}'"
        self.update(table, new_data, "ID=%s" % ID)

    def update_train_data_station_data(self, ID, new_text):
        table = "train_data"
        station_data = str(new_text).replace("'", '"')
        new_data = f"StationData='%s'" % station_data
        self.update(table, new_data, "ID=%s" % ID)

    def update_train_error(self, ID, error_text):
        table = "train"
        new_data = f"Error='%s'" % error_text
        self.update(table, new_data, "ID=%s" % ID)

    def update(self, table, new_data, where):
        sql = "update %s set %s where %s" % (table, new_data, where)
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()


class MysqlGetData(Mysql):
    def __init__(self):
        super(MysqlGetData, self).__init__()

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
        return self.get_select_data(return_text, tables, where)[0]

    def get_station(self, ID):
        tables = "station"
        return_text = "FromStation, ToStation, DateStation"
        where = "station.ID=%s" % ID
        return self.get_select_data(return_text, tables, where)[0]

    def get_user_name(self, ID, *args):
        tables = "user_name, login_data"
        return_text = "TicketType, SeatType, UserName"
        where = "user_name.ID=login_data.UserNameID and user_name.ID=%s" % ID
        if args:
            return_text = "%s, " % args + return_text
        return self.get_select_data(return_text, tables, where)[0]

    def get_user_name_add_sent(self, train_ID, *args):
        tables = "user_name, login_data"
        return_text = "Seat, TicketType, SeatType, UserName"
        where = "user_name.ID=login_data.UserNameID and user_name.TrainID=%s" % train_ID
        if args:
            where = where + " and %s" % args
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

    def get_train_data(self, ID):
        tables = "train_data"
        return_text = "StationData, TdInt"
        where = "train_data.TrainID=%s" % ID
        return self.get_select_data(return_text, tables, where)[0]

    def get_datas(self):
        return_text = "UserAccount, UserPassword, UserEmail, Train, StationData, TdInt, UserName, SeatType, TicketType, Seat, State, Error"
        tables = "user, station, train, train_data, user_name, login_data"
        where = "user.ID=station.UserID and Station.ID = train.StationID and train.ID=train_data.TrainID and train.ID " \
                "= user_name.TrainID  and user_name.ID=login_data.UserNameID "
        return self.get_select_data(return_text, tables, where)

    def get_user_station_id(self, train_id):
        return_text = "user.ID, station.ID"
        tables = "user, station, train"
        where = "train.ID=%s" % train_id
        return self.get_select_data(return_text, tables, where)

    def get_username_logindata_id(self, train_id):
        return_text = "user_name.ID, login_data.ID"
        tables = "train, user_name, login_data"
        where = "train.ID=user_name.TrainID and user_name.ID=login_data.UserNameID and train.ID=%s" % train_id
        return self.get_select_data(return_text, tables, where)

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


class MysqlDeleteData(Mysql):
    def __init__(self):
        super(MysqlDeleteData, self).__init__()

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
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()


if __name__ == '__main__':
    set_mysql = MysqlSetData()
    # set_mysql.set_user()
    # set_mysql.set_station()
    # set_mysql.set_train()
    # set_mysql.set_user_name()
    # set_mysql.set_login_data()
    # set_mysql.set_train_data(None, 8)
    # set_mysql.mysql_close()

    get_mysql = MysqlGetData()
    # print(get_mysql.get_all_data())
    # print(get_mysql.get_user_name(14))
    # print(get_mysql.get_train(1, "State"))
    # print(get_mysql.get_seat(26))
    # print(get_mysql.get_train_data(4))
    for data in get_mysql.get_datas():
        print(data)

    delete_mysql = MysqlDeleteData()
    # delete_mysql.delete_user()
    # delete_mysql.delete_user()

    update_mysql = MysqlUpdateDate()
    # update_mysql.update_train_state('active', 'static')
    # update_mysql.update_train_error(36, "爬取错误")
