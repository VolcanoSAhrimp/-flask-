$(document).on('click', '.return-book', function(event) {
    event.preventDefault();  // 阻止默认的链接跳转行为

    var bookId = $(this).data('book-id');
    var libraryCardNo = $('#libraryCardNo').val();

    $.ajax({
        url: returnBookUrl,  // 假设你有一个对应的视图函数来处理还书请求
        type: 'POST',
        data: {bookId: bookId, libraryCardNo: libraryCardNo},
        success: function (response) {
            if (response.success) {
                alert('图书已成功归还！');
                // 可能还需要在这里更新页面上的已借图书列表
                window.location.reload(true);
            } else {
                alert('图书归还失败，请稍后再试或联系管理员。');
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('AJAX请求失败:', textStatus, ', 错误:', errorThrown);
        }
    });
});
