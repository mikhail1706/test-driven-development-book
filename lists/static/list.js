window.Superlists = {};
window.Superlists.updateItems = function (url) {
    $.get(url).done(function (response) {
        var rows = '';
        for (var i = 0; i < response.items.length; i++) {
            var item = response.items[i];
            rows += '\n<tr><td>' + (i + 1) + ': ' + item.text + '</td></tr>';
        }
        $('#id_list_table').html(rows);
    });
};

window.Superlists.initialize = function (params) {
    $('input[name="text"]').on('keypress', function () {
        $('.has-error').hide();
    });

    if (params) {
        window.Superlists.updateItems(params.listApiUrl);
        var form = $('#id_item_form');
        form.on('submit', function (event) {
            event.preventDefault();
            $.post(params.itemsApiUrl, {
                'list': params.listId,
                'text': form.find('input[name=”text”]').val(),
                'csrfmiddlewaretoken': form.find('input[name="csrfmiddlewaretoken"]').val(),
            }).done(function () {
                window.Superlists.updateItems(params.listApiUrl);
            });
            ;
        });
    }
};







