import json

import pymysql as pymysql
from flask import Flask, request

import settings

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/register', methods=['POST'])
def user_register():
    """
    用户注册
    :return:
    """
    data = request.data
    # 字符串转 json
    j_data = json.loads(data)

    user_name = j_data["user_name"]
    password = j_data["password"]

    # 查询数据该信息是否存在


    connection = pymysql.connect(host=settings.DB_HOST,
                                 user=settings.DB_USER,
                                 password=settings.DB_PASSWORD,
                                 db=settings.DB_NAME,
                                 charset=settings.DB_CHARSET,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "SELECT * FROM  u_user WHERE user_name =%s"
            cursor.execute(sql, (user_name))
        result = cursor.fetchone()
        print("查询结果", result)

        # 存在
        if result:
            return {"message": "用户存在！无法注册"}
        # 不存在
        else:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `u_user` (`user_name`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, (user_name, password))
                connection.commit()
            return {"message": "注册成功！"}
    finally:
        connection.close()


if __name__ == '__main__':
    app.run()
