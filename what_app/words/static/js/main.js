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
    all_likes_btn.forEach(function (btn) {
        $(btn).on('click', function (el) {
            el.preventDefault()
            postingMarks(this, 'word__item-markslike--clicked')
        })
    })


    const all_dislikes_btn = document.querySelectorAll('.word__item-marksdislike')
    all_dislikes_btn.forEach(function (btn) {
        $(btn).on('click', function (el) {
            el.preventDefault()
            postingMarks(this, 'word__item-marksdislike--clicked')
        })
    })


    function postingMarks(el, selector) {
        const posting = $.get($(el).attr('href'));
        posting.done(function (data) {
            // Запихнуть в условие если нет лайка
            if ($(el).attr('class').indexOf(selector) !== -1) {
                let text = Number($(el).find('span').text()) - 1
                $(el).find('span').text(text)
            } else {
                let nearby_btn = $(el).siblings('a')[0];
                let text_el = Number($(el).find('span').text())
                let text_nearby_btn = Number($(nearby_btn).find('span').text())
                if ($(nearby_btn).attr('class').indexOf('word__item-markslike--clicked') !== -1) {
                    text_nearby_btn -= 1
                    $(nearby_btn).find('span').text(text_nearby_btn)
                    $(nearby_btn).removeClass('word__item-markslike--clicked')
                    text_el += 1
                    $(el).find('span').text(text_el)
                } else if ($(nearby_btn).attr('class').indexOf('word__item-marksdislike--clicked') !== -1) {
                    text_nearby_btn -= 1
                    $(nearby_btn).find('span').text(text_nearby_btn)
                    $(nearby_btn).removeClass('word__item-marksdislike--clicked')
                    text_el += 1
                    $(el).find('span').text(text_el)
                } else {
                    text_el += 1
                    $(el).find('span').text(text_el)
                }
            }


            // if ($(el).attr('class').indexOf(selector) !== -1) {
            //     let text = Number($(el).find('span').text()) - 1
            //     $(el).find('span').text(text)
            // } else {
            //     let text = Number($(el).find('span').text()) + 1
            //     $(el).find('span').text(text)
            // }
            $(el).toggleClass(selector)
        });
        posting.fail(function (data) {

        });
    }

    $('.change-name__magnific-popup').magnificPopup({
        type: 'inline',
        midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
    });

    $('.complain__form-bnt').magnificPopup({
        type: 'inline',
        midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
    });

    let popup_yes = document.querySelector('.popup__bnt-yes')
    $(popup_yes).on('click', function (el) {
        let form = $('.complain__form-form')[0]
        form.submit()
        $.magnificPopup.close();
    })

    let popup_no = document.querySelector('.popup__bnt-no')
    $(popup_no).on('click', function (el) {
        $.magnificPopup.close();
    })
});