$(function () {
    var num_items = 9;
    var loaded_count = 9;
    $('#load_more').click(function () {
        $.ajax({
            url: '/load_more/',
            data: {
                'num_items': num_items,
                'loaded_count': loaded_count
            },
            success: function (response) {
                var pages = response.data;
                if (pages.length > 0) {
                    var html = '';
                    for (var i = 0; i < pages.length; i++) {
                        var page = pages[i];
                        html += '<div class="card bg-base-100 shadow-xl border-2">';
                        html += '<figure class="transform transition duration-1000 ease-in delay-150">';
                        html += '<a href="/product/' + page.t_id + '/" target="_blank"><img src="' + page.image + '" alt="" class="cursor-pointer w-full"/></a>';
                        html += '</figure>';
                        html += '<div class="card-body">';
                        html += '<h2 class="card-title">';
                        html += '<a href="' + page.t_id + '" target="_blank">' + page.name + '</a></h2>';
                        html += '<p>' + page.price + '</p>';
                        html += '<div class="card-actions justify-start pt-4">';
                        html += '</div></div>';
                        html += '<div class="flex justify-between py-4 px-3">';
                        html += '<div class="w-full flex justify-center"><a class="btn btn-info w-36 text-white hover:bg-blue-400" href="/product/' + page.t_id + '/" target="_blank"><span>Customized</span></a></div></div></div>';
                    }
                    $('#load_more').before(html);
                    loaded_count += num_items;
                    num_items = 9;
                } else {
                    $('#load_more').hide();
                }
            },
            error: function () {
                alert('加载失败，请稍后再试。');
            },
        });
    });
});
