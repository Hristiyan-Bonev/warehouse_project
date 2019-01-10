
$(function() {
  article = {}
  $("#articles").autocomplete({
    source: "/get_articles/",
    delay:1,
    select: function(event, ui) {
        $(this).blur();
        console.log(ui)
        article['name'] = ui.item.label
        article['quantity'] = ui.item.value
        article['lookup_value'] = ui.item.id
        article['price'] = ui.item.price
        $(this).val(ui.item.label);
        $("#quantity_available").html(ui.item.value)
        return false;
    },
  })
});


// populate autocompleted item's data in html row
function appendRow(data, quantity){
    total_price = data.price * quantity;
    $('#order_list').append(`<div class="row row_${data.lookup_value}">
                                <div class="col text-center">${data.name}</div>
                                <div class="col text-center">${quantity}</div>
                                <div class="col text-center">${data.price}</div>
                                <div class="col text-center">${total_price}</div>
                                <input type="hidden" name="product-${data.lookup_value}-data" value="${data.lookup_value}_${quantity}"/>
                             </div>`)
}

// function that appends header row in order_list div
function addHeader(){
    if ($(".row").length == 0){      // If there are any rows, append table header
        $("#order_list").append(`<div class="row header">
                                    <div class="col text-center">Продукт</div>
                                    <div class="col text-center">Брой продукти</div>
                                    <div class="col text-center">Eдинична цена</div>
                                    <div class="col text-center">Общо</div>
                                </div>`);
    } else {
        //if there are already rows, there's already a header
        return
    }
}


// clear both search fields after item is added
function clearFields(){
    $("#articles").val('');
    $("#quantity").val('');
}


// Check if there are enough products in storage
function validateQuantity(){
    available_quantity = $("#quantity_available").html();
    requested_quantity = $("#quantity").val();
    console.log(available_quantity,
    requested_quantity)

    if (parseInt(available_quantity) == 0){
        $('#error_message2').show()
        return false
    }
    console.log(available_quantity, requested_quantity);
    if (available_quantity < requested_quantity){
     $("#error_message").show()
     return false
    }
    // if everything is correct, hide the error messages
    $("#error_message").hide();
    $('#error_message2').hide();
    return true
}

function submitRow(e){
    if (!$("#articles").val() || !$("#quantity").val() ){
        return
    }

//    if (validateQuantity()){
    addHeader();;
    appendRow(article, $("#quantity").val());
    clearFields()
//    }
}