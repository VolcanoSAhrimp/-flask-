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
                            '<div class="tag black-border">' + tag.name + '</div>'
                    });
                    $('#tags').css('display', 'block');
// 在循环结束后添加“添加标签”按钮
//                     booksListHtml += '<div class="tag black-border" id="add">添加标签</div>';
                    // 将生成的 HTML 插入到页面中显示已借图书列表的位置
                    $('#tags').html(booksListHtml);
                } else {
                    $('#tags').css('display', 'none');
                    $('#bookTitle').val(response.books)
                    // alert('未找到图书信息');
                    // $('#bookID').val('');
                    // $('#bookTitle').val('');
                    $('#tags').html("");

                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error('AJAX请求失败:', textStatus, ', 错误:', errorThrown);
            }
        });
    });
});
// $(document).onclick(function () {
//     $('#tagSubmit').on('onclick', function () {
//         var bookID = $(this).val();
//         // 使用AJAX向后端发送请求获取用户名
//         $.ajax({
//             url: addTagsUrl,  // 假设你有一个对应的视图函数来处理这个请求
//             type: 'POST',
//             data: {bookID: bookID},
//             success: function (response) {
//                 if (response.books && response.tags.length > 0) {
//                     $('#bookTitle').val(response.books)
//                     var booksListHtml = '';
//                     $.each(response.tags, function (index, tag) {
//                         booksListHtml +=
//                             '<div class="tag black-border">' + tag.name + '</div>'
//                     });
//
// // 在循环结束后添加“添加标签”按钮
//                     booksListHtml += '<div class="tag black-border" onclick="addtag">添加标签</div>';
//                     // 将生成的 HTML 插入到页面中显示已借图书列表的位置
//                     $('#tags').html(booksListHtml);
//                 } else {
//                     $('#bookTitle').val(response.books)
//                     alert('未找到图息');
//                     // $('#bookID').val('');
//                     // $('#bookTitle').val('');
//                     $('#tags').html("");
//
//                 }
//             },
//             error: function (jqXHR, textStatus, errorThrown) {
//                 console.error('AJAX请求失败:', textStatus, ', 错误:', errorThrown);
//             }
//         });
//     });
// });