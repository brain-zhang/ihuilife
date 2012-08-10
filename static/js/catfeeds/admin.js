/**
 * @author Administrator
 */

$(document).ready(function(){
    $('.btn').click(function(){
       $(this).button('loading');
       $.get('shopping', {'num_iid':$(this).attr('num_iid')}, function(data){alert(data);})
    });
});
