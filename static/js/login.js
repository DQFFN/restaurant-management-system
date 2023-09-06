function login() {
    // 获取账号和密码输入框的值
    var account = $('#account').val();
    var password = $('#password').val();

    // 发送登录请求
    $.ajax({
        url: '/api/login',  // 修改为对应的 API 路径
        method: 'POST',
        data: {
            login_account: account,
            login_password: password
        },
        success: function(response) {
            if (response.login_success) {
                console.log('登录成功');
                // 重定向或执行其他操作
                window.location.href = response.redirect_url;
            } else {
                console.log('登录失败');
                alert(response.message);
            }
        },
        error: function(error) {
            console.log('登录失败');
            alert('登录失败，请重试');
        }
    });
}



