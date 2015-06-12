function post_tweet() {
    var twtxt = $('#tw-text').text();
    if (twtxt == '') return;
    $.ajax(
        ('/post/' + twtxt),
        {
            success: function (d, statue, req) {
                alert(d);
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
