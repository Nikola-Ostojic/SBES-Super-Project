$( document ).ready(function() {
    console.log( "ready!" );
});

$('#criticalBusiness').click(function (e) { 
    e.preventDefault();
    window.location.href = "/criticalBusiness"
});


$('#smallBusiness').click(function (e) { 
    e.preventDefault();
    window.location.href = "/smallBusiness"
});

$('#individuals').click(function (e) { 
    e.preventDefault();
    window.location.href = "/individuals"
});

