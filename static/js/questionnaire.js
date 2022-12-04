var lastPage = 1
var pageNumber = 0

pageNumber = $('form').children().length - 1
currentPage = 1
lastPage = 1

$('.answer').click(function (e) { 
    let radio = $(this).find('input')
    radio.prop("checked", true);
    $(this).siblings().removeClass('selected')
    $(this).addClass('selected')
});

$(document).ready(function () {
    $('.page-1').addClass('selected-page')
});

$('.page').click(function (e) { 
    let pageClass = $(this).attr('class').split(' ')[1]
    lastPage = currentPage
    currentPage = pageClass.split('-')[1]
    if(lastPage != currentPage){
       goToPage(currentPage, lastPage)
    }
});

$('.button-next').click(function (e) { 
    goToPage(parseInt( currentPage ) + 1, currentPage)
    e.preventDefault();
});

$('.button-previous').click(function (e) {
    if(currentPage > 1){
        goToPage(parseInt(currentPage) - 1, currentPage)
    }
    e.preventDefault()
  })

$('.button-submit').click(function(e){
    var answers = $('input').val()
    console.log(answers)
})

function goToPage(page, last){
    lastPage = last
    currentPage = page
    $('.page-' + lastPage).removeClass('selected-page')
    $('.page-' + currentPage).addClass('selected-page')
    $('[index=' + currentPage + ']').removeClass('hidden')
    $('[index=' + lastPage + ']').addClass('hidden')
    
    $('.progress').animate({
        width: currentPage /  pageNumber * 100 + '%'
    });
    
    pageText = $('.page-' + currentPage).text()
    $('.page-title').text(pageText)

    switchButtons(currentPage, lastPage)
}

function switchButtons(page, lastPage){
    if(page == pageNumber){
        $('.button-submit').removeClass('hidden')
        $('.button-next').addClass('hidden')
    }
    else{
        if(lastPage == pageNumber)
        {
            $('.button-submit').addClass('hidden')
            $('.button-next').removeClass('hidden')
        }
        
    }
}