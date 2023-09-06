$(document).ready(function() {
    // 当页面加载完成后执行以下代码

    // 获取菜谱数据并显示
    $.ajax({
        url: '/api/recipes', // 请求的URL，根据你的路由设置进行修改
        method: 'GET',
        success: function(response) {
            // 请求成功的回调函数
            // response 为服务器返回的菜谱数据

            if (Array.isArray(response)) {
                // 遍历菜谱数据并添加到表格中
                response.forEach(function(recipe) {
                    var dishId = recipe[0];
                    var dishName = recipe[1];
                    var dishStatus = recipe[2];
                    var recipeType = recipe[3];
                    var price = recipe[4];
                    var monthlyOrders = recipe[5];

                    var row = '<tr>';
                    row += '<td class="dish-id">' + dishId + '</td>';
                    row += '<td>' + dishName + '</td>';
                    row += '<td>' + dishStatus + '</td>';
                    row += '<td>' + recipeType + '</td>';
                    row += '<td>' + price + '</td>';
                    row += '<td>' + monthlyOrders + '</td>';
                    row += '<td><label><input type="checkbox" name="food[]" value="' + dishId + '"> 点菜</label></td>';
                    row += '</tr>';

                    $('.menu-table').append(row);
                });
            }
        },
        error: function(xhr, status, error) {
            // 请求失败的回调函数
            console.error('Failed to get recipes:', error);
            // 可以在页面上显示错误信息，例如使用一个警告框
            alert('获取菜谱失败：' + error);
        }
    });

    // 监听表单的提交事件
    $('#order-form').submit(function(event) {
    event.preventDefault();

    // 获取表单中选中的菜品ID
    var selectedDishes = [];
    var orderCount = 1;  // 初始化 orderCount
    $('input[name="food[]"]:checked').each(function() {
        var dishId = $(this).val();
        selectedDishes.push({dish_id: dishId, order_count: orderCount});
        orderCount++;  // 增加 orderCount 为下一道菜品
    });

    if (selectedDishes.length > 0) {
        var customerId = '{{ customer_info["id"] }}'; // 替换为实际的客户ID

        // 发起 AJAX POST 请求提交菜品订单
        $.ajax({
            url: '/api/order', // 请求的URL，根据你的路由设置进行修改
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                customer_id: customerId,
                dishes: selectedDishes
            }),
            success: function(response) {
                // 请求成功的回调函数
                // response 为服务器返回的响应

                if (response.hasOwnProperty('success') && response.success) {
                    // 提交成功，显示成功提示
                    alert('点菜成功！');

                    // 弹出窗口询问用户是否完成点单
                    if (confirm('是否完成点单？')) {
                        // 用户确认完成点单，刷新页面
                        location.reload();
                        location.assign('/CurrentOrder');
                    } else {
                        // 用户取消完成点单，可以进行其他操作
                        // 例如清空表单数据或进行其他处理
                        $('input[name="food[]"]').prop('checked', false);
                    }
                } else {
                    // 提交失败，显示错误提示
                    console.error(response.hasOwnProperty('message') ? response.message : 'Failed to place order');
                    // 可以在页面上显示错误信息，例如使用一个警告框
                    alert('点菜失败');
                }
            },
            error: function(xhr, status, error) {
                // 请求失败的回调函数
                console.error('Failed to place order:', error);
                // 可以在页面上显示错误信息，例如使用一个警告框
                alert('点菜请求失败：' + error);
            }
        });
    } else {
        // 没有选择菜品
        alert('请选择至少一道菜品！');
    }
});


    // 其他 JavaScript 代码...
});
