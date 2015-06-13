function post_tweet() {
    var twtxt = $('#tw-text').text();
    var tweets = $('#tw-feed');
    var count = $('#tw-count');
    var loader = $('.loader');

    if (twtxt == '') return;

    if (twtxt.length > 140) {
        twtxt = twtxt.substring(0, 138) + '...';
    }

    loader.removeClass('hide');
    loader.addClass('show');
    $.ajax(
        ('/post/' + twtxt),
        {
            success: function (d, statue, req) {
                if (d == 'success') {
                    get_tweets();
                }
                else {
                    alert('Could not complete request, something went wrong!');
                }
            },
            error: function () {
                alert('Could not complete request, something went wrong!');
            }
        }
    );
    loader.removeClass('show');
    loader.addClass('hide');
    $('#tw-text').text('').focus();
    count.text(140);
}

function get_tweets() {
    var tweets = $('#tw-feed');
    var loader = $('.loader');

    loader.removeClass('hide');
    loader.addClass('show');
    $.ajax('/timeline',
           {
                success: function (d, status, req) {
                    var json = JSON.parse(d);
                    if ((json != null) && (json.length > 0)) {
                        tweets.empty();
                        for (var i = 0; i < json.length; i++) {
                            var div = $(document.createElement('div'));
                            div.text(json[i]);
                            div.addClass('tweet');
                            tweets.append(div);
                        }
                    }
                },
                error: function () {
                    alert('Could not refresh tweets, something went wrong!');
                }
           }
    );
    loader.removeClass('show');
    loader.addClass('hide');
}

function check_limit() {
    var twbox = $('#tw-text');
    var text = twbox.text();
    var count = $('#tw-count');

    if (text == '') return;

    var limit = 140 - text.length;
    count.text(limit);

    if (limit > 20) {
        twbox.removeClass('warning');
        twbox.removeClass('error');
    }
    else if ((limit > 0) && (limit <= 20))  {
        twbox.removeClass('error');
        twbox.addClass('warning');
    }
    else if (limit <= 0) {
        twbox.removeClass('warning');
        twbox.addClass('error');
    }
}

$(document).ready(function () {
    console.log('Ready...');
});
