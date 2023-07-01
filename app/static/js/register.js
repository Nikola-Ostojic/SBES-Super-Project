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

function register(){
    data = document.getElementById('register-form');
    formData = new FormData(data);

    $.ajax({
        type: "POST",
        url: "/register",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response === "REGISTERED") {
                toastr["success"]("Uspešno registrovan!", "Obaveštenje");
                window.location.href = window.location.origin + '/login';
            }
        },
        error: function () {
            toastr["error"]("Greška pri autentifikaciji!", "Obaveštenje");
        }
    });
}

