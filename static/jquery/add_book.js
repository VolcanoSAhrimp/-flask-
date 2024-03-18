$(document).on('click', '#bookSubmit', function(event) {
    event.preventDefault();  // 阻止默认的链接跳转行为

    var Name = $('#Name').val();
    var Author = $('#Author').val();
    var Publisher = $('#Publisher').val();
    var Synopsis = $('#Synopsis').val();
    var Price = $('#Price').val();

    $.ajax({
        url: addNameUrl,  // 假设你有一个对应的视图函数来处理还书请求
        type: 'POST',
        data: {Name: Name, Author: Author, Publisher: Publisher, Synopsis: Synopsis, Price: Price},
        success: function (response) {
            if (response.success) {
                alert('图书添加成功！');
                window.location.reload(true);
            } else {
                alert('图书添加失败。');
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('AJAX请求失败:', textStatus, ', 错误:', errorThrown);
        }
    });
});