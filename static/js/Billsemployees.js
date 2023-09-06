document.addEventListener("DOMContentLoaded", function() {
  // 发起AJAX GET请求获取账单数据
  $.ajax({
    url: '/api/employees/orders',
    type: 'GET',
    dataType: 'json',
    success: function(dataList) {
      // 获取待提交订单表格的tbody元素
      var pendingTableBody = $("#pending_orders_table tbody");

      dataList.forEach(function(data) {
        // 创建一个新的表格行
        var newRow = $("<tr>");

        // 添加订单属性的表格单元格
        newRow.append($("<td>").text(data['order_id']));
        newRow.append($("<td>").text(data['current_time']));
        newRow.append($("<td>").text(data['employee_id']));
        newRow.append($("<td>").text(data['customer_id']));
        newRow.append($("<td>").text(data['total_price']));
        newRow.append($("<td>").text(data['customer_review']));
        newRow.append($("<td>").html('<button class="editButton">新增订单</button>'));

        // 将新行添加到待提交订单表格的tbody中
        pendingTableBody.append(newRow);
      });
    },
    error: function(xhr, status, error) {
      // 请求失败的回调函数
      console.error('Failed to retrieve billing data:', error);
      alert("请求失败：" + error);
    }
  });

  // 添加事件监听器
  $(document).on('click', '.editButton', function() {
    openPopup(); // 显示弹出窗口
    var orderId = $(this).closest('tr').find('td:eq(0)').text(); // 获取订单ID
    var orderDate = $(this).closest('tr').find('td:eq(1)').text(); // 获取订单时间
    var orderEmployee = $(this).closest('tr').find('td:eq(2)').text(); // 获取接单员工
    var orderCustomer = $(this).closest('tr').find('td:eq(3)').text(); // 获取顾客号
    var orderAmount = $(this).closest('tr').find('td:eq(4)').text(); // 获取账单金额
    var orderFeedback = $(this).closest('tr').find('td:eq(5)').text(); // 获取评价

    // 填充数据到输入字段中
    document.getElementById("orderId").value = orderId;
    document.getElementById("orderDate").value = orderDate;
    document.getElementById("orderEmployee").value = orderEmployee;
    document.getElementById("orderCustomer").value = orderCustomer;
    document.getElementById("orderAmount").value = orderAmount;
    document.getElementById("orderFeedback").value = orderFeedback;
  });



 // 获取元素的引用
  const popup = document.getElementById("popup");
  const saveOrderButton = document.getElementById("saveOrderButton");
  const submittedTable = document.getElementById("submitted_orders_table");

    // 打开弹出窗口的函数
  function openPopup() {
    popup.classList.add("active");
  }

  // 关闭弹出窗口的函数
  function closePopup() {
    popup.classList.remove("active");
  }

  function extractYearFromOrderDate(orderDate) {
    return parseInt(orderDate.split("年")[0]);
  }

  function extractMonthFromOrderDate(orderDate) {
    return parseInt(orderDate.split("年")[1].split("月")[0]);
  }

  function extractDayFromOrderDate(orderDate) {
    return parseInt(orderDate.split("月")[1].split("日")[0]);
  }

    // 保存新订单的函数
  function saveOrder() {
    // Get input values
    const orderDate = document.getElementById("orderDate").value;
    const orderEmployee = document.getElementById("orderEmployee").value;
    const orderCustomer = document.getElementById("orderCustomer").value;
    const orderAmount = parseFloat(document.getElementById("orderAmount").value);
    const orderFeedback = document.getElementById("orderFeedback").value;

    // Convert date string to date object
    const year = extractYearFromOrderDate(orderDate);
    const month = extractMonthFromOrderDate(orderDate);
    const day = extractDayFromOrderDate(orderDate);

    const orderData = {
      year: year,
      month: month,
      day: day,
      customer_id: orderCustomer,
      employee_id: orderEmployee,
      totalMY: orderAmount,
      feedback: orderFeedback
    };

     // 发送订单数据到后端
    $.ajax({
      url: '/api/ShowBills',
      type: 'POST',
      data: JSON.stringify(orderData),
      dataType: 'json',
      contentType: 'application/json',
      success: function(response) {
        if (response.success) {
          alert("数据插入成功！");
          location.reload();
        } else {
          alert("数据插入失败：" + response.message);
        }
      },
      error: function(xhr, status, error) {
        console.error('Failed to insert data:', error);
        alert("请求失败：" + error);
      }
    });


    closePopup();
  }

  // 保存按钮的事件监听器
  saveOrderButton.addEventListener("click", saveOrder);
});


document.addEventListener("DOMContentLoaded", function() {
  // 发起AJAX GET请求获取账单数据
  $.ajax({
    url: '/api/ShowBills',
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      // 获取已提交订单表格的tbody元素
      var submittedTableBody = $("#submitted_orders_table tbody");

      // 对每一条账单数据进行处理
      data.forEach(function(bill) {
        // 创建一个新的表格行
        var newRow = $("<tr>");

        // 添加订单属性的表格单元格
        newRow.append($("<td>").text(bill['bill_id']));
        newRow.append($("<td>").text(bill['bill_time']));
        newRow.append($("<td>").text(bill['employee_id']));
        newRow.append($("<td>").text(bill['customer_id']));
        newRow.append($("<td>").text(bill['amount']));
        newRow.append($("<td>").text(bill['customer_review']));

        // 将新行添加到已提交订单表格的tbody中
        submittedTableBody.append(newRow);
      });
    },
    error: function(xhr, status, error) {
      // 请求失败的回调函数
      console.error('Failed to retrieve billing data:', error);
      alert("请求失败：" + error);
    }
  });
});
