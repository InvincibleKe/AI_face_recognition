import numpy as np
import pymysql
import traceback
# 数据清理
def data_clean():
    db = pymysql.connect(host="192.168.10.41", port=3306, user="root", passwd="emsoft", database="business", charset="utf8")
    cursor = db.cursor()
    del_faceFeature_sql = '''DELETE FROM face_feature;'''
    del_uidFid_sql = '''DELETE FROM uid_fid;'''
    del_userInfo_sql = '''DELETE FROM user_info;'''
    try:
        cursor.execute(del_faceFeature_sql)
        db.commit()
    except:
        print('fail to delete face_feature')
        traceback.print_exc()
        db.rollback()
        cursor.close()
        db.close()
        return 1
    try:
        cursor.execute(del_uidFid_sql)
        db.commit()
    except:
        print('fail to delete uid_fid')
        traceback.print_exc()
        db.rollback()
        cursor.close()
        db.close()
        return 2
    try:
        cursor.execute(del_userInfo_sql)
        db.commit()
    except:
        print('fail to delete user_info')
        traceback.print_exc()
        db.rollback()
        cursor.close()
        db.close()
        return 3
    cursor.close()
    db.close()
    return 0

# 查询人脸特征
def get_faceFeatures():
    print('get_faceFeatures connect before')
    db = pymysql.connect(host="192.168.10.41", port=3306, user="root", passwd="emsoft", database="business", charset="utf8")
    cursor = db.cursor()
    sql = '''SELECT * FROM face_feature;'''
    print('get_faceFeatures execute before')
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print('rollback')
        traceback.print_exc()
    finally:
        cursor.close()
        db.close()
        print('get_faceFeatures execute after')
        return results

# 从用户表根据uid获取memo值
def get_faceInfo(uid):
    print('get_faceInfo before')
    db_business = pymysql.connect(host="192.168.10.41", port=3306, user="root", passwd="emsoft", database="business", charset="utf8")
    cursor = db_business.cursor()
    print(uid)
    sql = '''SELECT memo FROM user_info WHERE uid='%s';'''%uid
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            memo = results[0][0]
        else: memo = 1
    except:
        print('rollback')
        traceback.print_exc()
    finally:
        cursor.close()
        db_business.close()
        return memo
# 根据fid查询业务库表uid_fid
def getUid(fid):
    try:
        db_business = pymysql.connect(host="192.168.10.41", port=3306, user="root", passwd="emsoft", database="business", charset="utf8")
    except:
        traceback.print_exc()
        print("Could not connect to MySQL server.")
    cursor = db_business.cursor()
    sql = '''SELECT uid FROM uid_fid WHERE fid='%s';'''%fid
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            uid = results[0][0]
        else: uid = 1
    except:
        traceback.print_exc()
    finally:
        cursor.close()
        db_business.close()
        return uid

# 往face_feature表插入数据
def insert_face_feature(fid, feature):
    db_ai = pymysql.connect(host="192.168.10.41", port=3306, user="root", passwd="emsoft", database="business")
    cursor_ai = db_ai.cursor()
    print(feature)

    try:
        cursor_ai.execute('INSERT INTO face_feature(fid, feature) VALUES(%s, %s)', ([fid, feature]))
        db_ai.commit()
    except:
        print('rollback')
        traceback.print_exc()
        db_ai.rollback()
    finally:
        cursor_ai.close()
        db_ai.close()

# 往user_info表插入数据
def insert_user_info(uid, memo):
    try:
        db_business = pymysql.connect(host="192.168.10.41", port=3306, user="root", passwd="emsoft", database="business", charset="utf8")
    except:
        print("Could not connect to MySQL server.")
    cursor_business = db_business.cursor()
    sql_business = '''INSERT INTO user_info(uid, memo)
                 VALUES('%s', '%s')''' % (uid, memo)
    try:
        cursor_business.execute(sql_business)
        db_business.commit()
    except:
        print('rollback')
        traceback.print_exc()
        db_business.rollback()
    finally:
        cursor_business.close()
        db_business.close()

# 往uid_fid表插入数据
def insert_uid_fid(uid, fid):
    try:
        db_business = pymysql.connect(host="192.168.10.41", port=3306, user="root", passwd="emsoft", database="business", charset="utf8")
    except:
        print("Could not connect to MySQL server.")
    cursor_business = db_business.cursor()
    sql_business = '''INSERT INTO uid_fid(uid, fid)
                 VALUES('%s', '%s')''' % (uid, fid)
    try:
        cursor_business.execute(sql_business)
        db_business.commit()
    except:
        print('rollback')
        traceback.print_exc()
        db_business.rollback()
    finally:
        cursor_business.close()
        db_business.close()

def readData():
    db = pymysql.connect(host="192.168.10.41", port=3306, user="root", passwd="emsoft", database="business", charset="utf8")
    # 连接数据库对象

    cur = db.cursor()
    # 游标对象

    sql = "select * from face_data"
    # 定义好sql语句，%s是字符串的占位符

    try:
        cur.execute(sql)
        # 执行sql语句
        results = cur.fetchall()
        # 获取所有结果集
        for row in results:
            numArr = np.fromstring(string=row[1], dtype=int)
            # 将读取到的字节流转化为ndarray数组
            shape = tuple(eval(row[2]))
            # 将读取到的shape转换为元组的格式，这里的eval（），由于我们元组里面的数据是int的所以，这里eval（）的作用就是把本该是数字的转化回来
            numArr.shape = shape
            # 设置维度，设置的数值为元组
            print(numArr)
        db.commit()
        # 提交到数据库中
    except Exception as e:
        # 捕获异常
        raise e
    finally:
        db.close()  # 关闭连接

