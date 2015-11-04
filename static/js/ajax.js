$(document).ready(function(){

    $.cookie('watched', 'no');
    $.cookie('n', 0);

    setTimeout(function (){

        function load_post() {
            
            var number1 = +$('p.number:first').text();

            $.ajax({
                type : "GET",
                url:"ajax_request_list",
                dataType:"json",
                success:function(data){
                    
                    var all_requests = $('#all_requests');
                    all_requests.empty();

                    $.each(data, function(key, value){
                        var html = '<tr>';
                        html += '<td align="center" valign="middle"><p>[' + value.req_date + ']</p><p class="number">' + value.req_id + '</p></td>';
                        html += '<td align="center" valign="middle"><p>' + value.req_method + '</p></td>';
                        html += '<td align="center" valign="middle"><p>' + value.req_path + '</p></td>';
                        html += '<td align="center" valign="middle"><p>' + value.req_priority + '</p></td>';
                        html += '<td align="center" valign="middle"><p><a href="../edit_request/' + value.req_id + '">Edit</a></p></td>';
                        html += '</tr>';
                        all_requests.append(html);
                    });

                    var watched = $.cookie('watched');
                    var number2 = +$('p.number:first').text();
                    var n = number2 - number1;
                    var past_n = +$.cookie('n');

                    if (n > 0 || past_n > 0) {
                        
                        if (watched === 'no') {
                            n += past_n;
                        } 
                        $('title').text(n + ' new request(s)');
                        $.cookie('n', n);
                        $.cookie('watched', 'no')
                    } else {
                        $('title').text('Last 10 requests');
                    }

                }
            });
        
            $('html').click(function() {
                if ( $(window).height() === $(document).height()) {
                        $.cookie('watched', 'yes');
                        $.cookie('n', 0);
                        $('title').text('Last 10 requests');
                } 
            });

            $(window).scroll(function() {
                if($(window).scrollTop() + $(window).height() >= $(document).height() - 50 ) {
                    $.cookie('watched', 'yes');
                    $.cookie('n', 0);
                    $('title').text('Last 10 requests');         
                }  
            });
        }
        
        load_post();

        setInterval(load_post, 5000);
    },2000);

});
