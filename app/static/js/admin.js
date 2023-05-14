toastr.options = {
    "closeButton": false,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-top-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "800",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
  }


function editPage(pageId){
    data = document.getElementById("edit-page-" + pageId);
    formData = new FormData(data);  
    formData.append('pageId', pageId)  

    $.ajax({
        type: "POST",
        url: "/editPage",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            toastr["success"]("Uspešno izvršena akcija!", "Obaveštenje")
        }
    });
}

function editQuestion(pageId,questionId){
    data = document.getElementById("edit-question-" + pageId + "-" + questionId);
    formData = new FormData(data);  
    formData.append('pageId', pageId)  
    formData.append('questionId', questionId)  

    $.ajax({
        type: "POST",
        url: "/editQuestion",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            toastr["success"]("Uspešno izvršena akcija!", "Obaveštenje")
        }
    });
}

function editAnswer(pageId,questionId,answerId){
    data = document.getElementById("edit-answer-" + pageId + "-" + questionId + "-" + answerId);
    formData = new FormData(data);  
    formData.append('pageId', pageId)  
    formData.append('questionId', questionId)  
    formData.append('answerId', answerId)

    $.ajax({
        type: "POST",
        url: "/editAnswer",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            toastr["success"]("Uspešno izvršena akcija!", "Obaveštenje")
        }
    });
}

function addAnswer(pageId,questionId){
    n = "answer-form-" + pageId + "-" + questionId
    data = document.getElementById(n);
    formData = new FormData(data);
    formData.append('pageId',pageId);
    formData.append('questionId', questionId);

    $.ajax({
        type: "POST",
        url: "/addAnswer",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            window.location.reload();
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
    $('.new-answer-form').addClass('hidden')

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

function showAddAnswer(pageIndex,questionIndex){
    $('.new-answer-form').addClass('hidden')
    $('.admin-form-container').addClass('hidden')
    $('.new-answer-form[data-page="' + pageIndex + '"][data-question="' + questionIndex + '"]').removeClass("hidden")         
}





