$(document).ready(function () {
    $('#bookID').on('blur', function () {
        var bookID = $(this).val();
        // 使用AJAX向后端发送请求获取用户名
        $.ajax({
            url: searchTagsUrl,  // 假设你有一个对应的视图函数来处理这个请求
            type: 'POST',
            data: {bookID: bookID},
            success: function (response) {
                if (response.books && response.tags.length > 0) {
                    $('#bookTitle').val(response.books)
                    var booksListHtml = '';
                    $.each(response.tags, function (index, tag) {
                        booksListHtml +=
                            '<a href="#" class="tag-id" data-tag-id="' + tag.id + '"><div class="tag black-border">'+ tag.name + '</div></a>'
                    });
                    $('#tags').css('display', 'block');
                    $('#tags').html(booksListHtml);
                } else {
                    $('#tags').css('display', 'none');
                    $('#bookTitle').val(response.books)
                    $('#tags').html("");
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error('AJAX请求失败:', textStatus, ', 错误:', errorThrown);
            }
        });
    });
});
