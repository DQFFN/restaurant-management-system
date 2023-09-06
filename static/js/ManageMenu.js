
function getStatusText(status) {
    // 根据状态值返回对应的文本
    if (status === '0') {
        return '售空';
    } else if (status === '1') {
        return '在售';
    } else {
        return '未知状态';
    }
}

function loadRecipes() {
    // 发送获取菜单数据的请求
    $.ajax({
        url: '/api/recipes',
        method: 'GET',
        success: function(menuData) {
            var tbody = $('tbody');
            tbody.empty(); // 清空表格内容

            // 遍历菜单数据，生成表格行
            $.each(menuData, function(index, item) {
                var row = $('<tr>');
                row.append($('<td>').text(item[0])); // 序号
                row.append($('<td>').text(item[1])); // 菜品名称
                row.append($('<td>').text(getStatusText(item[2]))); // 状态
                row.append($('<td>').text(item[3])); // 类型
                row.append($('<td>').text(item[4])); // 价格
                var deleteButton = $('<button>').text('删除').attr('onclick', 'deleteRecipe(' + item[0] + ')');
                var editButton = $('<button>').text('修改').attr('onclick', 'showEditForm(' + item[0] + ')');
                row.append($('<td>').append(deleteButton));
                row.append($('<td>').append(editButton));
                tbody.append(row);
            });
        },
        error: function(error) {
            console.log('获取菜单数据失败');
        }
    });
}

function addRecipe() {
    // 获取表单输入的值
    var name = $('#name').val();
    var status = $('#status').val();
    var type = $('#type').val();
    var price = $('#price').val();

    // 发送添加菜谱请求
    $.ajax({
        url: '/api/recipes',
        method: 'POST',
        data: {
            name: name,
            status: status,
            type: type,
            price: price
        },
        success: function(response) {
            if (response.success) {
                console.log('菜谱添加成功');
                alert(response.message);
                loadRecipes();
            } else {
                console.log('菜谱添加失败');
                alert(response.message);
            }
        },
        error: function(error) {
            console.log('菜谱添加失败');
            alert('菜谱添加失败，请重试');
        }
    });
}

function deleteRecipe(recipeId) {
    if (window.confirm('您确定要删除该菜谱吗？')) {
        // 发送删除菜谱请求
        $.ajax({
            url: '/api/recipes/' + recipeId,
            method: 'DELETE',
            success: function(response) {
                if (response.success) {
                    console.log('菜谱删除成功');
                    alert(response.message);
                    loadRecipes();
                } else {
                    console.log('菜谱删除失败');
                    alert(response.message);
                }
            },
            error: function(error) {
                console.log('菜谱删除失败');
                alert('菜谱删除失败，请重试');
            }
        });
    }
}

function showEditForm(recipeId) {
    // 获取菜谱对应的行
    var row = $('tr[data-id="' + recipeId + '"]');

    // 获取菜谱的各个字段值
    var dishName = row.find('td:nth-child(2)').text();
    var dishStatus = row.find('td:nth-child(3)').text();
    var recipeType = row.find('td:nth-child(4)').text();
    var price = row.find('td:nth-child(5)').text();

    // 填充修改窗口中的表单数据
    $('#editId').val(recipeId);
    $('#editName').val(dishName);
    $('#editStatus').val(dishStatus);
    $('#editType').val(recipeType);
    $('#editPrice').val(price);

    // 显示修改窗口
    $('#editModal').css('display', 'flex');
}

function hideEditForm() {
    // 隐藏修改窗口
    $('#editModal').hide();
}

function updateRecipe() {
    // 获取修改后的数据
    var recipeId = $('#editId').val();
    var name = $('#editName').val();
    var status = $('#editStatus').val();
    var type = $('#editType').val();
    var price = $('#editPrice').val();

    // 发送更新菜谱请求
    $.ajax({
        url: '/api/recipes/' + recipeId,
        method: 'PUT',
        data: {
            name: name,
            status: status,
            type: type,
            price: price
        },
        success: function(response) {
            if (response.success) {
                console.log('菜谱更新成功');
                alert(response.message);
                loadRecipes();
                hideEditForm();
            } else {
                console.log('菜谱更新失败');
                alert(response.message);
            }
        },
        error: function(error) {
            console.log('菜谱更新失败');
            alert('菜谱更新失败，请重试');
        }
    });
}

function resetForm() {
    document.getElementById("addRecipeForm").reset();
}

$(document).ready(function() {
    // 页面加载时加载菜谱数据
    loadRecipes();
});