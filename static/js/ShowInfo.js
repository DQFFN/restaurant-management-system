function getCustomerInfo() {
  $.ajax({
    url: '/api/customer/info',  // 请求的URL，根据你的后端路由设置进行修改
    method: 'GET',
    success: function(response) {
      if (response.success) {
        var customerInfo = response.data;
        $('#name').val(customerInfo.name);
        $('#account').val(customerInfo.account);
      } else {
        console.error(response.message);
      }
    },
    error: function(xhr, status, error) {
      console.error('Failed to get customer information:', error);
    }
  });
}

$(document).ready(function() {
  // 在页面加载完成后调用getCustomerInfo函数获取客户信息
  getCustomerInfo();

  // 监听表单的提交事件，并进行更新客户信息
  $('form').submit(function(event) {
    event.preventDefault();

    // 获取表单中输入的客户信息
    var name = $('#name').val();
    var account = $('#account').val();
    var password = $('#password').val();

    // 发起 AJAX POST 请求更新客户信息
    $.ajax({
      url: '/api/register/updatecustomer', // 请求的URL，根据你的后端路由设置进行修改
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        name: name,
        account: account,
        password: password
      }),
      success: function(response) {
        // 请求成功的回调函数
        // response 为服务器返回的响应

        if (response.hasOwnProperty('success') && response.success) {
          // 更新成功，显示成功提示
          alert('更新客户信息成功！');
          // 可以进行其他相关操作，例如清空表单数据或刷新页面
          $('form')[0].reset();
        } else {
          // 更新失败，显示错误提示
          console.error(response.hasOwnProperty('message') ? response.message : 'Failed to update customer information');
          // 可以在页面上显示错误信息，例如使用一个警告框
          alert('更新客户信息失败');
        }
      },
      error: function(xhr, status, error) {
        // 请求失败的回调函数
        console.error('Failed to update customer information:', error);
        // 可以在页面上显示错误信息，例如使用一个警告框
        alert('更新客户信息请求失败：' + error);
      }
    });
  });

  // 其他 JavaScript 代码...
});


$(document).ready(function() {
  // 发起 GET 请求获取客户信息
  $.ajax({
    url: '/api/customer/info', // 根据你的路由设置进行修改
    method: 'GET',
    success: function(response) {
      if (response.success) {
        // 获取订单次数和消费总额
        var purchase_count = response.data.purchase_count;
        var total_amount = response.data.total_amount;

        // 显示订单次数和消费总额
        $('#order_count').text(purchase_count);
        $('#total_amount').text(total_amount);
      } else {
        console.error('Failed to get customer information:', response.message);
        // 可以在页面上显示错误信息，例如使用一个警告框
        alert('获取客户信息失败');
      }
    },
    error: function(xhr, status, error) {
      console.error('Failed to get customer information:', error);
      // 可以在页面上显示错误信息，例如使用一个警告框
      alert('获取客户信息失败');
    }
  });
});


function openForm(id, date, employee_id, customer_id, total, feedback) {
    document.getElementById('orderForm').style.display = 'block';
    document.getElementById('orderID').value = id;
    document.getElementById('orderDate').value = date;
    document.getElementById('orderEmployee').value = employee_id;
    document.getElementById('orderCustomer').value = customer_id;
    document.getElementById('orderAmount').value = total;
    document.getElementById('orderFeedback').value = feedback;
}

