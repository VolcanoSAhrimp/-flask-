// 获取 ".form-space" 的宽度并设置给 "#addbook"
function syncWidth() {
  var formSpaceWidth = $('.form-space').width();
   $('.green-book').css('width', 'auto');
  $('.green-book').width(formSpaceWidth);
  // alert(formSpaceWidth)
}

// 在窗口大小改变时同步宽度
// $(window).on('resize', syncWidth);


// 页面加载完成后首次同步宽度
$(document).ready(syncWidth);