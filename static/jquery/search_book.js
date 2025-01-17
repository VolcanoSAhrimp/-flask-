$(document).ready(function () {
    $('#libraryCardNo').on('blur', function () {
        var libraryCardNo = $(this).val();
        $.ajax({
            url: searchBookUrl,  // 假设你有一个对应的视图函数来处理这个请求
            type: 'POST',
            data: {libraryCardNo: libraryCardNo},
            success: function (response) {
                if (response.books && response.books.length > 0) {
                    var booksListHtml = '';
                    $.each(response.books, function (index, book) {
                        booksListHtml += '<div class="book-detail">' +
                            '<div>图书名称：' + book.title + '</div>' +
                            '<div><a href="#" class="return-book" data-book-id="' + book.book_id + '">返还</a></div>' +
                            '</div>';
                    });
                    $('#borrowed-books-list').html(booksListHtml);
                } else {
                    alert('未找到图书信息');
                    $('#libraryCardNo').val('');
                    $('#username').val('');
                    $('#borrowed-books-list').html("");

                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error('AJAX请求失败:', textStatus, ', 错误:', errorThrown);
            }
        });
    });
});