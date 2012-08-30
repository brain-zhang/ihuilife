/**
 * @author Administrator
 */

$(document).ready(function() {
    $('.taobao_shopping_btn').click(function() {
        $.get('/catfeeds/admin/taobaoshopping', {
            'num_iid' : $(this).parent().find(".span4").attr('value')
        }, function(data) {
            alert(data);
        })
        return false;
    });

    $('.taobaoke_shopping_btn').click(function() {
        $.get('/catfeeds/admin/taobaokeshopping', {
            'num_iid' : $(this).attr('num_iid')
        }, function(data) {
            alert(data);
        })
        return false;
    });

    $('.carousel').carousel({
        interval : 2000
    });

    //商品图片中的说明文字渐现效果
    $('.topic-item').mouseenter(function() {
        $(this).find('p').animate({
            height : '60'
        }, 300);
        return false;
    });

    //商品图片中的说明文字渐隐效果
    $('.topic-item').mouseleave(function() {
        $(this).find('p').animate({
            height : '0'
        }, 300);
        return false;
    });
});
