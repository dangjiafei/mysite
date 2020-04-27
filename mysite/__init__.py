import pymysql

pymysql.install_as_MySQLdb()  # 告诉django利用pymysql模块代替默认的MySQLdb去连接MySQL数据库
