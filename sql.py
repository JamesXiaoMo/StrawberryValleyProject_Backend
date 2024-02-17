import time
from tqdm import tqdm
import pymysql
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def sql_ini():
    for i in tqdm(range(5), ascii=True, desc='重连次数'):
        try:
            print('正在尝试连接Mysql服务器...')
            sql = pymysql.connect(host=config.get('sql', 'host'),
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


def sql_add_data(data_owner: str, data_air_temp: int, data_air_hum: int, data_illum: int, data_battery: int,
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


def sql_add_device(device_uuid: str, device_type: str, device_owner: int, device_state: int):
    db = sql_ini()
    cursor = db.cursor()
    print('正在尝试新建设备...')
    try:
        cursor.execute("INSERT INTO device_table (device_uuid, device_type, device_owner, device_state) VALUES"
                       " (%s, %s, %s, %s)", (device_uuid, device_type, device_owner,device_state))
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

