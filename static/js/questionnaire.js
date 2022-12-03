$('.answer').click(function (e) { 
    let radio = $(this).find('input')
    radio.prop("checked", true);
    $(this).siblings().removeClass('selected')
    $(this).addClass('selected')
});

var lastPage = 1
var pageNumber = 0

pageNumber = $('.questions-wrapper').length


$('.page').click(function (e) { 
    let pageClass = $(this).attr('class').split(' ')[1]
    currentPage = pageClass.split('-')[1]
    if(lastPage != currentPage){
        $('.page-' + lastPage).removeClass('selected-page')
        $('.page-' + currentPage).addClass('selected-page')
        $('[index=' + currentPage + ']').removeClass('hidden')
        $('[index=' + lastPage + ']').addClass('hidden')
        lastPage = currentPage
    }

    $('.progress').width(currentPage / pageNumber * 100 + '%');
});