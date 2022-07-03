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

    const all_likes_btn = document.querySelectorAll('.word__item-markslike')
    console.log(all_likes_btn)
    all_likes_btn.forEach(function (btn) {
        $(btn).on('click', function (el) {
            console.log(this)
            el.preventDefault()
            postingMarks(this, 'word__item-markslike--clicked')
            $('.word__item-marksdislike').removeClass('word__item-marksdislike--clicked')
        })
    })




    const all_dislikes_btn = document.querySelectorAll('.word__item-marksdislike')
    all_dislikes_btn.forEach(function (btn) {
        $(btn).on('click', function (el) {
            console.log(this)
            el.preventDefault()
            postingMarks(this, 'word__item-marksdislike--clicked')
            $('.word__item-markslike').removeClass('word__item-markslike--clicked')
        })
    })



    function postingMarks(el, selector) {
        const posting = $.get($(el).attr('href'));
        posting.done(function (data) {
            $(el).toggleClass(selector)
        });
        posting.fail(function (data) {

        });
    }


});