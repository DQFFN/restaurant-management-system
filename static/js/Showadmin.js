$(document).ready(function() {
	// 当页面加载完成后执行以下代码

	// 监听表单的提交事件
	$('form').submit(function(event) {
		event.preventDefault();

		// 获取表单中的数据
		var name = $('#name').val();
		var position = $('#post').val();
		var account = $('#account').val();
		var oldPassword = $('#old_password').val();
		var newPassword = $('#new_password').val();
		var confirmPassword = $('#confirm_password').val();

		// 验证新密码和确认密码是否相符
		if (newPassword !== confirmPassword) {
			alert("确认密码和新密码不相符");
			return;
		}

		// 发起 AJAX POST 请求更新员工信息
		$.ajax({
			url: '/api/register/updateemployee',  // 请求的URL，根据你的路由设置进行修改
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				"employee_name": name,
				"position": position,
				"account": account,
				"password": newPassword,
				"old_password": oldPassword
			}),
			success: function(response) {
				// 请求成功的回调函数
				// response 为服务器返回的响应

				if (response.hasOwnProperty('success') && response.success) {
					// 更新成功，显示成功提示
					alert("员工信息修改成功！");
					// 可以进行其他相关操作，例如清空表单数据或刷新页面
					$('#name').val("");
					$('#post').val("");
					$('#account').val("");
					$('#old_password').val("");
					$('#new_password').val("");
					$('#confirm_password').val("");
				} else {
					// 更新失败，显示错误提示
					console.error(response.hasOwnProperty('message') ? response.message : 'Failed to update employee information');
					// 可以在页面上显示错误信息，例如使用一个警告框
					alert("员工信息修改失败");
				}
			},
			error: function(xhr, status, error) {
				// 请求失败的回调函数
				console.error('Failed to update employee information:', error);
				// 可以在页面上显示错误信息，例如使用一个警告框
				alert("请求失败：" + error);
			}
		});
	});

	// 其他 JavaScript 代码...
});
