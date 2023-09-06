$(document).ready(function() {
  // 发起AJAX GET请求获取账单数据
  $.ajax({
    url: '/api/ShowBills',  // 请求的URL，根据你的路由设置进行修改
    method: 'GET',
    success: function(response) {
      // 请求成功的回调函数
      // response为服务器返回的响应

      // 遍历账单数据，并将其添加到表格中
      for (var i = 0; i < response.length; i++) {
        var bill = response[i];
        var row = '<tr>' +
          '<td>' + bill.bill_id + '</td>' +
          '<td>' + bill.bill_time + '</td>' +
          '<td>' + bill.employee_id + '</td>' +
          '<td>' + bill.customer_id + '</td>' +
          '<td>' + bill.amount + '</td>' +
          '<td>' + bill.customer_review + '</td>' +
          '</tr>';

        $('#table_page').append(row);
      }
    },
    error: function(xhr, status, error) {
      // 请求失败的回调函数
      console.error('Failed to retrieve billing data:', error);
      // 可以在页面上显示错误信息，例如使用一个警告框
      alert("请求失败：" + error);
    }
  });

  // 其他JavaScript代码...
});

$(document).ready(function() {
  // 当页面加载完成后执行以下代码

  // 监听表单的提交事件
  $('form').submit(function(event) {
    event.preventDefault();

    // 获取表单中的数据
    var bill_id = $('input[name="bill_id"]').val();
    var year = $('input[name="year"]').val();
    var month = $('input[name="month"]').val();
    var day = $('input[name="day"]').val();
    var customer_id = $('input[name="customer_id"]').val();
    var employee_id = $('input[name="employee_id"]').val();
    var totalMY = $('input[name="totalMY"]').val();
    var feedback = $('input[name="feedback"]').val();

    // 发起AJAX POST请求添加账单数据
    $.ajax({
      url: '/api/ShowBills',  // 请求的URL，根据你的路由设置进行修改
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        "bill_id": bill_id,
        "year": year,
        "month": month,
        "day": day,
        "customer_id": customer_id,
        "employee_id": employee_id,
        "totalMY": totalMY,
        "feedback": feedback
      }),
      success: function(response) {
        // 请求成功的回调函数
        // response为服务器返回的响应

        if (response.hasOwnProperty('success') && response.success) {
          // 添加成功，显示成功提示
          alert("账单添加成功！");
          // 刷新页面
          location.reload();
        } else {
          // 添加失败，显示错误提示
          console.error(response.hasOwnProperty('message') ? response.message : 'Failed to add billing data');
          // 可以在页面上显示错误信息，例如使用一个警告框
          alert("账单添加失败");
        }
      },
      error: function(xhr, status, error) {
        // 请求失败的回调函数
        console.error('Failed to add billing data:', error);
        // 可以在页面上显示错误信息，例如使用一个警告框
        alert("请求失败：" + error);
      }
    });
  });

  // 其他JavaScript代码...
});
