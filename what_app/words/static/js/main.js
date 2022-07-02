$(function () {

    let favorite_btn = $('.word__item-favorite button')

    favorite_btn.on('click', function(el){
        $(this).toggleClass('favorite--clicked')
        console.log(this);
    });
  
  });