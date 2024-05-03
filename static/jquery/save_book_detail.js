$(document).on('click', '#submit-btn', function (event) {
    event.preventDefault();  // 阻止默认的链接跳转行为
    $.ajax({
        url: saveUrl,  // 假设你有一个对应的视图函数来处理还书请求
        type: 'POST',
        data: $('#book_datail_form').serialize(), // 序列化表单数据
        success: function (response) {
            if (response.success) {
                alert('图书保存成功！');
            } else {
                alert('图书保存失败，请联系管理员。');
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('AJAX请求失败:', textStatus, ', 错误:', errorThrown);
        }
    });
});