$(function () {

    const forms = document.querySelectorAll('.word__item-form')

    forms.forEach(function (el) {
        $(el).on('submit', function (el) {
            el.preventDefault()

            let favorite_btn = $(this).find('.word__item-favorite').find('button')
            const posting = $.get($(this).attr('action'));
            posting.done(function (data) {

                $(favorite_btn).toggleClass('favorite--clicked')
            });
            posting.fail(function (data) {

            });

        })
    })


});