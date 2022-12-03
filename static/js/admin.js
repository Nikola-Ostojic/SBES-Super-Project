function addPage(){
    data = document.getElementById("page-form");
    formData = new FormData(data);

    $.ajax({
        type: "POST",
        url: "/addPage",
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            console.log(data)
        }
    });
}

