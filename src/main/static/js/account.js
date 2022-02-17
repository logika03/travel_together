document.getElementById('avatar').onchange = function () {
    // document.getElementById('img_label').innerHTML = this.files[0].name;
    document.getElementById('btn-avatar').removeAttribute('disabled')
    return this;
};

$('#article-link').on('click', function () {
    $.ajax({
        url: '../../blog/last_articles/',
        type: 'GET',
        beforeSend: function () {
            $('#article-content').empty();
        },
        success: function (responce) {
            $('#article-content').append(responce);
        },
        error: function () {
            alert('Error!');
        }
    });
});

let links = document.querySelectorAll('.article-link');
links.forEach((elem) => {
    elem.addEventListener('click', () => {
        const url_template = `../../blog/${elem.id}/`;
        const content_id = `#${elem.id}-content`;
        $.ajax({
            url: url_template,
            type: 'GET',
            beforeSend: function () {
                $(content_id).empty();
            },
            success: function (response) {
                $(content_id).append(response);
            },
            error: function () {
                alert('Error!');
            }
        });
    })
});