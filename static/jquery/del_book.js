$(document).on('click', '.return-book', function(event) {
    event.preventDefault();  // 阻止默认的链接跳转行为

    var bookRow = $(this).closest('.book-detail');  // 获取当前a标签所在的.book-detail div .是类，#是id

    var bookId = $(this).data('book-id');
    var libraryCardNo = $('#libraryCardNo').val();

    $.ajax({
        url: returnBookUrl,  // 假设你有一个对应的视图函数来处理还书请求
        type: 'POST',
        data: {bookId: bookId, libraryCardNo: libraryCardNo},
        success: function (response) {
            if (response.success) {
                bookRow.slideUp(300, function() { bookRow.remove(); });  // 使用slideUp动画效果后移除（可选）
            } else {
                alert('图书归还失败，请稍后再试或联系管理员。');
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('AJAX请求失败:', textStatus, ', 错误:', errorThrown);
        }
    });
});
