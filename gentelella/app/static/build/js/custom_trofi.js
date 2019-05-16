
function sucess_database(){
    var notice = PNotify.success({
        title: 'Database Updated!',
        text: 'Click me anywhere to dismiss me.',
        modules: {
          Buttons: {
            closer: false,
            sticker: false
          }
        }
      });
      notice.on('click', function() {
        notice.close();
      });
}

function show_error_msg(msg){
    var notice = PNotify.error({
        title: msg,
        text: 'Click me anywhere to dismiss me.',
        modules: {
          Buttons: {
            closer: false,
            sticker: false
          }
        }
      });
      notice.on('click', function() {
        notice.close();
      });
}

function show_loading(){
    return PNotify.info({
        text: 'Please Wait',
        icon: 'fa fa-spinner fa-pulse',
        hide: false,
        shadow: false,
        width: '200px',
        modules: {
          Buttons: {
            closer: false,
            sticker: false
          }
        }
      });
}

function hide_loading(loader){
    loader.close();
}

function update_database_message(msg){
    var notice = PNotify.info({
         title: 'Database Updated!',
         text: 'Refreshing page in 2 seconds...',
         addClass: 'nonblock',
       });
       setTimeout(function () {
         location.reload();
     }, 2000);

     //   notice.on('click', function() {
     //     notice.close();
     //   });
 }

function init_manage_listener(db, uid){

    // none as of now

}

function init_history_listener(db, uid){

    var history_table = $('#datatable-responsive-history').DataTable();
    var wait = 0;
    db.collection("restaurants").doc(uid).collection("private").doc(uid).collection("orders")
    .onSnapshot(function(snapshot) {
        snapshot.docChanges().forEach(function(change) {
            if (change.type === "added") {
                // change.doc.id

                // TODO: deal with first time call

                if(wait < history_table.data().length){
                    wait += 1
                }
                else{

                    // console.log("New city: ", change.doc.data());

                    update_database_message("Update: New order " +  change.doc.id.substr(11) + " added! Refreshing page in 2 seconds...")


                        }

                }

            if (change.type === "modified") {

                console.log("Modified city: ", change.doc.data());

                update_database_message("Update: New order " +  change.doc.id.substr(11) + " added! Refreshing page in 2 seconds...")
            }
            if (change.type === "removed") {
                console.log("Removed city: ", change.doc.data());

                update_database_message("Update: New order " +  change.doc.id.substr(11) + " added! Refreshing page in 2 seconds...")
            }
        });
    });

}


function init_incoming_listener(db, uid){

    var incoming_table = $('#datatable-responsive-incoming').DataTable();
    var wait = 0;
    db.collection("restaurants").doc(uid).collection("private").doc(uid).collection("orders").where("incoming", "==", true)
    .onSnapshot(function(snapshot) {
        snapshot.docChanges().forEach(function(change) {
            if (change.type === "added") {
                // change.doc.id

                // TODO: deal with first time call

                if(wait < incoming_table.data().length){
                    wait += 1
                }
                else{

                    // console.log("New city: ", change.doc.data());

                    update_database_message("Update: New order " +  change.doc.id.substr(11) + " added! Refreshing page in 2 seconds...")


                        }

                }

            if (change.type === "modified") {

                console.log("Modified city: ", change.doc.data());

                update_database_message("Update: New order " +  change.doc.id.substr(11) + " added! Refreshing page in 2 seconds...")
            }
            if (change.type === "removed") {
                console.log("Removed city: ", change.doc.data());

                update_database_message("Update: New order " +  change.doc.id.substr(11) + " added! Refreshing page in 2 seconds...")
            }
        });
    });

}

function init_menu(){

    var menu_table = $('#datatable-responsive-menu').DataTable();

    for(var i = 1; i <= menu_table.data().length; i++){
        $('#update-sales-price-' + parseInt(i)).hide();
        $('#update-profit-margin-' + parseInt(i)).hide();
        $('#update-ingredients-cost-' + parseInt(i)).hide();
    }


    $('.trofi-manage-sales-price').keyup(function() {
        // console.log("focused me")
        //console.log(this)
        table_id = this.id.substr(12)
        if(this.value == ""){
            $('#update-sales-price-' + table_id).hide()
        }
        else{
            $('#update-sales-price-' + table_id).show()
        }
      });

      $('.trofi-manage-profit-margin').keyup(function() {
        // console.log("focused me")
        //console.log(this)
        table_id = this.id.substr(13)
        if(this.value == ""){
            $('#update-profit-margin' + table_id).hide()
        }
        else{
            $('#update-profit-margin' + table_id).show()
        }
      });

      $('.trofi-manage-ingredients-cost').keyup(function() {
        // console.log("focused me")
        //console.log(this)
        table_id = this.id.substr(16)
        if(this.value == ""){
            $('#update-ingredients-cost' + table_id).hide()
        }
        else{
            $('#update-ingredients-cost' + table_id).show()
        }
      });

      $('.trofi-update-sales-price').click(function() {
        // console.log("clicked me")
        // console.log(this)
        table_id = this.id.substr(19)
        new_sales_price = $('#sales-price-' + table_id).val()

        new_sales_price_num = parseFloat(new_sales_price)

        if(!isNaN(new_sales_price_num) && new_sales_price_num >= 0){

               loader = show_loading();

               food_id = this.classList[3]

               var url = '/api/foods/'
               var data = {id: "sales-price-update", food_id: food_id, sales_price: new_sales_price_num}

               fetch(url, {
                   method: 'PUT', // or 'PUT'
                   body: JSON.stringify(data), // data can be `string` or {object}!
                   headers:{
                     'Content-Type': 'application/json'
                   }
                 })
                 .then(response => {
                    response.json().then(data => {
                        // code that can access both here
                        //console.log(data)
                        if(data.status == 200){
                            // Show success message
                            hide_loading(loader);
                            sucess_database()
                            $('#update-sales-price-' + table_id).hide()
                       $('#sales-price-' + table_id).val('')
                       $('#sales-price-' + table_id).attr("placeholder", "$" + new_sales_price_num);
                        }
                        else if(data.status == 404){
                            hide_loading(loader);
                            show_error_msg(data.message)
                            console.log(data.error)
                        }
                    })

               })
               .catch(error => console.error('Error:', error))
               .then(response => {
                   // console.log('Success:', JSON.stringify(response));

               });

            }
        else{
            show_error_msg('Error: The sales price \'' + new_sales_price +  '\' is not valid!')
        }

      });

      $('.trofi-update-profit-margin').click(function() {
        // console.log("clicked me")
        // console.log(this)
        table_id = this.id.substr(21)
        new_profit_margin = $('#profit-margin-' + table_id).val()

        new_profit_margin_num = parseFloat(new_profit_margin)

        if(!isNaN(new_profit_margin_num) && new_profit_margin_num >= 0){

               loader = show_loading();

               food_id = this.classList[3]

               var url = '/api/foods/'
               var data = {id: "profit-margin-update", food_id: food_id, profit_margin: new_profit_margin_num}

               fetch(url, {
                   method: 'PUT', // or 'PUT'
                   body: JSON.stringify(data), // data can be `string` or {object}!
                   headers:{
                     'Content-Type': 'application/json'
                   }
                 })
                 .then(response => {
                    response.json().then(data => {
                        // code that can access both here
                        //console.log(data)
                        if(data.status == 200){
                            // Show success message
                            hide_loading(loader);
                            sucess_database()
                            $('#update-profit-margin-' + table_id).hide()
                            $('#profit-margin-' + table_id).val('')
                            $('#profit-margin-' + table_id).attr("placeholder", "$" + new_profit_margin_num);
                        }
                        else if(data.status == 404){
                            hide_loading(loader);
                            show_error_msg(data.message)
                            console.log(data.error)
                        }
                    })

               })
               .catch(error => console.error('Error:', error))
               .then(response => {
                   // console.log('Success:', JSON.stringify(response));

               });

            }
        else{
            show_error_msg('Error: The profit margin \'' + new_profit_margin +  '\' is not valid!')
        }

      });

      $('.trofi-update-ingredients-cost').click(function() {
        // console.log("clicked me")
        // console.log(this)
        table_id = this.id.substr(24)
        new_ingredients_cost = $('#ingredients-cost-' + table_id).val()

        new_ingredients_cost_num = parseFloat(new_ingredients_cost)

        if(!isNaN(new_ingredients_cost_num) && new_ingredients_cost_num >= 0){

               loader = show_loading();

               food_id = this.classList[3]

               var url = '/api/foods/'
               var data = {id: "ingredients-cost-update", food_id: food_id, ingredients_cost: new_ingredients_cost_num}

               fetch(url, {
                   method: 'PUT', // or 'PUT'
                   body: JSON.stringify(data), // data can be `string` or {object}!
                   headers:{
                     'Content-Type': 'application/json'
                   }
                 })
                 .then(response => {
                    response.json().then(data => {
                        // code that can access both here
                        //console.log(data)
                        if(data.status == 200){
                            // Show success message
                            hide_loading(loader);
                            sucess_database()
                            $('#update-ingredients-cost-' + table_id).hide()
                       $('#ingredients-cost-' + table_id).val('')
                       $('#ingredients-cost-' + table_id).attr("placeholder", "$" + new_ingredients_cost_num);
                        }
                        else if(data.status == 404){
                            hide_loading(loader);
                            show_error_msg(data.message)
                            console.log(data.error)
                        }
                    })



               })
               .catch(error => console.error('Error:', error))
               .then(response => {
                   // console.log('Success:', JSON.stringify(response));

               });

            }
        else{
            show_error_msg('Error: The ingredients cost \'' + new_ingredients_cost +  '\' is not valid!')
        }

      });

}

function init_hours(){

    var hours_table = $('#datatable-responsive-manage').DataTable({
        paging: false,
        ordering: false,
    });

    for(var i = 1; i <= hours_table.data().length; i++){
        $('#datatable-responsive-' + parseInt(i)).DataTable();
        $('#update-discount-' + parseInt(i)).hide();
        $('#update-payroll-' + parseInt(i)).hide();
        $('#update-overhead-' + parseInt(i)).hide();
    }

    $('.trofi-manage-discount').keyup(function() {
        // console.log("focused me")
        //console.log(this)
        table_id = this.id.substr(18)
        if(this.value == ""){
            $('#update-discount-' + table_id).hide()
        }
        else{
            $('#update-discount-' + table_id).show()
        }
      });

      $('.trofi-manage-payroll').keyup(function() {
        // console.log("focused me")
        //console.log(this)
        table_id = this.id.substr(8)
        if(this.value == ""){
            $('#update-payroll-' + table_id).hide()
        }
        else{
            $('#update-payroll-' + table_id).show()
        }
      });

      $('.trofi-manage-overhead').keyup(function() {
        // console.log("focused me")
        //console.log(this)
        table_id = this.id.substr(9)
        if(this.value == ""){
            $('#update-overhead-' + table_id).hide()
        }
        else{
            $('#update-overhead-' + table_id).show()
        }
      });


      $('.trofi-update-payroll').click(function() {

        table_id = this.id.substr(15)
        new_payroll = $('#payroll-' + table_id).val()

        new_payroll_num = parseFloat(new_payroll);

        if(!isNaN(new_payroll_num) && new_payroll_num > 0.0){

                loader = show_loading();

               hour_id = this.classList[4]

               var url = '/api/hours/'
               var data = {id: "payroll-update", hour_id: hour_id, payroll: new_payroll_num}

               fetch(url, {
                   method: 'PUT', // or 'PUT'
                   body: JSON.stringify(data), // data can be `string` or {object}!
                   headers:{
                     'Content-Type': 'application/json'
                   }
                 })
                 .then(response => {
                    response.json().then(data => {
                        // code that can access both here
                        //console.log(data)
                        if(data.status == 200){
                            // Show success message
                            hide_loading(loader);
                            sucess_database()
                            $('#update-payroll-' + table_id).hide()
                        }
                        else if(data.status == 404){
                            hide_loading(loader);
                            show_error_msg(data.message)
                            console.log(data.error)
                        }
                    })
               })
               .catch(error => console.error('Error:', error))
               .then(response => {
                   // console.log('Success:', JSON.stringify(response));

               });

        }
        else{
            show_error_msg('Error: The payroll amount \'' + new_payroll +  '\' is not valid!',)
        }

      });

      $('.trofi-update-overhead').click(function() {

        table_id = this.id.substr(16)
        new_overhead = $('#overhead-' + table_id).val()

        new_overhead_num = parseFloat(new_overhead);

        if(!isNaN(new_overhead_num) && new_overhead_num > 0.0){

             loader = show_loading();

               hour_id = this.classList[4]

               var url = '/api/hours/'
               var data = {id: "overhead-cost-update", hour_id: hour_id, overhead_cost: new_overhead_num}

               fetch(url, {
                   method: 'PUT', // or 'PUT'
                   body: JSON.stringify(data), // data can be `string` or {object}!
                   headers:{
                     'Content-Type': 'application/json'
                   }
                 })
                 .then(response => {
                    response.json().then(data => {
                        // code that can access both here
                        //console.log(data)
                        if(data.status == 200){
                            // Show success message
                            hide_loading(loader);
                            sucess_database()
                            $('#update-overhead-' + table_id).hide()
                        }
                        else if(data.status == 404){
                            hide_loading(loader);
                            show_error_msg(data.message)
                            console.log(data.error)
                        }
                    })

               })
               .catch(error => console.error('Error:', error))
               .then(response => {
                   // console.log('Success:', JSON.stringify(response));

               });

        }
        else{
            show_error_msg('Error: The overhead cost \'' + new_overhead +  '\' is not valid!',)
        }

      });

      $('.trofi-update-discount').click(function() {
        // console.log("clicked me")
        // console.log(this)
        table_id = this.id.substr(16)
        new_discount = $('#starting-discount-' + table_id).val()

        new_discount_num = parseInt(new_discount)

        if(!isNaN(new_discount_num) && new_discount_num >= 0 && new_discount_num <= 100){

               loader = show_loading();

               hour_id = this.classList[3]

               var url = '/api/hours/'
               var data = {id: "percent-discount-update", hour_id: hour_id, starting_discount: new_discount_num}

               fetch(url, {
                   method: 'PUT', // or 'PUT'
                   body: JSON.stringify(data), // data can be `string` or {object}!
                   headers:{
                     'Content-Type': 'application/json'
                   }
                 })
                 .then(response => {

                    response.json().then(data => {
                        // code that can access both here
                        ////console.log(data)
                        if(data.status == 200){
                            // Show success message
                            hide_loading(loader);
                            sucess_database()
                            $('#update-discount-' + table_id).hide()
                            $('#starting-discount-' + table_id).val('')
                            $('#starting-discount-' + table_id).attr("placeholder", "Currently: " + new_discount_num + "%");
                        }
                        else if(data.status == 404){
                            hide_loading(loader);
                            show_error_msg(data.message)
                            console.log(data.error)
                        }
                    })
               })
               .catch(error => console.error('Error:', error))
               .then(response => {
                   // console.log('Success:', JSON.stringify(response));

               });

            }
        else{
            show_error_msg('Error: The starting discount \'' + new_discount +  '\' is not valid!')
        }

      });

    $('.trofi-hour-status').on('ifChecked', function() {
        loader = show_loading();

        id = this.id
        hour_id = id

        var url = '/api/hours/'
        var data = {id: "hour-status-active", hour_id: hour_id, hour_active: true}

        fetch(url, {
            method: 'PUT', // or 'PUT'
            body: JSON.stringify(data), // data can be `string` or {object}!
            headers:{
              'Content-Type': 'application/json'
            }
          })
          .then(response => {
            response.json().then(data => {
                // code that can access both here
                ////console.log(data)
                if(data.status == 200){
                    // Show success message
                    hide_loading(loader);
                    sucess_database()
                }
                else if(data.status == 404){
                    hide_loading(loader);
                    show_error_msg(data.message)
                    console.log(data.error)
                }
            })
        })
        .catch(error => console.error('Error:', error))
        .then(response => {
            // console.log('Success:', JSON.stringify(response));

        });

    });

    $('.trofi-hour-status').on('ifUnchecked', function() {
        loader = show_loading();

        id = this.id
        hour_id = id

        var url = '/api/hours/'
        var data = {id: "hour-status-active", hour_id: hour_id, hour_active: false}

        fetch(url, {
            method: 'PUT', // or 'PUT'
            body: JSON.stringify(data), // data can be `string` or {object}!
            headers:{
              'Content-Type': 'application/json'
            }
          })
          .then(response => {
            response.json().then(data => {
                // code that can access both here
                //console.log(data)
                if(data.status == 200){
                    // Show success message
                    hide_loading(loader);
                    sucess_database()
                }
                else if(data.status == 404){
                    hide_loading(loader);
                    show_error_msg(data.message)
                    console.log(data.error)
                }
            })
        })
        .catch(error => console.error('Error:', error))
        .then(response => {
            // console.log('Success:', JSON.stringify(response));

        });

    });

    $('.trofi-hour-food-status').on('ifChecked', function() {
        loader = show_loading();

        id = this.id
        separator = this.id.indexOf('-')
        hour_id = id.substr(0, separator)
        food_id = id.substr(separator+1)

        var url = '/api/hours/'
        var data = {id: "food-status-active", hour_id: hour_id, food_id: food_id, food_active: true}

        fetch(url, {
            method: 'PUT', // or 'PUT'
            body: JSON.stringify(data), // data can be `string` or {object}!
            headers:{
              'Content-Type': 'application/json'
            }
          })
          .then(response => {
            response.json().then(data => {
                // code that can access both here
                //console.log(data)
                if(data.status == 200){
                    // Show success message
                    hide_loading(loader);
                    sucess_database()
                }
                else if(data.status == 404){
                    hide_loading(loader);
                    show_error_msg(data.message)
                    console.log(data.error)
                }
            })
        })
        .catch(error => console.error('Error:', error))
        .then(response => {
            console.log('Success:', JSON.stringify(response));

        });

    });

    $('.trofi-hour-food-status').on('ifUnchecked', function() {
        loader = show_loading();

        id = this.id
        separator = this.id.indexOf('-')
        hour_id = id.substr(0, separator)
        food_id = id.substr(separator+1)

        var url = '/api/hours/'
        var data = {id: "food-status-active", hour_id: hour_id, food_id: food_id, food_active: false}

        fetch(url, {
            method: 'PUT', // or 'PUT'
            body: JSON.stringify(data), // data can be `string` or {object}!
            headers:{
              'Content-Type': 'application/json'
            }
          })
          .then(response => {
            response.json().then(data => {
                // code that can access both here
                //console.log(data)
                if(data.status == 200){
                    // Show success message
                    hide_loading(loader);
                    sucess_database()
                }
                else if(data.status == 404){
                    hide_loading(loader);
                    show_error_msg(data.message)
                    console.log(data.error)
                }
            })
        })
        .catch(error => console.error('Error:', error))
        .then(response => {
            // console.log('Success:', JSON.stringify(response));

        });

    });



}

function init_other(){

    // $('#datatable-responsive-other').DataTable({
    //     paging: false,
    //     ordering: false,
    // });

    $('#update-ccf-percentage').hide()
    $('#update-ccf-constant').hide()

    $('#ccf-percentage').keyup(function() {
        // console.log("focused me")
        //console.log(this)
        if(this.value == ""){
            $('#update-ccf-percentage').hide()
        }
        else{
            $('#update-ccf-percentage').show()
        }
      });

    $('#ccf-constant').keyup(function() {
        // console.log("focused me")
        //console.log(this)
        if(this.value == ""){
            $('#update-ccf-constant').hide()
        }
        else{
            $('#update-ccf-constant').show()
        }
      });

      $('#update-ccf-percentage').click(function() {

        new_ccf_percentage = $('#ccf-percentage').val()

        new_ccf_percentage_num = parseFloat(new_ccf_percentage);

        if(!isNaN(new_ccf_percentage_num) && new_ccf_percentage_num >= 0.0 && new_ccf_percentage_num <= 100.0){

             loader = show_loading();

               var url = '/api/other/'
               var data = {id: "ccf-percentage-update", ccf_percentage: new_ccf_percentage_num}

               fetch(url, {
                   method: 'PUT', // or 'PUT'
                   body: JSON.stringify(data), // data can be `string` or {object}!
                   headers:{
                     'Content-Type': 'application/json'
                   }
                 })
                 .then(response => {

                    response.json().then(data => {
                        // code that can access both here
                        //console.log(data)
                        if(data.status == 200){
                            // Show success message
                            hide_loading(loader);
                            sucess_database()
                            $('#update-ccf-percentage').hide()
                            $('#ccf-percentage').val('')
                            $('#ccf-percentage').attr("placeholder", new_ccf_percentage_num + "%");
                        }
                        else if(data.status == 404){
                            hide_loading(loader);
                            show_error_msg(data.message)
                            console.log(data.error)
                        }
                    })

               })
               .catch(error => console.error('Error:', error))
               .then(response => {
                   // console.log('Success:', JSON.stringify(response));

               });

        }
        else{
            show_error_msg('Error: The credit card fee percentage \'' + new_ccf_percentage +  '\' is not valid!',)
        }

      });


      $('#update-ccf-constant').click(function() {

        new_ccf_constant = $('#ccf-constant').val()

        new_ccf_constant_num = parseFloat(new_ccf_constant);

        if(!isNaN(new_ccf_constant_num) && new_ccf_constant_num >= 0.0){

             loader = show_loading();

               var url = '/api/other/'
               var data = {id: "ccf-constant-update", ccf_constant: new_ccf_constant_num}

               fetch(url, {
                   method: 'PUT', // or 'PUT'
                   body: JSON.stringify(data), // data can be `string` or {object}!
                   headers:{
                     'Content-Type': 'application/json'
                   }
                 })
                 .then(response => {

                    response.json().then(data => {
                        // code that can access both here
                        //console.log(data)
                        if(data.status == 200){
                            // Show success message
                            hide_loading(loader);
                            sucess_database()
                            $('#update-ccf-constant').hide()
                            $('#ccf-constant').val('')
                            $('#ccf-constant').attr("placeholder", new_ccf_constant_num);
                        }
                        else if(data.status == 404){
                            hide_loading(loader);
                            show_error_msg(data.message)
                            console.log(data.error)
                        }
                    })
               })
               .catch(error => console.error('Error:', error))
               .then(response => {
                   // console.log('Success:', JSON.stringify(response));

               });

        }
        else{
            show_error_msg('Error: The credit card fee constant \'' + new_ccf_constant +  '\' is not valid!',)
        }

      });

}

function init_manage(){
    console.log('init manage');

    init_hours();
    init_menu();
    init_other();

    $('#datatable-responsive-manage').show()
    $('#datatable-responsive-menu').show()
    $('#datatable-responsive-other').show()



}

function init_incoming_table(){
    console.log('init incoming');

    var incoming_table = $('#datatable-responsive-incoming').DataTable();

    for(var i = 1; i <= incoming_table.data().length; i++){
        $('#datatable-responsive-' + parseInt(i)).DataTable();
    }

    $('#datatable-responsive-incoming').show()

    $('.trofi-incoming-status').on('ifChecked', function() {
        loader = show_loading();

        id = this.id
        order_id = this.id.substring(10)

        var url = '/api/orders/'
        var data = {id: "food-status-ready", order_id: order_id, order_ready: true}

        fetch(url, {
            method: 'PUT', // or 'PUT'
            body: JSON.stringify(data), // data can be `string` or {object}!
            headers:{
              'Content-Type': 'application/json'
            }
          })
          .then(response => {

            response.json().then(data => {
                // code that can access both here
                //console.log(data)
                if(data.status == 200){
                    // Show success message
                    hide_loading(loader);
                    sucess_database()
                }
                else if(data.status == 404){
                    hide_loading(loader);
                    show_error_msg(data.message)
                    console.log(data.error)
                }
            })
        })
        .catch(error => console.error('Error:', error))
        .then(response => {
            // console.log('Success:', JSON.stringify(response));

        });

    });

    $('.trofi-incoming-status').on('ifUnchecked', function() {
        loader = show_loading();

        id = this.id
        order_id = this.id.substring(10)

        var url = '/api/orders/'
        var data = {id: "food-status-ready", order_id: order_id, order_ready: false}

        fetch(url, {
            method: 'PUT', // or 'PUT'
            body: JSON.stringify(data), // data can be `string` or {object}!
            headers:{
              'Content-Type': 'application/json'
            }
          })
          .then(response => {
            response.json().then(data => {
                // code that can access both here
                //console.log(data)
                if(data.status == 200){
                    // Show success message
                    hide_loading(loader);
                    sucess_database()
                }
                else if(data.status == 404){
                    hide_loading(loader);
                    show_error_msg(data.message)
                    console.log(data.error)
                }
            })
        })
        .catch(error => console.error('Error:', error))
        .then(response => {
            // console.log('Success:', JSON.stringify(response));

        });

    });

}

function init_history_table(){

    console.log('init history');

    var history_table = $('#datatable-responsive-history').DataTable();

    for(var i = 1; i <= history_table.data().length; i++){
        $('#datatable-responsive-' + parseInt(i)).DataTable();
    }

    $('#datatable-responsive-history').show()

}


$(document).ready(function() {

    var db = firebase.firestore();
    var uid = $('#uid').val()

    if ( location.href.includes("incoming") ) {
        init_incoming_table();
        init_incoming_listener(db, uid);
    }

    if ( location.href.includes("manage") ) {
        init_manage();
        init_manage_listener(db, uid);
    }

    if ( location.href.includes("history") ) {
        init_history_table();
        init_history_listener(db, uid);
    }

});
