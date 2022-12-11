function addPage(){
    data = document.getElementById("page-form");
    formData = new FormData(data);    

    $.ajax({
        type: "POST",
        url: "/addPage",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            console.log(response)
        }
    });
}

function addQuestion(index){
    n = "question-form-" + index
    data = document.getElementById(n)
    formData = new FormData(data);
    formData.append('pageIndex', index)

    $.ajax({
        type: "POST",
        url: "/addQuestion",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            console.log(response)
        }
    });
}

function addAnswer(pageIndex,questionIndex){
    n = "answer-form-" + pageIndex + "-" + questionIndex
    data = document.getElementById(n);
    formData = new FormData(data);
    formData.append('pageIndex',pageIndex);
    formData.append('questionIndex', questionIndex);

    $.ajax({
        type: "POST",
        url: "/addAnswer",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            console.log(response)
        }
    });
}

function collapse(page,question=null){
    elements = null;

    if (question){
        elements = $('.admin-tab[data-page="' + page + '"][data-question="' + question + '"]')

        
    }else{        
        elements = $('.admin-tab[data-page="' + page + '"]')
    }
    $.each(elements, function(){        
        if ($(this).hasClass('hidden')){ 
            if(question){
                $(this).removeClass('hidden')
            }else{
                if(!$(this).attr('data-question')){
                    $(this).removeClass('hidden')
                }
            }
        }else{
            if(question){
                $(this).addClass('hidden')
            }else{                
                $(this).addClass('hidden')                
            }
        }
    })        
}

function showElement(page, question = null, answer = null){
    elements = null;

    if (answer){
        elements = $('.admin-form-container[data-page="' + page + '"][data-question="' + question + '"][data-answer="' + answer + '"]')        
    }
    else if (question){
        elements = $('.admin-form-container[data-page="' + page + '"][data-question="' + question + '"]')        
    }else{        
        elements = $('.admin-form-container[data-page="' + page + '"]')
    }

    $('.admin-form-container').addClass('hidden')

    $.each(elements, function(){        
        if ($(this).hasClass('hidden')){ 
            if(answer){
                $(this).removeClass('hidden')
            }
            else if(question){
                if(!$(this).attr('data-answer')){
                    $(this).removeClass('hidden')
                }
            }else
            {
                if(!$(this).attr('data-question') && !$(this).attr('data-answer')){
                    $(this).removeClass('hidden')
                }
            }
        }    
    })   


}





