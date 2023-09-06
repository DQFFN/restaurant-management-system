$(document).ready(function() {
  // 当页面加载完成后执行以下代码

  // 发起AJAX GET请求获取员工数据
  $.ajax({
    url: '/api/DetailInfo',  // 请求的URL，根据你的路由设置进行修改
    method: 'GET',
    dataType: 'json',
    success: function(response) {
      // 请求成功的回调函数
      // response为获取到的员工数据

      // 清空原有数据
      $('#employee-table-body').empty();

      // 遍历员工数据，添加到表格中
      for (var i = 0; i < response.length; i++) {
        var employee = response[i];
        var row = '<tr>' +
                    '<td>' + employee.employee_id + '</td>' +
                    '<td>' + employee.employee_name + '</td>' +
                    '<td>' + employee.position + '</td>' +
                    '<td>' + employee.base_salary + '</td>' +
                    '<td>' + employee.performance + '</td>' +
                    '<td>' + employee.bonus_salary + '</td>' +
                    '<td>' + employee.penalty_salary + '</td>' +
                    '<td>' + employee.total_salary + '</td>' +
                    '<td>' +
                      '<form>' +
                        '罚款金额<input type="number" name="fakuan">' +
                        '<button type="button" onclick="calculateTotalSalary()">确定</button>' +
                      '</form>' +
                    '</td>' +
                  '</tr>';

        $('#employee-table-body').append(row);
      }
    },
    error: function(xhr, status, error) {
      // 请求失败的回调函数
      console.error('Failed to retrieve employee data:', error);
    }
  });

  // 添加样式
  // ...

});

$(document).ready(function() {
  // 当页面加载完成后执行以下代码

  // 监听罚款提交按钮的点击事件
  $('#employee-table-body').on('click', 'button', function(event) {
    event.preventDefault();

    // 获取当前行的员工ID和罚款金额
    var row = $(this).closest('tr');
    var employeeId = row.find('td:nth-child(1)').text();
    var penaltyAmount = row.find('input[name="fakuan"]').val();

    // 发起AJAX POST请求提交罚款金额
    $.ajax({
      url: '/api/DetailInfo/penalty',  // 请求的URL，根据你的路由设置进行修改
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        "employee_id": employeeId,
        "penalty_amount": penaltyAmount
      }),
      success: function(response) {
        // 请求成功的回调函数
        // response为服务器返回的响应

        if (response.success) {
          // 罚款金额插入成功，刷新页面显示更新后的数据
          location.reload();
        } else {
          // 罚款金额插入失败，显示错误提示
          console.error(response.message);
          // 可以在页面上显示错误信息，例如使用一个警告框
          alert("罚款金额插入失败：" + response.message);
        }
      },
      error: function(xhr, status, error) {
        // 请求失败的回调函数
        console.error('Failed to post penalty salary:', error);
        // 可以在页面上显示错误信息，例如使用一个警告框
        alert("请求失败：" + error);
      }
    });
  });

  // 其他JavaScript代码...
});


$(document).ready(function() {
  // 当页面加载完成后执行以下代码

  // 监听注册按钮的点击事件
  $('input[type="submit"]').click(function(event) {
    event.preventDefault();

    // 获取注册表单中的数据
    var position = $('input[name="employeePosition"]').val();
    var employee_name = $('input[name="employeeName"]').val();
    var account = $('input[name="employeeId"]').val();
    var password = $('input[name="employeePassword"]').val();
    var base_salary = $('input[name="employeeSalary"]').val();

    // 发起AJAX POST请求注册员工账号
    $.ajax({
      url: '/api/register/employee',  // 请求的URL，根据你的路由设置进行修改
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        "position": position,
        "employee_name": employee_name,
        "account": account,
        "password": password,
        "base_salary": base_salary
      }),
      success: function(response) {
        // 请求成功的回调函数
        // response为服务器返回的响应

        if (response.hasOwnProperty('success') && response.success) {
          // 注册成功，显示成功提示
          alert("员工账号注册成功！");
          // 可以进行其他相关操作，例如清空表单数据或跳转到其他页面
          $('input[name="employeePosition"]').val("");
          $('input[name="employeeName"]').val("");
          $('input[name="employeeId"]').val("");
          $('input[name="employeePassword"]').val("");
          $('input[name="employeeSalary"]').val("");
          // 刷新页面
          location.reload();
        } else {
          // 注册失败，显示错误提示
          console.error(response.hasOwnProperty('message') ? response.message : 'Failed to register employee');
          // 可以在页面上显示错误信息，例如使用一个警告框
          alert("员工账号注册失败");
        }
      },
      error: function(xhr, status, error) {
        // 请求失败的回调函数
        console.error('Failed to register employee:', error);
        // 可以在页面上显示错误信息，例如使用一个警告框
        alert("请求失败：" + error);
      }
    });
  });

  // 监听重置按钮的点击事件
  $('input[type="reset"]').click(function(event) {
    // 清空表单数据
    $('input[name="employeePosition"]').val("");
    $('input[name="employeeName"]').val("");
    $('input[name="employeeId"]').val("");
    $('input[name="employeePassword"]').val("");
    $('input[name="employeeSalary"]').val("");
  });

  // 其他JavaScript代码...
});

$(document).ready(function() {
  // 监听查询按钮的点击事件
  $('#searchBtn').click(function(event) {
    event.preventDefault();

    // 获取输入的员工ID和查询日期
    var employeeId = $('input[name="employee"]').val();
    var date = $('#date').val();

    // 发起AJAX GET请求获取账单统计信息
    $.ajax({
      url: '/api/DetailInfo/billing',  // 请求的URL，根据你的路由设置进行修改
      method: 'GET',
      data: {
        employee_id: employeeId,
        date: date
      },
      dataType: 'json',
      success: function(response) {
        // 请求成功的回调函数
        // response为服务器返回的响应

        if (response.hasOwnProperty('success') && response.success) {
          // 获取账单统计信息
          var billingInfo = response.billing_info;

          // 更新下单次数和消费总额的输入框值
          $('input[name="times"]').val(billingInfo.order_count);
          $('input[name="money"]').val(billingInfo.total_amount);
        } else {
          // 查询失败，显示错误提示
          console.error(response.hasOwnProperty('message') ? response.message : '查询账单统计信息失败');
          // 可以在页面上显示错误信息，例如使用一个警告框
          alert("查询账单统计信息失败");
        }
      },
      error: function(xhr, status, error) {
        // 请求失败的回调函数
        console.error('查询账单统计信息失败:', error);
        // 可以在页面上显示错误信息，例如使用一个警告框
        alert("请求失败：" + error);
      }
    });
  });

  // 其他JavaScript代码...
});











