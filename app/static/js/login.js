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

function login(){
    data = document.getElementById('login-form');
    formData = new FormData(data);

    $.ajax({
        type: "POST",
        url: "/login",
        data: formData,
        contentType: false,
        processData: false,
        success: function () {
            toastr["success"]("Uspešno autentifikovan!", "Obaveštenje")
            window.location.href = window.location.origin + '/admin';
        }
    });
}

