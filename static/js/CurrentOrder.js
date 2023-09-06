$(document).ready(function() {
    // 当页面加载完成后执行以下代码

    // 获取已点菜品数据并显示
    $.ajax({
        url: '/api/customer/orders', // 请求的URL，根据你的路由设置进行修改
        method: 'GET',
        success: function(response) {
            // 请求成功的回调函数
            // response 为服务器返回的已点菜品数据

            if (Array.isArray(response)) {
                // 遍历已点菜品数据并添加到表格中
                response.forEach(function(order) {
                    var orderId = order[0];
                    var dishName = order[1];
                    var price = order[2];

                    var row = '<tr>';
                    row += '<td>' + orderId + '</td>';
                    row += '<td>' + dishName + '</td>';
                    row += '<td>' + price + '</td>';
                    row += '</tr>';

                    $('.order-table').append(row);
                });
            }
        },
        error: function(xhr, status, error) {
            // 请求失败的回调函数
            console.error('Failed to get customer orders:', error);
            // 可以在页面上显示错误信息，例如使用一个警告框
            alert('获取已点菜品失败：' + error);
        }
    });

    // 其他 JavaScript 代码...
});



$(document).ready(function () {
    // 监听确认按钮的点击事件
    $('#confirm-button').submit(function (event) {
        event.preventDefault();

        // 获取评价和员工ID输入框的值
        var customer_review = $('#feedback-input').val();
        var employee_id = $('#employee-id-input').val();

        // 发起POST请求到指定的API端点
        $.ajax({
            url: '/api/customer/orders/History',
            method: 'POST',
            data: {
                customer_review: customer_review,
                employee_id: employee_id
            },
            success: function (response) {
                // 请求成功的处理逻辑
                if (response.hasOwnProperty('account') && response.hasOwnProperty('purchase_count')) {
                    var account = response.account;
                    var purchase_count = response.purchase_count;
                    console.log('更新消费次数成功', '账号:', account, '购买次数:', purchase_count);
                    alert('更新消费次数成功');
                } else {
                    console.log('无法获取客户信息');
                    alert('无法获取客户信息');
                }
            },
            error: function (xhr, status, error) {
                // 请求失败的处理逻辑
                console.log('更新消费次数失败', error);
                alert('更新消费次数失败');
            }
        });
    });
});





