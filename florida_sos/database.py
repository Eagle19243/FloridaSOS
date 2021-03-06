import pymysql


class Database:
    def __init__(self, settings):
        host = settings.get('MYSQL')['host']
        user = settings.get('MYSQL')['user']
        password = settings.get('MYSQL')['password']
        db = settings.get('MYSQL')['db']

        self.con = pymysql.connect(host=host, user=user, password=password,
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        self.cur.execute('CREATE DATABASE IF NOT EXISTS %s' % db)
        self.con = pymysql.connect(host=host, user=user, password=password, db=db,
                                   autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS `corps` ('
                         '`id` int(11) NOT NULL auto_increment, '
                         '`corp_name` VARCHAR(200), '
                         '`fei_ein_number` VARCHAR(20), '
                         '`date_filed` VARCHAR(20), '
                         '`status` VARCHAR(100), '
                         '`last_event` VARCHAR(300), '
                         '`principal_addr` VARCHAR(300), '
                         '`mailing_addr` VARCHAR(300), '
                         '`registered_agent_addr` VARCHAR(500), '
                         '`officer_addr` VARCHAR(2000), '
                         '`url` VARCHAR(400), '
                         'PRIMARY KEY (`id`))')
        self.cur.execute('CREATE TABLE IF NOT EXISTS `logs` ('
                         '`id` int(11) NOT NULL auto_increment, '
                         '`url` VARCHAR(400), '
                         'PRIMARY KEY (`id`))')

    def remove_data(self):
        self.cur.execute('TRUNCATE TABLE `corps`')
        return

    def get_data(self):
        self.cur.execute('SELECT * FROM `corps`')
        result = self.cur.fetchall()
        return result

    def get_last_url(self):
        self.cur.execute('SELECT * FROM `logs` ORDER BY `id` DESC LIMIT 1')
        result = self.cur.fetchone()
        return result['url'] if result else None

    def save_log(self, url):
        last_url = self.get_last_url()

        if last_url:
            query = """UPDATE `logs` SET `url` = %s WHERE `url` = %s"""
            self.cur.execute(query, (url, last_url))
        else:
            query = """INSERT INTO `logs` (`url`) VALUES (%s)"""
            self.cur.execute(query, url)

        return

    def remove_log(self):
        self.cur.execute('TRUNCATE TABLE `logs`')
        return

    def save_data(self,
                  corp_name,
                  fei_ein_number,
                  date_filed,
                  status,
                  last_event,
                  principal_addr,
                  mailing_addr,
                  registered_agent_addr,
                  officer_addr,
                  url):
        query = """INSERT INTO `corps` (`corp_name`, 
                `fei_ein_number`, 
                `date_filed`, 
                `status`, 
                `last_event`, 
                `principal_addr`, 
                `mailing_addr`, 
                `registered_agent_addr`, 
                `officer_addr`, 
                `url`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cur.execute(query, (corp_name,
                                 fei_ein_number,
                                 date_filed, status,
                                 last_event,
                                 principal_addr,
                                 mailing_addr,
                                 registered_agent_addr,
                                 officer_addr,
                                 url))

        return
