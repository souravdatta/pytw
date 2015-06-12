function post_tweet() {
    var twtxt = $('#tw-text').text();
    var tweets = $('#tw-feed');

    if (twtxt == '') return;
    $.ajax(
        ('/post/' + twtxt),
        {
            success: function (d, statue, req) {
                if (d == 'success') {
                    get_tweets();
                    $('#tw-text').text('').focus();
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
}

function get_tweets() {
    var tweets = $('#tw-feed');
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
}

$(document).ready(function () {
    console.log('Ready...');
});
