$(document).ready(function() {
    $('#libraryCardNo').on('blur', function() {
        var libraryCardNo = $(this).val();

        // 使用AJAX向后端发送请求获取用户名
        $.ajax({
            url: searchNameUrl,  // 假设你有一个对应的视图函数来处理这个请求
            // url: '/admin/search_name',
            type: 'POST',
            data: { libraryCardNo: libraryCardNo },
            success: function(response) {
                if (response.username) {
                    $('#username').val(response.username);
                } else {
                    $('#libraryCardNo').val('');
                    alert('未找到该图书馆卡号对应的用户名');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('AJAX请求失败:', textStatus, ', 错误:', errorThrown);
            }
        });
    });
     // 当书ID输入框失去焦点时，获取书名
    $('#bookID').on('blur', function() {
        var bookID = $(this).val();

        $.ajax({
            url: searchNameUrl,  // 假设这是获取书名的后端路由地址
            type: 'POST',
            data: { bookID: bookID },
            success: function(response) {
                if (response.bookTitle) {
                    $('#bookTitle').val(response.bookTitle);
                } else {
                    $('#bookID').val('');
                    alert('未找到该书ID对应的书名');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('AJAX请求失败:', textStatus, ', 错误:', errorThrown);
            }
        });
    });
});