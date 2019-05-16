
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

function init_manage(){
    console.log('init manage');

    var manage_table = $('#datatable-responsive-manage').DataTable({        
        paging: false,
        ordering: false,   
    });    

    $('#datatable-responsive-menu').DataTable();  

    $('#datatable-responsive-other').DataTable({        
        paging: false,
        ordering: false,   
    });  
    


    for(var i = 1; i <= manage_table.data().length; i++){
        $('#datatable-responsive-' + parseInt(i)).DataTable();
        $('#update-discount-' + parseInt(i)).hide();
        $('#update-payroll-' + parseInt(i)).hide();
        $('#update-overhead-' + parseInt(i)).hide();
    }

    $('#datatable-responsive-manage').show()
    $('#datatable-responsive-menu').show()
    $('#datatable-responsive-other').show()

    

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
                   response.json();
                   if(response.status == 200){
                       // Show success message   
                       hide_loading(loader);         
                       sucess_database()                       
                       $('#update-payroll-' + table_id).hide()                                              
                   } 
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
                   response.json();
                   if(response.status == 200){
                       // Show success message   
                       hide_loading(loader);         
                       sucess_database()                       
                       $('#update-overhead-' + table_id).hide()                                              
                   } 
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
                   response.json();
                   if(response.status == 200){
                       // Show success message   
                       hide_loading(loader);         
                       sucess_database()                       
                       $('#update-discount-' + table_id).hide()
                       $('#starting-discount-' + table_id).val('')
                       $('#starting-discount-' + table_id).attr("placeholder", "Currently: " + new_discount_num + "%");
                   } 
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
            response.json();
            if(response.status == 200){
                // Show success message   
                hide_loading(loader);         
                sucess_database()
            } 
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
            response.json();
            if(response.status == 200){
                // Show success message   
                hide_loading(loader);         
                sucess_database()
            } 
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
                console.log(data)
                if(data.status == 200){
                    // Show success message   
                    hide_loading(loader);         
                    sucess_database()
                }
                else if(data.status == 404){
                    hide_loading(loader);                 
                    show_error_msg(data.message)
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
            response.json();
            if(response.status == 200){
                // Show success message   
                hide_loading(loader);         
                sucess_database()
            } 
        })
        .catch(error => console.error('Error:', error))
        .then(response => {            
            // console.log('Success:', JSON.stringify(response));

        });
    
    });



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
            response.json();
            if(response.status == 200){
                // Show success message   
                hide_loading(loader);         
                sucess_database()
            } 
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
            response.json();
            if(response.status == 200){
                // Show success message   
                hide_loading(loader);         
                sucess_database()
            } 
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
