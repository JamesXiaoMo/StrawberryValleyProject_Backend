import time
import pymysql
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


# 初始化数据库对象
def sql_ini():
    for i in range(5):
        try:
            print('正在尝试连接Mysql服务器...')
            sql = pymysql.connect(host=config.get('sql', 'server_ip'),
                                  port=int(config.get('sql', 'port')),
                                  user=config.get('sql', 'user'),
                                  password=config.get('sql', 'pwd'),
                                  db=config.get('sql', 'db')
                                  )
            print('成功连接到Mysql！')
            time.sleep(0.5)
            return sql
        except pymysql.err.OperationalError as e:
            print(f'无法连接到MySQL！错误原因是: {e}')
        time.sleep(5)
    raise Exception('连接到Mysql服务器失败！')


# 新增操作
def sql_add_user(user_id: str, user_pwd: str, user_email: str):
    import uuid
    new_uuid = uuid.uuid4()
    db = sql_ini()
    cursor = db.cursor()
    print('正在尝试创建用户...')
    try:
        cursor.execute("INSERT INTO user_table (user_uuid, user_id, user_pwd, user_email) VALUES (%s, %s, %s, %s)"
                       , (new_uuid, user_id, user_pwd, user_email))
        db.commit()
    except pymysql.err.ProgrammingError as e:
        print(f'创建用户失败！程序错误！原因是:{e}')
        db.rollback()
    except pymysql.err.DataError as e:
        print(f'创建用户失败！输入数据错误！原因是:{e}')
        db.rollback()
    else:
        print('创建用户成功！\n用户UUID:{uuid}\n用户名：{user_id}\n密码：{pwd}\n用户邮箱：{email}'.
              format(uuid=new_uuid, user_id=user_id, pwd=len(user_pwd) * '*', email=user_email))
    finally:
        db.close()


def sql_add_data(data_owner: int, data_air_temp: float, data_air_hum: float, data_illum: float, data_battery: int,
                 data_signal: int):
    db = sql_ini()
    cursor = db.cursor()
    print('正在尝试新建数据...')
    try:
        cursor.execute("INSERT INTO data_table (data_owner, data_air_temp, data_air_hum, data_illum, "
                       "data_battery, data_signal) VALUES (%s, %s, %s, %s, %s, %s)", (data_owner, data_air_temp,
                                                                                      data_air_hum, data_illum,
                                                                                      data_battery, data_signal))
        db.commit()
    except pymysql.err.ProgrammingError as e:
        print(f'新建数据失败！程序错误！原因是:{e}')
        db.rollback()
    except pymysql.err.DataError as e:
        print(f'新建数据失败！输入数据错误！原因是:{e}')
        db.rollback()
    else:
        print('数据新建成功')
    finally:
        db.close()


def sql_add_device(device_type: str, device_owner: int, device_state: int):
    import uuid
    new_uuid = uuid.uuid4()
    db = sql_ini()
    cursor = db.cursor()
    print('正在尝试新建设备...')
    try:
        cursor.execute("INSERT INTO device_table (device_uuid, device_type, device_owner, device_state) VALUES"
                       " (%s, %s, %s, %s)", (new_uuid, device_type, device_owner, device_state))
        db.commit()
    except pymysql.err.ProgrammingError as e:
        print(f'新建设备失败！程序错误！原因是:{e}')
        db.rollback()
    except pymysql.err.DataError as e:
        print(f'新建设备失败！输入数据错误！原因是:{e}')
        db.rollback()
    else:
        print('设备新建成功')
    finally:
        db.close()


def data_processing(raw_data: str):
    temp = float(raw_data.split(':')[0])
    hum = float(raw_data.split(':')[1])
    print('温度：' + str(temp))
    print('湿度：' + str(hum))
    sql_add_data(2, temp, hum, 0, 100, 100)
