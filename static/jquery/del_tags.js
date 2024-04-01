$(document).on('click', '.tag-id', function(event) {
    event.preventDefault();  // 阻止默认的链接跳转行为

    var bookRow = $(this)  // 获取当前a标签所在的.book-detail div .是类，#是id

    var tag_id = $(this).data('tag-id');
    var book_id = $('#bookID').val();
    $.ajax({
        url: delTagsUrl,
        type: 'GET',
        data: {tag_id: tag_id,book_id: book_id},
        success: function (response) {
            if (response.success) {
                alert('图书标签删除成功！');
                // 隐藏或删除当前书籍记录
                bookRow.slideUp(300, function() { bookRow.remove(); });  // 使用slideUp动画效果后移除（可选）
                // 或者直接删除（无动画效果）
                // bookRow.remove();
            } else {
                alert('图书标签删除失败！');
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('AJAX请求失败:', textStatus, ', 错误:', errorThrown);
        }
    });
});
