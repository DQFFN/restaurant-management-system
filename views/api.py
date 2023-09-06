from flask import Blueprint, request, jsonify, render_template, url_for, session
from mysql import *
from datetime import datetime
import pytz

api_bp = Blueprint('api', __name__)


# 获取客户信息
def get_customer_info(account):
    all_customer_data = get_customer_all()
    for customer_data in all_customer_data:
        if customer_data[2] == account:
            return {'id': customer_data[0], 'name': customer_data[1], 'account': account, 'password': customer_data[3],
                    'purchase_count': customer_data[4], 'total_amount': customer_data[5]}
    return None


# 获取员工信息
def get_employees_info(account):
    all_employees_data = get_employees_all()
    for employee_data in all_employees_data:
        if employee_data[3] == account:
            return {
                'employee_id': employee_data[0],
                'position': employee_data[1],
                'employee_name': employee_data[2],
                'account': employee_data[3],
                'password': employee_data[4],
                'base_salary': employee_data[5],
                'performance': employee_data[6],
                'bonus_salary': employee_data[7],
                'penalty_salary': employee_data[8],
                'total_salary': employee_data[9],
                'order_count': employee_data[10],
                'completed_count': employee_data[11]
            }
    return None


# 登录
@api_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('login_account')
        password = request.form.get('login_password')

        # 检查输入
        if not account or not password:
            return jsonify(login_success=False, message="用户名和密码不能为空")

        # 验证客户凭据
        elif check_customer_credentials(account, password):
            # 登录成功，将用户类型、账号和客户信息存入会话
            session['user_type'] = 'customer'
            session['account'] = account
            customer_info = get_customer_info(account)  # 获取客户信息
            if customer_info is not None:
                session['customer_info'] = customer_info  # 将客户信息存入会话
            return jsonify(login_success=True, redirect_url=url_for('main.customers', customer_info=customer_info))

        # 验证管理员凭据
        elif check_manager_credentials(account, password):
            # 登录成功，将用户类型存入会话
            session['user_type'] = 'manager'
            return jsonify(login_success=True, redirect_url=url_for('main.admin'))

        # 验证员工凭据
        elif check_employee_credentials(account, password):
            # 登录成功，将用户类型和员工ID存入会话
            session['user_type'] = 'employee'
            session['account'] = account  # 存储账户名
            employee_info = get_employees_info(account)  # 获取员工信息
            if employee_info is not None:
                session['employee_info'] = employee_info  # 将员工信息存入会话
                session['employee_id'] = employee_info['employee_id']  # 获取并存储员工ID
            return jsonify(login_success=True, redirect_url=url_for('main.employees'))

        else:
            # 登录失败，返回JSON响应
            return jsonify(login_success=False, message="用户名或密码错误")
    else:
        # GET 请求，显示登录页面
        return render_template('login.html')


# 获取当前登录客户的个人信息
@api_bp.route('/customer/info', methods=['GET'])
def get_customer_info_route():
    if 'user_type' in session and session['user_type'] == 'customer':
        customer_info = session.get('customer_info')
        if customer_info is not None:
            account = customer_info['account']
            # 使用get_customer_info函数获取客户信息，包括purchase_count字段
            customer_info = get_customer_info(account)
            if customer_info is not None:
                customer_id = customer_info['id']
                calculate_total_amount(customer_id)  # 计算消费总额并更新到customers表的total_amount字段
                return jsonify(success=True, data=customer_info)

    return jsonify(success=False, message="无法获取客户信息")


# 获取员工信息
@api_bp.route('/employees/info', methods=['GET'])
def get_employees_info_route():
    if 'user_type' in session and session['user_type'] == 'employee':
        account = session.get('account')  # 获取账户名
        if account is not None:
            get_billing_employee()  # 更新员工的下单次数
            employee_info = get_employees_info(account)  # 使用账户名获取员工信息
            if employee_info is not None:
                return jsonify(success=True, data=employee_info)
    return jsonify(success=False, message='用户未登录或非员工用户')


# 修改客户信息
@api_bp.route('/register/updatecustomer', methods=['POST'])
def update_customer():
    data = request.get_json()
    name = data.get('name')
    account = data.get('account')
    password = data.get('password')

    success = update_customer_in_db(name, account, password)

    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Failed to update customer information'})


# 注册客户
@api_bp.route('/register/customer', methods=['POST'])
def register():
    name = request.form.get('register_name')
    account = request.form.get('register_account')
    password = request.form.get('register_password')

    # 检查输入
    if not name or not account or not password:
        return jsonify(register_success=False, message="姓名、用户名和密码不能为空")

    # 在此处添加其他的输入验证逻辑，如检查账号是否已存在等

    # 初始化下单次数和消费金额为0
    purchase_count = 0
    total_amount = 0.00

    # 将用户数据插入数据库
    insert_customer(name, account, password, purchase_count, total_amount)

    # 注册成功，返回JSON响应
    return jsonify(register_success=True, message="注册成功")


# 注册员工
@api_bp.route('/register/employee', methods=['POST'])
def register_employee_api():
    """
    注册员工账号的API

    请求方法：POST
    请求体参数：
        - position: 员工职位
        - employee_name: 员工姓名
        - account: 员工账号
        - password: 员工密码
        - base_salary: 员工基本工资

    返回值：
        - 注册成功：{"success": true}
        - 注册失败：{"success": false, "message": 错误信息}
    """
    try:
        data = request.get_json()
        position = data.get('position')
        employee_name = data.get('employee_name')
        account = data.get('account')
        password = data.get('password')
        base_salary = data.get('base_salary')

        # 执行注册员工账号的操作
        success = register_employee(account, password, employee_name, position, base_salary)

        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Failed to register employee'})

    except Exception as e:
        # 处理异常并返回适当的错误响应
        error_message = "Failed to register employee: {}".format(str(e))
        return jsonify({'success': False, 'message': error_message}), 500


# 修改员工信息
@api_bp.route('/register/updateemployee', methods=['POST'])
def update_employee_api():
    try:
        data = request.get_json()
        position = data.get('position')
        employee_name = data.get('employee_name')
        account = data.get('account')
        password = data.get('password')
        old_password = data.get('old_password')

        # 查询数据库，验证旧密码是否匹配
        connection = pymysql.connect(**DB_CONFIG)

        try:
            with connection.cursor() as cursor:
                # 根据账号查询数据库中的密码字段
                query = "SELECT password FROM employees WHERE account = %s"
                cursor.execute(query, (account,))
                result = cursor.fetchone()

                if result:
                    password_from_db = result[0]
                    if password_from_db == old_password:
                        # 旧密码匹配，执行更新员工信息的操作
                        sql = "UPDATE employees SET position = %s, employee_name = %s, password = %s WHERE account = %s"
                        cursor.execute(sql, (position, employee_name, password, account))
                        connection.commit()
                        return jsonify({'success': True})
                    else:
                        # 旧密码不匹配
                        return jsonify({'success': False, 'message': '旧密码错误'})

                # 账号不存在
                return jsonify({'success': False, 'message': '账号不存在'})

        except Exception as e:
            print(f"更新员工信息失败: {e}")
            return jsonify({'success': False, 'message': 'Failed to update employee'})

        finally:
            connection.close()

    except Exception as e:
        # 处理异常并返回适当的错误响应
        error_message = "Failed to update employee: {}".format(str(e))
        return jsonify({'success': False, 'message': error_message}), 500


# 显示菜谱
@api_bp.route('/recipes', methods=['GET'])
def get_recipes():
    try:
        recipes = get_all_recipes()  # 从数据库获取数据
        filtered_recipes = [recipe for recipe in recipes if recipe[2] == '1']
        return jsonify(filtered_recipes)  # 将数据转换为 JSON 并返回
    except Exception as e:
        error_message = "Failed to retrieve recipes: {}".format(str(e))
        return jsonify({'success': False, 'message': error_message}), 500


# 新增菜谱
@api_bp.route('/recipes', methods=['POST'])
def add_recipe():
    # 从请求中获取菜谱信息
    name = request.form.get('name')
    status = request.form.get('status')
    recipe_type = request.form.get('type')
    price = request.form.get('price')

    # 检查必要参数是否存在
    if not name or not status or not recipe_type or not price:
        return jsonify(success=False, message="缺少必要参数")

    # 调用插入菜谱的函数
    recipe_id = insert_recipe(name, status, recipe_type, price)

    if recipe_id:
        return jsonify(success=True, recipe_id=recipe_id, message="菜谱添加成功")
    else:
        return jsonify(success=False, message="菜谱添加失败")


# 删除菜谱
@api_bp.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe_api(recipe_id):
    """
    API路由，用于删除菜谱
    """
    try:
        delete_recipe(recipe_id)
        return {'success': True, 'message': '菜谱删除成功'}
    except:
        return {'success': False, 'message': '菜谱删除失败，请重试'}


# 更新菜谱
@api_bp.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe_api(recipe_id):
    """
    API路由，用于更新菜谱
    """
    name = request.form.get('name')
    status = request.form.get('status')
    recipe_type = request.form.get('type')
    price = request.form.get('price')

    try:
        update_recipe(recipe_id, name, status, recipe_type, price)
        return {'success': True, 'message': '菜谱更新成功'}
    except:
        return {'success': False, 'message': '菜谱更新失败，请重试'}


@api_bp.route('/DetailInfo', methods=['GET'])
def get_employees_api():
    """
    获取所有员工的数据，并以JSON格式返回
    返回值:
        JSON格式的员工数据，包括计算后的工资数据
    """
    try:
        employees = get_employees_all()  # 调用之前在mysql.py中定义的get_employees_all()函数

        # 计算工资并将员工数据转换为JSON格式
        json_data = []
        for employee in employees:
            employee_id = employee[0]
            position = employee[1]
            employee_name = employee[2]
            account = employee[3]
            password = employee[4]
            base_salary = float(employee[5])
            performance = float(employee[6]) if employee[6] is not None else 0.0

            # 根据员工绩效计算奖励工资
            bonus_salary = performance * 20

            # 获取罚款金额
            penalty_salary = float(employee[8]) if employee[8] is not None else 0.0

            # 计算员工总工资
            total_salary = base_salary + bonus_salary - penalty_salary

            # 构建员工数据字典
            employee_dict = {
                'employee_id': employee_id,
                'position': position,
                'employee_name': employee_name,
                'account': account,
                'password': password,
                'base_salary': str(base_salary),
                'performance': str(performance),
                'bonus_salary': str(bonus_salary),
                'penalty_salary': str(penalty_salary),
                'total_salary': str(total_salary)
            }

            json_data.append(employee_dict)

        return jsonify(json_data)

    except Exception as e:
        # 处理异常并返回适当的错误响应
        error_message = "Failed to retrieve employee data: {}".format(str(e))
        return jsonify({'error': error_message}), 500


@api_bp.route('/DetailInfo/penalty', methods=['POST'])
def post_penalty_salary_api():
    """
    POST 请求用于插入罚款金额

    请求体 JSON 格式:
    {
        "employee_id": 员工ID,
        "penalty_amount": 罚款金额
    }

    返回 JSON 格式:
    {
        "success": True 或 False,
        "message": 提示信息
    }
    """
    try:
        data = request.get_json()

        employee_id = data.get('employee_id')
        penalty_amount = data.get('penalty_amount')

        if employee_id is None or penalty_amount is None:
            return jsonify({"success": False, "message": "员工ID和罚款金额不能为空"})

        # 调用 post_penalty_salary 函数插入罚款金额
        success = post_penalty_salary(employee_id, penalty_amount)

        if success:
            return jsonify({"success": True, "message": "罚款金额插入成功"})
        else:
            return jsonify({"success": False, "message": "罚款金额插入失败"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@api_bp.route('/DetailInfo/billing', methods=['GET'])
def get_billing_info_api():
    """
    获取消费信息的API

    请求方法：GET

    返回值：
        - 成功：{"success": true, "billing_info": {"total_amount": 消费金额, "order_count": 下单次数}}
        - 失败：{"success": false, "message": 错误信息}
    """
    try:
        # 获取查询参数
        employee_id = request.args.get('employee_id')
        date = request.args.get('date')

        # 构建查询参数列表
        query_params = []

        # 连接到数据库
        connection = get_connection()

        with connection.cursor() as cursor:
            # 创建SQL查询
            sql = "SELECT employee_id, amount FROM Billing WHERE 1=1"

            # 如果提供了员工ID，则添加员工ID的查询条件
            if employee_id:
                sql += " AND employee_id = %s"
                query_params.append(employee_id)

            # 如果提供了日期，则添加日期的查询条件
            if date:
                sql += " AND DATE(bill_time) = %s"
                query_params.append(date)

            # 执行SQL查询
            cursor.execute(sql, query_params)
            billing_data = cursor.fetchall()

        # 统计消费金额和下单次数
        total_amount = sum([amount for _, amount in billing_data])
        order_count = len(billing_data)

        # 构建响应数据
        response_data = {
            "total_amount": total_amount,
            "order_count": order_count
        }

        return jsonify({'success': True, 'billing_info': response_data})

    except Exception as e:
        # 处理异常并返回适当的错误响应
        error_message = "Failed to retrieve billing info: {}".format(str(e))
        return jsonify({'success': False, 'message': error_message}), 500


@api_bp.route('/ShowBills', methods=['GET'])
def get_ShowBills_all():
    """
    获取所有账单数据，并以JSON格式返回
    """
    try:
        user_type = session.get('user_type')

        # 获取所有账单
        billing_data = get_billing()  # 调用之前在mysql.py中定义的get_billing()函数

        if user_type == 'employee':
            employee_id = session.get('employee_id')
            # 筛选出与当前员工相关联的账单
            billing_data = [bill for bill in billing_data if bill[2] == employee_id]
        elif user_type != 'manager':
            return jsonify({'error': '无权访问账单数据'})

        json_data = []
        for bill in billing_data:
            bill_id = bill[0]
            bill_time = bill[1].strftime("%Y年%m月%d日")
            employee_id = bill[2]
            customer_id = bill[3]
            amount = bill[4]
            customer_review = bill[5]

            bill_dict = {
                'bill_id': bill_id,
                'bill_time': bill_time,
                'employee_id': employee_id,
                'customer_id': customer_id,
                'amount': amount,
                'customer_review': customer_review
            }

            json_data.append(bill_dict)

        return jsonify(json_data)

    except Exception as e:
        error_message = "Failed to retrieve billing data: {}".format(str(e))
        return jsonify({'error': error_message}), 500


# 新增账单
@api_bp.route('/ShowBills', methods=['POST'])
def post_show_bills():
    try:
        data = request.get_json()
        year = int(data.get('year'))
        month = int(data.get('month'))
        day = int(data.get('day'))
        customer_id = int(data.get('customer_id'))
        employee_id = int(data.get('employee_id'))
        totalMY = float(data.get('totalMY'))
        customer_review = data.get('feedback')

        # 获取当前时间（北京时间）
        tz = pytz.timezone('Asia/Shanghai')
        now = datetime.now(tz)

        # 构造账单时间的 datetime 对象
        bill_timestamp_str = datetime(year, month, day, now.hour, now.minute, now.second)

        # 将 datetime 对象转换为字符串格式的时间戳
        bill_time = bill_timestamp_str.strftime("%Y-%m-%d %H:%M:%S")

        # 执行插入账单数据的操作
        success = post_billing(bill_id=None, bill_time=bill_time, employee_id=employee_id, customer_id=customer_id,
                               amount=totalMY, customer_review=customer_review)

        if success:
            user_type = session.get('user_type')
            # 如果是员工，清除订单
            if user_type == 'employee':
                clear_customer_orders(customer_id)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Failed to add billing data'})

    except Exception as e:
        error_message = "Failed to add billing data: {}".format(str(e))
        return jsonify({'success': False, 'message': error_message}), 500


# 获取客户的最大order_count
customer_max_order_count = {}


@api_bp.route('/order', methods=['POST'])
def place_order():
    try:
        if 'user_type' in session and session['user_type'] == 'customer':
            customer_info = session.get('customer_info')
            if customer_info is not None:
                customer_id = customer_info['id']  # 获取当前登录客户的ID
                data = request.get_json()
                dishes = data.get('dishes')

                if isinstance(dishes, list):
                    # 批量保存点菜信息
                    success = True  # 默认设置为成功

                    # 获取客户的最大order_count，如果不存在则设置为0
                    max_order_count = customer_max_order_count.get(customer_id, 0)

                    for dish_info in dishes:
                        dish_id = dish_info.get('dish_id')

                        # 更新order_count为下一个值，并更新最大order_count
                        max_order_count += 1
                        order_count = max_order_count

                        # 获取菜谱信息
                        dish = get_recipe_by_id(dish_id)
                        if dish:
                            dish_name = dish[1]
                            price = dish[4]
                            result = save_order(customer_id, dish_id, dish_name, price, order_count)

                            # 如果有一个保存失败，则将成功标志设置为 False
                            if not result:
                                success = False
                                break
                        else:
                            success = False
                            break

                    if success:
                        # 更新客户的最大order_count
                        customer_max_order_count[customer_id] = max_order_count

                        return jsonify({'success': True})
                    else:
                        return jsonify({'success': False, 'message': 'Failed to save order'})
                else:
                    return jsonify({'success': False, 'message': '提交的菜品数据格式不正确'})
            else:
                return jsonify({'success': False, 'message': '无法提交订单，未获取到客户信息'})
        else:
            return jsonify({'success': False, 'message': '无法提交订单，用户未登录或非客户用户'})
    except Exception as e:
        error_message = "Failed to place order: {}".format(str(e))
        return jsonify({'success': False, 'message': error_message}), 500


@api_bp.route('/customer/orders', methods=['GET'])
def get_customer_orders_api():
    if 'user_type' in session and session['user_type'] == 'customer':
        customer_id = session.get('customer_info').get('id')  # 获取当前登录客户的ID
        customer_orders = get_customer_orders()  # 获取 customer_orders 表的全部数据
        orders_data = [[order[7], order[3], order[4]] for order in customer_orders if
                       order[1] == customer_id]  # 只保留订单ID、菜名和价格字段的数据，并筛选出当前客户的订单数据
        return jsonify(orders_data)  # 将数据转换为 JSON 并返回

    return jsonify(success=False, message="无法获取客户订单数据")


# 更新客户的消费次数
@api_bp.route('/customer/orders/History', methods=['POST'])
def update_orders_History():
    account = session.get('account')  # 获取账号信息

    if account:
        customer_info = get_customer_info(account)  # 获取客户信息

        if customer_info:
            purchase_count = customer_info['purchase_count']  # 获取当前消费次数
            customer_review = request.form.get('customer_review')  # 获取客户评价
            employee_id = request.form.get('employee_id')  # 获取服务员工ID

            try:
                # 更新购买次数、评价和服务员工ID
                update_purchase_and_review(account, purchase_count + 1, customer_review, employee_id)

                # 返回更新后的消费次数
                return jsonify(account=account, purchase_count=purchase_count + 1)

            except Exception as e:
                return jsonify(error=str(e))

    return jsonify(error="无法获取客户信息")


# 获取待提交订单
@api_bp.route('/employees/orders', methods=['GET'])
def get_employees_orders():
    try:
        # 检查用户类型
        user_type = session.get('user_type')

        if user_type != 'employee':
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

        # 获取员工ID
        employee_id = session.get('employee_id')

        # 调用get_customer_orders函数获取customer_orders表的全部数据
        orders = get_customer_orders()

        # 构建待提交订单数据的字典，字典的键是customer_id，值是对应客户的订单数据
        employees_orders_dict = {}
        customer_prices = {}  # 用于记录每个customer_id对应的价格

        for order in orders:
            order_id = order[0]
            customer_id = order[1]
            price = order[4]
            employee_id_order = order[6]
            customer_review = order[5]

            # 仅处理与当前员工相关的订单数据
            if employee_id_order != employee_id:
                continue

            # 计算总消费金额
            if customer_id not in customer_prices:
                customer_prices[customer_id] = 0
            customer_prices[customer_id] += price

            # 获取当前时间（北京时间）
            tz = pytz.timezone('Asia/Shanghai')
            now = datetime.now(tz)

            # 构建待提交订单数据的字典
            current_time = now.strftime('%Y-%m-%d %H:%M:%S')
            current_time_formatted = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S').strftime(
                '%Y年%m月%d日')
            order_data = {
                'order_id': order_id,
                'customer_id': customer_id,
                'employee_id': employee_id_order,
                'current_time': current_time_formatted,
                'customer_review': customer_review
            }

            # 将订单数据添加到对应客户的订单数据中
            if customer_id not in employees_orders_dict:
                employees_orders_dict[customer_id] = order_data
            else:
                # 如果已存在订单数据，则更新其review和order_id
                old_order = employees_orders_dict[customer_id]
                old_order['customer_review'] = max(old_order['customer_review'], customer_review)
                old_order['order_id'] = max(old_order['order_id'], order_id)

        # 更新待提交订单数据的价格字段
        for customer_id, order_data in employees_orders_dict.items():
            total_price = customer_prices[customer_id]
            order_data['total_price'] = total_price

        # 将字典转化为列表
        employees_orders = list(employees_orders_dict.values())

        # 返回待提交订单数据
        if employees_orders:
            return jsonify(employees_orders)
        else:
            return jsonify([])

    except Exception as e:
        error_message = "Failed to retrieve employees orders: {}".format(str(e))
        return jsonify({'success': False, 'message': error_message}), 500
