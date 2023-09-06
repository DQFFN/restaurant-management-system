function getEmployeeInfo() {
  $.ajax({
    url: '/api/employees/info',
    method: 'GET',
    success: function(response) {
      if (response.success) {
        var employeeInfo = response.data;
        $('#name').val(employeeInfo.employee_name);
        $('#position').val(employeeInfo.position);
        $('#account').val(employeeInfo.account);

        // 设置工资明细数据
        $('#base_salary').val(employeeInfo.base_salary);
        $('#completed_count').val(employeeInfo.completed_count);
        $('#bonus_salary').val(employeeInfo.bonus_salary);
        $('#penalty_salary').val(employeeInfo.penalty_salary);
        $('#total_salary').val(employeeInfo.total_salary);
      } else {
        console.error(response.message);
      }
    },
    error: function(xhr, status, error) {
      console.error('Failed to get employee information:', error);
    }
  });
}

$(document).ready(function() {
  getEmployeeInfo(); // 在页面加载完成后调用获取员工信息的函数

  $('#updateForm').submit(function(event) {
    event.preventDefault();

    var position = $('#post').val();
    var employeeName = $('#name').val();
    var account = $('#account').val();
    var oldPassword = $('#old_password').val();
    var newPassword = $('#new_password').val();
    var confirmPassword = $('#confirm_password').val();

    if (newPassword !== confirmPassword) {
      alert('新密码和确认密码不匹配');
      return;
    }

    $.ajax({
      url: '/api/register/updateemployee',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        position: position,
        employee_name: employeeName,
        account: account,
        password: newPassword,
        old_password: oldPassword
      }),
      success: function(response) {
        if (response.success) {
          alert('更新员工信息成功！');
          $('form')[0].reset();
        } else {
          alert(response.message);
        }
      },
      error: function(xhr, status, error) {
        console.error('Failed to update employee information:', error);
        alert('更新员工信息请求失败：' + error);
      }
    });
  });
});
