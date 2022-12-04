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





