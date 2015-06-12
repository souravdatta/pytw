function post_tweet() {
    var twtxt = $('#tw-text').text();
    var tweets = $('#tw-feed');

    if (twtxt == '') return;
    $.ajax(
        ('/post/' + twtxt),
        {
            success: function (d, statue, req) {
                if (d == 'success') {
                    var div = $(document.createElement('div'));
                    div.addClass('tweet');
                    tweets.prepend(div);
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

$(document).ready(function () {
    console.log('Ready...');
});
