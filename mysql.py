import pymysql
import datetime

# 数据库连接配置
DB_CONFIG = {
    'host': 'ovocc.cc',
    'user': 'DoubleQ',
    'password': 'KRRHtRimRySZZiWf',
    'database': 'doubleq'
}


def get_connection():
    """
    创建并返回数据库连接对象
    """
    return pymysql.connect(**DB_CONFIG)


# 管理员登录
def check_manager_credentials(account, password):
    """
    验证管理员凭据
    参数:
        - account: 登录账号
        - password: 登录密码
    返回值:
        True，如果凭据验证通过；False，如果凭据验证失败
    """
    connection = pymysql.connect(**DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM store_managers WHERE login_account = %s AND login_password = %s'
            cursor.execute(sql, (account, password))
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False
    finally:
        connection.close()


# 客户登录
def check_customer_credentials(account, password):
    """
    验证客户凭据
    参数:
        - account: 登录账号
        - password: 登录密码
    返回值:
        True，如果凭据验证通过；False，如果凭据验证失败
    """
    connection = pymysql.connect(**DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM customers WHERE account = %s AND password = %s'
            cursor.execute(sql, (account, password))
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False
    finally:
        connection.close()


# 客户注册
def insert_customer(name, account, password, purchase_count, total_amount):
    """
    将客户数据插入到数据库
    参数:
        - name: 客户姓名
        - account: 注册账号
        - password: 注册密码
        - purchase_count: 购买次数
        - total_amount: 总金额
    """
    connection = pymysql.connect(**DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO customers (name, account, password, purchase_count, total_amount) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (name, account, password, purchase_count, total_amount))
        connection.commit()
    finally:
        connection.close()


# 修改客户信息
def update_customer_in_db(name, account, password):
    """
    更新客户信息
    参数:
        - name: 客户姓名
        - account: 客户账号
        - password: 客户密码
    返回值:
        - 成功更新返回 True，否则返回 False
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = 'UPDATE customers SET name=%s, password=%s WHERE account=%s'
            values = (name, password, account)
            cursor.execute(sql, values)
            connection.commit()

            # 检查是否更新成功
            if cursor.rowcount > 0:
                return True
            else:
                return False

    finally:
        connection.close()


# 获取客户所有信息
def get_customer_all():
    """
    获取所有客户的数据
    返回值:
        包含客户数据的列表
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM customers'
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    finally:
        connection.close()


# 更新客户的消费次数
def update_purchase_and_review(account, purchase_count, customer_review, employee_id):
    """
    更新指定账号的客户的消费次数、评价和服务员工ID
    参数:
        account: 客户账号
        purchase_count: 更新后的购买次数
        customer_review: 客户评价
        employee_id: 服务员工ID
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # 开始事务
            connection.begin()

            # 更新customer_orders表中的customer_review和employee_id字段
            sql = 'UPDATE customer_orders SET customer_review = %s, employee_id = %s WHERE customer_id = (SELECT id FROM customers WHERE account = %s)'
            cursor.execute(sql, (customer_review, employee_id, account))

            # 更新customers表中的purchase_count字段
            sql = 'UPDATE customers SET purchase_count = %s WHERE account = %s'
            cursor.execute(sql, (purchase_count, account))

            # 提交事务
            connection.commit()

    except Exception as e:
        # 回滚事务
        connection.rollback()
        raise e

    finally:
        connection.close()


# def insert_billing(customer_id, employee_id, customer_review):
#     """
#     将数据插入到 Billing 表
#     参数:
#         customer_id: 顾客ID
#         employee_id: 员工ID
#         customer_review: 顾客评价
#     """
#     connection = get_connection()
#
#     try:
#         with connection.cursor() as cursor:
#             # 生成当前时间
#             bill_time = datetime.datetime.now()
#
#             # 获取对应顾客ID的消费金额并相加
#             sql = 'SELECT SUM(price) FROM customer_orders WHERE customer_id = %s'
#             cursor.execute(sql, (customer_id,))
#             result = cursor.fetchone()
#             amount = result[0] if result[0] else 0
#
#             # 插入数据到 Billing 表
#             sql = 'INSERT INTO Billing (bill_time, employee_id, customer_id, amount, customer_review) VALUES (%s, %s, %s, %s, %s)'
#             cursor.execute(sql, (bill_time, employee_id, customer_id, amount, customer_review))
#
#             connection.commit()
#
#     finally:
#         connection.close()


def clear_customer_orders(customer_id):
    """
    清空指定顾客的 customer_orders 表中的数据
    参数:
        customer_id: 顾客ID
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # 删除指定顾客的数据
            sql = 'DELETE FROM customer_orders WHERE customer_id = %s'
            cursor.execute(sql, (customer_id,))

            connection.commit()

    finally:
        connection.close()


# 员工登录
def check_employee_credentials(account, password):
    """
    验证员工凭据
    参数:
        - account: 登录账号
        - password: 登录密码
    返回值:
        True，如果凭据验证通过；False，如果凭据验证失败
    """
    connection = pymysql.connect(**DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM employees WHERE account = %s AND password = %s'
            cursor.execute(sql, (account, password))
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False
    finally:
        connection.close()


# 获取所有员工信息
def get_employees_all():
    """
    获取所有员工的数据
    返回值:
        包含员工数据的列表
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM employees'
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    finally:
        connection.close()


# 罚款金额
def post_penalty_salary(employee_id, penalty_amount):
    """
    更新员工的罚款金额

    参数:
        employee_id: 员工ID
        penalty_amount: 罚款金额

    返回值:
        更新成功返回 True，否则返回 False
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # 执行更新操作
            sql = "UPDATE employees SET penalty_salary = %s WHERE employee_id = %s"
            cursor.execute(sql, (penalty_amount, employee_id))

            # 提交事务
            connection.commit()

            return True

    except Exception as e:
        # 发生异常时回滚事务
        connection.rollback()
        print("Failed to update penalty salary:", e)
        return False

    finally:
        connection.close()


# 注册员工
def register_employee(account, password, name, position, base_salary):
    """
    注册员工
    参数:
        - account: 登录账号
        - password: 登录密码
        - name: 员工姓名
        - position: 员工职位
    返回值:
        True，如果注册成功；False，如果注册失败
    """
    connection = pymysql.connect(**DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO employees (account, password, employee_name, position, base_salary) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (account, password, name, position, base_salary))
            connection.commit()
            return True
    except Exception as e:
        print(f"注册失败: {e}")
        return False
    finally:
        connection.close()


# 获取员工的下单次数
def get_billing_employee():
    """
    更新"employees"表中的"completed_count"字段，根据"Billing"表中的员工下单次数
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # 获取员工ID和对应的下单次数
            sql = "SELECT employee_id, COUNT(*) as count FROM Billing GROUP BY employee_id"
            cursor.execute(sql)

            # 获取查询结果
            results = cursor.fetchall()

            # 更新"employees"表中的"completed_count"字段
            for employee_id, count in results:
                sql = "UPDATE employees SET completed_count = %s WHERE employee_id = %s"
                cursor.execute(sql, (count, employee_id))

            connection.commit()

    except Exception as e:
        print("Failed to update completed_count:", e)
        connection.rollback()

    finally:
        connection.close()


# 修改员工信息
def update_employee(position, employee_name, account, password):
    """
    修改员工信息的操作

    参数:
        position: 员工职位
        employee_name: 员工姓名
        account: 员工账号
        password: 员工密码

    返回值:
        修改成功返回 True，否则返回 False
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # 执行更新操作
            sql = "UPDATE employees SET position=%s, employee_name=%s, password=%s WHERE account=%s"
            cursor.execute(sql, (position, employee_name, password, account))

            # 提交事务
            connection.commit()

            return True

    except Exception as e:
        # 发生异常时回滚事务
        connection.rollback()
        print("Failed to update employee:", e)
        return False

    finally:
        connection.close()


# 菜谱
def create_recipe(name, status, recipe_type, price):
    """
    创建菜谱并将其添加到数据库
    参数:
        - name: 菜谱名称
        - status: 状态（售空或在售）
        - recipe_type: 类型
        - price: 价格
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO recipes (dish_name, dish_status, recipe_type, price) VALUES (%s, %s, %s, %s)'
            cursor.execute(sql, (name, status, recipe_type, price))
            connection.commit()
    finally:
        connection.close()


def get_all_recipes():
    """
    获取所有菜谱的数据
    返回值:
        包含菜谱数据的列表
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM recipes'
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    finally:
        connection.close()


def delete_recipe(recipe_id):
    """
    根据菜谱ID删除菜谱
    参数:
        - recipe_id: 菜谱ID
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM recipes WHERE dish_id = %s'
            cursor.execute(sql, (recipe_id,))
            connection.commit()
    finally:
        connection.close()


def insert_recipe(name, status, recipe_type, price):
    """
    插入菜谱信息到数据库
    参数:
        - name: 菜谱名称
        - status: 状态（售空或在售）
        - recipe_type: 类型
        - price: 价格
    返回值:
        插入的菜谱ID，如果插入失败则返回 None
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO recipes (dish_name, dish_status, recipe_type, price) VALUES (%s, %s, %s, %s)'
            cursor.execute(sql, (name, status, recipe_type, price))
            connection.commit()
            recipe_id = cursor.lastrowid
            return recipe_id
    except:
        connection.rollback()
        return None
    finally:
        connection.close()


def update_recipe(recipe_id, name, status, recipe_type, price):
    """
    根据菜谱ID更新菜谱信息
    参数:
        - recipe_id: 菜谱ID
        - name: 菜谱名称
        - status: 状态（售空或在售）
        - recipe_type: 类型
        - price: 价格
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = 'UPDATE recipes SET dish_name=%s, dish_status=%s, recipe_type=%s, price=%s WHERE dish_id=%s'
            cursor.execute(sql, (name, status, recipe_type, price, recipe_id))
            connection.commit()
    finally:
        connection.close()


def get_billing():
    """
    获取账单数据
    返回值:
        账单数据的列表，每个元素为一条账单记录
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT bill_id, bill_time, employee_id, customer_id, amount, customer_review FROM billing"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    except Exception as e:
        print("Failed to retrieve billing data:", e)

    finally:
        connection.close()


def post_billing(bill_id, bill_time, employee_id, customer_id, amount, customer_review):
    """
    插入账单数据

    参数:
        bill_id: 账单编号
        bill_time: 账单时间
        employee_id: 员工编号
        customer_id: 顾客编号
        amount: 账单金额
        customer_review: 顾客评价

    返回值:
        插入成功返回 True，否则返回 False
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # 执行插入操作
            sql = "INSERT INTO billing (bill_id, bill_time, employee_id, customer_id, amount, customer_review) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (bill_id, bill_time, employee_id, customer_id, amount, customer_review))

            # 提交事务
            connection.commit()

            return True

    except Exception as e:
        # 发生异常时回滚事务
        connection.rollback()
        print("Failed to insert billing data:", e)
        return False

    finally:
        connection.close()


def save_order(customer_id, dish_id, dish_name, price, order_count):
    """
    保存点菜信息到客户已点菜品表，并更新菜谱表中的 monthly_orders 参数
    参数:
        - customer_id: 客户ID
        - dish_id: 菜品ID
        - dish_name: 菜品名称
        - price: 菜品价格
        - order_count: 客户点菜的序列号
    返回值:
        True，如果保存成功；False，如果保存失败
    """
    connection = pymysql.connect(**DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            # 保存点菜信息到客户已点菜品表
            sql = 'INSERT INTO customer_orders (customer_id, dish_id, dish_name, price, order_count) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (customer_id, dish_id, dish_name, price, order_count))
            connection.commit()

            # 更新菜谱表中的 monthly_orders 参数
            sql = 'UPDATE recipes SET monthly_orders = monthly_orders + 1 WHERE dish_id = %s'
            cursor.execute(sql, (dish_id,))
            connection.commit()

            return True
    except Exception as e:
        print(f"保存点菜信息失败: {e}")
        return False
    finally:
        connection.close()


def get_recipe_by_id(dish_id):
    """
    根据菜品编号查询菜谱信息
    参数：
        dish_id: 菜品编号
    返回值：
        查询到的菜谱信息，如果未查询到则返回 None
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM recipes WHERE dish_id = %s'
            cursor.execute(sql, (dish_id,))
            result = cursor.fetchone()
            return result

    finally:
        connection.close()


def get_customer_orders():
    """
    获取 customer_orders 表的全部数据
    返回值:
        包含 customer_orders 数据的列表
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM customer_orders'
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    finally:
        connection.close()


def calculate_total_amount(customer_id):
    """
    计算指定客户的消费总额并更新到customers表的total_amount字段
    参数:
        - customer_id: 客户ID
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # 查询billing表中指定客户的订单数据并计算消费总额
            sql = 'SELECT SUM(amount) FROM billing WHERE customer_id = %s'
            cursor.execute(sql, (customer_id,))
            result = cursor.fetchone()
            total_amount = result[0] if result[0] else 0

            # 更新customers表中的total_amount字段
            sql = 'UPDATE customers SET total_amount = %s WHERE id = %s'
            cursor.execute(sql, (total_amount, customer_id))
            connection.commit()

    finally:
        connection.close()



