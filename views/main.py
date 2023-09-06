from flask import render_template, Blueprint, session, redirect, url_for

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/Restaurant')
def restaurant():
    return render_template('Restaurant.html')


@main_bp.route('/RestaurantHistory')
def restaurant_history():
    return render_template('RestaurantHistory.html')


@main_bp.route('/login')
def login():
    return render_template('login.html')


@main_bp.route('/Register')
def register():
    return render_template('Register.html')


@main_bp.route('/customers')
def customers():
    if 'user_type' not in session or session['user_type'] not in ['customer', 'manager']:
        # 如果用户没有登录，或者不是客户也不是管理员，重定向他们到登录页面
        return redirect(url_for('api.login'))
    # 客户的处理逻辑
    return render_template('customers.html')


@main_bp.route('/admin')
def admin():
    if 'user_type' not in session or session['user_type'] != 'manager':
        # 如果用户没有登录，或者用户不是管理员，重定向他们到登录页面
        return redirect(url_for('api.login'))
    # 管理员的处理逻辑
    return render_template('admin.html')


@main_bp.route('/employees')
def employees():
    if 'user_type' not in session or session['user_type'] not in ['employee', 'manager']:
        # 如果用户没有登录，或者不是员工也不是管理员，重定向他们到登录页面
        return redirect(url_for('api.login'))
    # 员工的处理逻辑
    return render_template('employees.html')


@main_bp.route('/ManageMenu')
def manage_menu():
    return render_template('ManageMenu.html')


@main_bp.route('/DetailInfo')
def DetailInfo():
    return render_template('DetailInfo.html')


@main_bp.route('/ShowBills')
def ShowBills():
    return render_template('ShowBills.html')


@main_bp.route('/Showadmin')
def Showadmin():
    return render_template('Showadmin.html')


@main_bp.route('/ChooseMenu')
def ChooseMenu():
    return render_template('ChooseMenu.html')


@main_bp.route('/ShowInfo')
def ShowInfo():
    return render_template('ShowInfo.html')


@main_bp.route('/CurrentOrder')
def CurrentOrder():
    return render_template('CurrentOrder.html')


@main_bp.route('/Billsemployees')
def Billsemployees():
    return render_template('Billsemployees.html')


@main_bp.route('/Showemployees')
def Showemployees():
    return render_template('Showemployees.html')
