function register() {
    // 获取姓名、账号、密码和确认密码输入框的值
    var name = $('#name').val();
    var account = $('#account').val();
    var password = $('#password').val();
    var confirm_password = $('#confirm_password').val();

    // 检查输入是否为空
    if (!name || !account || !password || !confirm_password) {
        alert("请输入姓名、账号和密码");
        return;
    }

    // 检查密码与确认密码是否一致
    if (password !== confirm_password) {
        alert("确认密码与密码不一致");
        return;
    }

    // 发送注册请求
    $.ajax({
        url: '/api/register/customer',
        method: 'POST',
        data: {
            register_name: name,
            register_account: account,
            register_password: password
        },
        success: function(response) {
            if (response.register_success) {
                console.log('注册成功');
                alert(response.message);
                // 可以在这里执行其他操作，如跳转到登录页面
            } else {
                console.log('注册失败');
                alert(response.message);
            }
        },
        error: function(error) {
            console.log('注册失败');
            alert('注册失败，请重试');
        }
    });
}
