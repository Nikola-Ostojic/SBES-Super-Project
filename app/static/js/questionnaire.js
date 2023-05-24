var lastPage = 1
var pageNumber = 0
var result = 0

pageNumber = $('form').children().length - 1
currentPage = 1
lastPage = 1

$('.ftn-img').click(function (e) { 
    e.preventDefault()
    window.location.href = "/home"
 })

$('.answer').click(function (e) { 
    let radio = $(this).find('input[type=radio]')
    if (radio.length != 0){
        radio.prop("checked", true);
        $(this).siblings().removeClass('selected')
        $(this).addClass('selected')
    }
   

    let checkbox = $(this).find('input[type=checkbox]')
    if(checkbox.length != 0){
        if(checkbox.is(':checked')){
            checkbox.prop("checked", false);
            $(this).removeClass('selected')
        }
        else{
            checkbox.prop("checked", true);
            $(this).addClass('selected')
        }
    }
   
        
});

$(document).ready(function () {
    $('.page-1').addClass('selected-page')
});

$('.page').click(function (e) { 
    if(!validatePage(currentPage)){
        alert('Niste odgovorili na sva obavezna pitanja!')
        return false;
    }
    let pageClass = $(this).attr('class').split(' ')[1]
    lastPage = currentPage
    currentPage = pageClass.split('-')[1]
    if(lastPage != currentPage){
        goToPage(currentPage, lastPage)
    }
});

$('.button-next').click(function (e) { 
    e.preventDefault();
    if(!validatePage(currentPage)){
        alert('Niste odgovorili na sva obavezna pitanja!')
        return false;
    }
        
    goToPage(parseInt( currentPage ) + 1, currentPage)
});

$('.button-previous').click(function (e) {
    if(currentPage > 1){
        if(!validatePage(currentPage)){
            alert('Niste odgovorili na sva obavezna pitanja!')
            return false;
        }
        goToPage(parseInt(currentPage) - 1, currentPage)
    }
    e.preventDefault()
  })

$('.button-submit').click(function(e){
    e.preventDefault()
    if(!validatePage(currentPage)){
        alert('Niste odgovorili na sva obavezna pitanja!')
        return false;
    }
    var answers = $('input').val()
    submitForm()
})


function submitForm(){
    data = document.getElementById("question-form");
    formData = new FormData(data);

    $.ajax({
        type: "POST",
        url: "/result",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            alert('hello')
            result = response
            window.location.href = "/result"
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            alert("Status: " + textStatus); alert("Error: " + errorThrown); 
        } 
    })
}

function validatePage(page){
    let valid = true

    $("#question-form :input").each(function(){
        let input = $(this)

        let questionPageName = input.attr('name')
        let questionPage = -1
        if(questionPageName != undefined)
            questionPage = questionPageName.split('-')[1]

        if(questionPage == page && input.attr('type') == 'radio'){
            $(input).parent().parent().parent().addClass('error');
        }
    })

    $("#question-form :input").each(function(){
        let input = $(this)
        let questionPageName = input.attr('name')
        let questionPage = -1
        if(questionPageName != undefined)
            questionPage = questionPageName.split('-')[1]

        if(questionPage == page && (input.attr('type') == 'text' || input.attr('type') == 'number')){
            if(input.val() == ''){
                $(input).parent().parent().parent().addClass('error');
            }
            else{
                $(input).parent().parent().parent().removeClass('error');
            }
        }

        if(questionPage == page && input.attr('type') == 'radio'){
            if(!input.is(':checked')){
                
            }
            else{
                $(input).parent().parent().parent().removeClass('error');
            }   
        }
    })

    if($('div').hasClass('error')){
        return false
    }

    return true
}

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

    window.scrollTo(0, 0);
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

function checkLength(e){    
    let value = $(e).val()
    let length = value.length
    
    if(length > 9){
        $(e).val(value.slice(0, 9))
        alert('Maksimalna vrednost je 1 milijarda.')
    }
}