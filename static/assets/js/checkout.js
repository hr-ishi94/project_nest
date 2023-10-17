$(document).ready(function(){
    $('#proceedPayment').click(function(e){
        e.preventDefault();

        var selectedPaymentMethod =$("input[name='payment-method']:checked").val();
    })
})