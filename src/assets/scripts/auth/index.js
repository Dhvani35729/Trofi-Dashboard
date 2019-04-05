import * as $ from 'jquery';
import * as firebase from 'firebase';
import 'firebase/firestore';
var Tabulator = require('tabulator-tables');

export default (function () {
                
                // Initialize Firebase
                
                var config = {
                apiKey: "AIzaSyCwgogOI0rJDijj-r97dbWjEinKkrBH1Ok",
                authDomain: "daydesign-a277f.firebaseapp.com",
                databaseURL: "https://daydesign-a277f.firebaseio.com",
                projectId: "daydesign-a277f",
                storageBucket: "daydesign-a277f.appspot.com",
                messagingSenderId: "758132951647"
                };
                firebase.initializeApp(config);
                
                var db = firebase.firestore();
                
                console.log("app scripts :)");
                
                                
                $('select').each(function(){
                                 var $this = $(this), numberOfOptions = $(this).children('option').length;
                                 
                                 $this.addClass('select-hidden');
                                 $this.wrap('<div class="select"></div>');
                                 $this.after('<div class="select-styled"></div>');
                                 
                                 var $styledSelect = $this.next('div.select-styled');
                                 $styledSelect.text($this.children('option').eq(0).text());
                                 
                                 var $list = $('<ul />', {
                                               'class': 'select-options'
                                               }).insertAfter($styledSelect);
                                 
                                 for (var i = 0; i < numberOfOptions; i++) {
                                 $('<li />', {
                                   text: $this.children('option').eq(i).text(),
                                   rel: $this.children('option').eq(i).val()
                                   }).appendTo($list);
                                 }
                                 
                                 var $listItems = $list.children('li');
                                 
                                 $styledSelect.click(function(e) {
                                                     e.stopPropagation();
                                                     $('div.select-styled.active').not(this).each(function(){
                                                                                                  $(this).removeClass('active').next('ul.select-options').hide();
                                                                                                  });
                                                     $(this).toggleClass('active').next('ul.select-options').toggle();
                                                     });
                                 
                                 $listItems.click(function(e) {
                                                  e.stopPropagation();
                                                  $styledSelect.text($(this).text()).removeClass('active');
                                                  $this.val($(this).attr('rel'));
                                                  $list.hide();
                                                  //console.log($this.val());
                                                  });
                                 
                                 $(document).click(function() {
                                                   $styledSelect.removeClass('active');
                                                   $list.hide();
                                                   });
                                 
                                 });
                
                
                
                if(document.URL.indexOf("signup.html") != -1){
                
                $('#r_err_message').hide();
                $('#r_succ_message').hide();
                $('#r_loading').hide();
                
                $('#r_name').keypress(function() {
                                      $('#r_err_message').hide();
                                      $(this).focus();
                                      });
                $('#r_email').keypress(function() {
                                       $('#r_err_message').hide();
                                       $(this).focus();
                                       });
                $('#trofi_code').keypress(function() {
                                          $('#r_err_message').hide();
                                          $(this).focus();
                                          });
                $('#r_password').keypress(function() {
                                          $('#r_err_message').hide();
                                          $(this).focus();
                                          });
                $('#r_confirm_password').keypress(function() {
                                                  $('#r_err_message').hide();
                                                  $(this).focus();
                                                  });
                
                
                $('#register_user').on('click', e => {
                                       registerUser(db);
                                       e.preventDefault();
                                       });
                
                }
                
                if(document.URL.indexOf("signin.html") != -1){
                
                $('#l_err_message').hide();
                $('#l_succ_message').hide();
                $('#l_loading').hide();
                
                $('#l_email').keypress(function() {
                                       $('#l_err_message').hide();
                                       $(this).focus();
                                       });
                $('#l_password').keypress(function() {
                                          $('#l_err_message').hide();
                                          $(this).focus();
                                          });
                
                $('#login_user').on('click', e => {
                                    loginUser(db);
                                    e.preventDefault();
                                    });
                }
                
                handleUserAuth(db);
                
                $('#logout').on('click', e => {
                                logoutUser();
                                e.preventDefault();
                                });
                
                }());

function handleUserAuth(db){
    firebase.auth().onAuthStateChanged(function(user) {
                                       
                                       if (user) {
                                       // User is signed in.
                                       
                                       var rememberMe = localStorage.getItem("remember_me_trofi");
                                       if(rememberMe != 'true'){
                                       firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION)
                                       }
                                       else{
                                       firebase.auth().setPersistence(firebase.auth.Auth.Persistence.LOCAL)
                                       }
                                       
                                       if( (!$('#l_succ_message').is(":visible") && document.URL.indexOf("signin.html") != -1) ||  document.URL.indexOf("signup.html") != -1){
                                       window.location.href = "index.html";
                                       }
                                       
                                       if(document.URL.indexOf("manage.html") != -1){
                                       
                                       var manageData = [];
                                       
                                       var tableManage = new Tabulator("#manage-table", {
                                                                       height:"100%", // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
                                                                       reactiveData:true, //enable reactive data
                                                                       data:manageData, //assign data to table
                                                                       dataTree:true,
                                                                       dataTreeStartExpanded:false,
                                                                       layout:"fitColumns", //fit columns to width of table (optional)
                                                                       columns:[ //DeffitDataine Table Columns
                                                                                {title:"sort", field:"sort_id", visible: false},
                                                                                {title:"Active", field:"active", formatter:function(cell, formatterParams, onRendered){
                                                                                //cell - the cell component
                                                                                //formatterParams - parameters set for the column
                                                                                //onRendered - function to call when the formatter has been rendered
                                                                                console.log("render");
                                                                                console.log(cell.getValue());
                                                                                // if(cell.getValue() == true){
                                                                                //   return "<label class=\"switch\"><input id=\"slider_" + cell.getRow().getData().id + "\" type=\"checkbox\" checked><span class=\"slider round\"></span></label>"
                                                                                // }
                                                                                // else{
                                                                                onRendered(function(){
                                                                                           console.log('set active');
                                                                                           console.log(cell.getValue());
                                                                                           $("#slider_" + cell.getRow().getData().sort_id).prop('checked', cell.getValue());
                                                                                           });
                                                                                
                                                                                return "<label class=\"switch\"><input id=\"slider_" + cell.getRow().getData().sort_id + "\" type=\"checkbox\"><span class=\"slider round\"></span></label>"
                                                                                // }
                                                                                
                                                                                
                                                                                },cellClick:function(e, cell){
                                                                                //e - the click event object
                                                                                //cell - cell component
                                                                                console.log("click time active");
                                                                                console.log(cell.getRow().getData().sort_id);
                                                                                var timeRef = db.collection("restaurants").doc(user.uid).collection("hours").doc(cell.getRow().getData().sort_id);
                                                                                
                                                                                timeRef.update({
                                                                                               hour_is_active: !cell.getValue()
                                                                                               })
                                                                                .then(function() {
                                                                                      console.log("Cell Active successfully updated!");
                                                                                      // cell.setValue(!cell.getValue(), true);
                                                                                      })
                                                                                .catch(function(error) {
                                                                                       // The document probably doesn't exist.
                                                                                       console.error("Error updating document: ", error);
                                                                                       });
                                                                                
                                                                                
                                                                                // cell.setValue(!cell.getValue(), true);
                                                                                
                                                                                }
                                                                                },
                                                                                {title:"Hour", field:"id"},
                                                                                {title:"Edit Details", field:"edit_details", formatter:function(cell, formatterParams, onRendered){
                                                                                //cell - the cell component
                                                                                //formatterParams - parameters set for the column
                                                                                //onRendered - function to call when the formatter has been rendered
                                                                              //  return "<button type=\"button\" href=\"#popup1\" class=\"btn cur-p btn-outline-primary\">Edit Details</button>"
                                                                               
                                                                              return "<a class=\"btn cur-p btn-outline-primary\" href=\"#popup1\">Edit Details</a>"


                                                                                },
                                                                                
                                                                                cellClick:function(e, cell){
                                                                                console.log("whowowhi");
                                                                            
                                                                                
                                                                                
                                                                                //Create Date Editor
                                                                                var dateEditor = function(cell, onRendered, success, cancel){
                                                                                //cell - the cell component for the editable cell
                                                                                //onRendered - function to call when the editor has been rendered
                                                                                //success - function to call to pass the successfuly updated value to Tabulator
                                                                                //cancel - function to call to abort the edit and return to a normal cell
                                                                                
                                                                                //create and style input
                                                                                var cellValue = moment(cell.getValue(), "DD/MM/YYYY").format("YYYY-MM-DD"),
                                                                                input = document.createElement("input");
                                                                                
                                                                                input.setAttribute("type", "date");
                                                                                
                                                                                input.style.padding = "4px";
                                                                                input.style.width = "100%";
                                                                                input.style.boxSizing = "border-box";
                                                                                
                                                                                input.value = cellValue;
                                                                                
                                                                                onRendered(function(){
                                                                                           input.focus();
                                                                                           input.style.height = "100%";
                                                                                           });
                                                                                
                                                                                function onChange(){
                                                                                if(input.value != cellValue){
                                                                                success(moment(input.value, "YYYY-MM-DD").format("DD/MM/YYYY"));
                                                                                }else{
                                                                                cancel();
                                                                                }
                                                                                }
                                                                                
                                                                                //submit new value on blur or change
                                                                                input.addEventListener("blur", onChange);
                                                                                
                                                                                //submit new value on enter
                                                                                input.addEventListener("keydown", function(e){
                                                                                                       if(e.keyCode == 13){
                                                                                                       onChange();
                                                                                                       }
                                                                                                       
                                                                                                       if(e.keyCode == 27){
                                                                                                       cancel();
                                                                                                       }
                                                                                                       });
                                                                                
                                                                                return input;
                                                                                };

                                                                                
                                                                                var tabledata = [
                                                                                                 {id:1, name:"Pasta", salesprice:10, cost:4, profit:2 },
                                                                                                 {id:2, name:"Pizza", salesprice:10, cost:4, profit:2 },
                                                                                                 {id:3, name:"Paneer", salesprice:10, cost:4, profit:2 },
                                                                                                 {id:4, name:"Dal", salesprice:10, cost:4, profit:2 },
                                                                                                 {id:5, name:"Bhindi", salesprice:10, cost:4, profit:2 },
                                                                                                 ];
                                                                                
                                                                                //Build Tabulator
                                                                                var table = new Tabulator("#example-table", {
                                                                                                          height:"800spx",
                                                                                                          layout:"fitColumns",
                                                                                                          addRowPos:"bottom",
                                                                                                          reactiveData:true, //turn on data reactivity
                                                                                                          data:tabledata, //load data into table
                                                                                                          columns:[
                                                                                                                   {formatter:"buttonCross", width:40, align:"center", cellClick:function(e, cell){
                                                                                                                   cell.getRow().delete();
                                                                                                                   }},
                                                                                                                   {title:"Item Name", field:"name", sorter:"string", editor:"input"},
                                                                                                                     {title:"Sales Price", field:"salesprice", sorter:"number", editor:"input"},
                                                                                                                   {title:"Cost of Ingredients", field:"cost", sorter:"number", editor:"input"},
                                                                                                                        {title:"Profit", field:"profit", sorter:"number", editor:"input"},
                                                                                                                   ],
                                                                                                          });
                                     
                                                                                $("#add-row").click(function(){
                                                                                                    $("#example-table").tabulator("addRow", {});
                                                                                                    });

                                                                                

                                                                                
                                                                                var tabledatatwo = [
                                                                                                 {id:1, payroll:50, overhead:40, ccf:0.3, ccp:0.02 },
                                                                                                 ];
                                                                                
                                                                                //Build Tabulator
                                                                                var table = new Tabulator("#example-table-two", {
                                                                                                          height:"800spx",
                                                                                                          layout:"fitColumns",
                                                                                                          reactiveData:true, //turn on data reactivity
                                                                                                          data:tabledatatwo, //load data into table
                                                                                                          columns:[
                                                                                                                   {title:"Hourly Payroll", field:"payroll", sorter:"string", editor:"input"},
                                                                                                                   {title:"Hourly Overhead Costs", field:"overhead", sorter:"number", editor:"input"},
                                                                                                                   {title:"Credit Card Fixed Fee", field:"ccf", sorter:"number", editor:"input"},
                                                                                                                   {title:"Credit Card Percentage Fee", field:"ccp", sorter:"number", editor:"input"},
                                                                                                                   
                                                                                                                   ],
                                                                                                          });
                                                                                
                                                                                }
                                                                                },
                                                                                
                                                                               
                                                                                
                                                                                
                                                                                {title:"Starting Discount %", field:"starting_discount", formatter:function(cell, formatterParams, onRendered){
                                                                                //cell - the cell component
                                                                                //formatterParams - parameters set for the column
                                                                                //onRendered - function to call when the formatter has been rendered
                                                                                return "<input type=\"number\" min=\"0\" max=\"100\" name=\"set_discount\" value=\"" + cell.getValue() + "\">"
                                                                                
                                                                                }},
                                                                                ],
                                                                       rowClick:function(e, row){ //trigger an alert message when the row is clicked
                                                                       //  alert("Row " + row.getData().id + " Clicked!!!!");
                                                                       console.log("Row " + row.getData().id + " Clicked!!!!");
                                                                       },
                                                                       });
                                       
                                       
                                       $('#m_loading').show();
                                       $('#all_slider_message').hide();
                                       $('#s_all_active').hide();
                                       
                                       $('#s_all_active').change(function() {
                                                                 console.log("all slider");
                                                                 console.log(this);
                                                                 
                                                                 var allRef = db.collection("restaurants").doc(user.uid);
                                                                 var statusActive = this.checked;
                                                                 allRef.update({
                                                                               all_discounts_active: statusActive
                                                                               })
                                                                 .then(function() {
                                                                       console.log("Active successfully updated!");
                                                                       if(statusActive) {
                                                                       //Do stuff
                                                                       // console.log("checked!");
                                                                       $('#all_slider_message').text("Discounts Live").show();
                                                                       }
                                                                       else{
                                                                       $('#all_slider_message').text("Discounts Disabled").show();
                                                                       }
                                                                       })
                                                                 .catch(function(error) {
                                                                        // The document probably doesn't exist.
                                                                        console.error("Error updating document: ", error);
                                                                        });
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 });
                                       
                                       var resRef = db.collection("restaurants").doc(user.uid);
                                       
                                       resRef.get().then(function(doc) {
                                                         if (doc.exists) {
                                                         console.log("Document data:", doc.data());
                                                         
                                                         
                                                         var hoursRef = db.collection("restaurants").doc(user.uid).collection("hours");
                                                         var opHours = doc.data().op_hours;
                                                         var opening = parseInt(opHours.substring(0, 2));
                                                         var closing = parseInt(opHours.substring(3, 5));
                                                         console.log(opening);
                                                         console.log(closing);
                                                         
                                                         var query = hoursRef.where("start_id", ">=", opening).where("start_id", "<", closing)
                                                         
                                                         query.get()
                                                         .then(function(querySnapshot) {
                                                               console.log("got em");
                                                               querySnapshot.forEach(function(doc) {
                                                                                     
                                                                                     console.log(doc.id, " => ", doc.data());
                                                                                     
                                                                                     var startingDisc = 0;
                                                                                     for(var i = 0; i < doc.data().discounts.length; i++){
                                                                                     
                                                                                     if(doc.data().discounts[i].is_active == true){
                                                                                     startingDisc = doc.data().discounts[i].percent_discount;
                                                                                     break;
                                                                                     }
                                                                                     }
                                                                                     //  console.log(startingDisc);
                                                                                     var timeId = 0;
                                                                                     if(doc.id < 10){
                                                                                     timeId = tConvert("0" + doc.id + ":00");
                                                                                     }
                                                                                     else{
                                                                                     timeId = tConvert(doc.id + ":00");
                                                                                     }
                                                                                     
                                                                                     var hour = {
                                                                                     sort_id: doc.id,
                                                                                     id: timeId,
                                                                                     edit_details: "Edit Details",
                                                                                     starting_discount: startingDisc,
                                                                                     active: doc.data().hour_is_active,
                                                                                     }
                                                                                     
                                                                                     
                                                                                     manageData.push(hour);
                                                                                     
                                                                                     
                                                                                     });
                                                               
                                                               
                                                               
                                                               tableManage.setSort("sort_id", "asc");
                                                               $('#m_loading').hide();
                                                               $('#s_all_active').prop("checked", doc.data().all_discounts_active);
                                                               if(doc.data().all_discounts_active == true) {
                                                               //Do stuff
                                                               // console.log("checked!");
                                                               $('#all_slider_message').text("Discounts Live").show();
                                                               }
                                                               else{
                                                               $('#all_slider_message').text("Discounts Disabled").show();
                                                               }
                                                               
                                                               });
                                                         
                                                         
                                                         
                                                         } else {
                                                         // doc.data() will be undefined in this case
                                                         console.log("No such document!");
                                                         }
                                                         }).catch(function(error) {
                                                                  console.log("Error getting document:", error);
                                                                  });
                                       
                                       }
                                       
                                       
                                       
                                       
                                       if(document.URL.indexOf("index.html") != -1){
                                       
                                       // display table:
                                       
                                       //create Tabulator on DOM element with id "example-table"
                                       var incomingOrdersData = [];
                                       
                                       var tableIncoming = new Tabulator("#incoming-table", {
                                                                         height:"100%", // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
                                                                         reactiveData:true, //enable reactive data
                                                                         data:incomingOrdersData, //assign data to table
                                                                         layout:"fitColumns", //fit columns to width of table (optional)
                                                                         columns:[ //DeffitDataine Table Columns
                                                                                  {formatter:"rownum", align:"center", width:40},
                                                                                  {title:"Order Number", field:"id"},
                                                                                  {title:"Order Placed At", field:"placed_at"},
                                                                                  {title:"Order Active Between", field:"active_between"},
                                                                                  {title:"Current Price $CAD", field:"current_price", sorter:"string"},
                                                                                  {title:"Status Ready", field:"status", formatter:"tickCross", editor:true, align:"center", sorter:"boolean", cellEdited:function(cell){
                                                                                  //cell - cell component
                                                                                  ready_food(db, user, cell)
                                                                                  }},
                                                                                  ],
                                                                         rowFormatter:function(row){
                                                                         //create and style holder elements
                                                                         var holderEl = document.createElement("div");
                                                                         var tableEl = document.createElement("div");
                                                                         
                                                                         holderEl.style.boxSizing = "border-box";
                                                                         holderEl.style.padding = "10px 30px 10px 10px";
                                                                         holderEl.style.borderTop = "1px solid #333";
                                                                         holderEl.style.borderBotom = "1px solid #333";
                                                                         holderEl.style.background = "#ddd";
                                                                         
                                                                         tableEl.style.border = "1px solid #333";
                                                                         
                                                                         holderEl.appendChild(tableEl);
                                                                         
                                                                         row.getElement().appendChild(holderEl);
                                                                         
                                                                         var subTable = new Tabulator(tableEl, {
                                                                                                      layout:"fitColumns",
                                                                                                      data:row.getData().items,
                                                                                                      columns:[
                                                                                                               {title:"Food Name", field:"name"},
                                                                                                               {title:"Quantity", field:"quantity"},
                                                                                                               {title:"Price", field:"initial_price"},
                                                                                                               {title:"Toppings", field:"toppings"},
                                                                                                               {title:"Comments", field:"comments"},
                                                                                                               ]
                                                                                                      })
                                                                         },
                                                                         rowClick:function(e, row){ //trigger an alert message when the row is clicked
                                                                         //  alert("Row " + row.getData().id + " Clicked!!!!");
                                                                         console.log("Row " + row.getData().id + " Clicked!!!!");
                                                                         },
                                                                         });
                                       
                                       //Trigger sort when "Trigger Sort" button is clicked
                                       $("#sort-trigger").click(function(){
                                                                tableIncoming.setSort($("#sort-field").val(), $("#sort-direction").val());
                                                                });
                                       
                                       var totalOrdersListener = db.collection("restaurants").doc(user.uid).collection("private").doc(user.uid);
                                       
                                       totalOrdersListener.onSnapshot(function(doc) {
                                                                      //console.log("Current data: ", doc.data());
                                                                      // console.log(doc.data().total_orders);
                                                                      
                                                                      console.log("listener for # total orders set");
                                                                      // tableIncoming.clearData();
                                                                      var ordersRef = db.collection("restaurants").doc(user.uid).collection("private").doc(user.uid).collection("orders");
                                                                      var incomingOrdersQuery = ordersRef.where("incoming", "==", true);
                                                                      
                                                                      incomingOrdersQuery.get().then(function(querySnapshot) {
                                                                                                     
                                                                                                     querySnapshot.forEach(function(doc) {
                                                                                                                           // doc.data() is never undefined for query doc snapshots
                                                                                                                           console.log(doc.id, " => ", doc.data());
                                                                                                                           
                                                                                                                           // Order Number, Order Placed At, Order Active Between, Current Price, Items, Toppings, Comments, Status
                                                                                                                           console.log("getting incoming orders")
                                                                                                                           console.log(incomingOrdersData);
                                                                                                                           for(var i = 0; i < incomingOrdersData.length; i++){
                                                                                                                           incomingOrdersData.pop();
                                                                                                                           console.log("popping");
                                                                                                                           }
                                                                                                                           console.log("done popping" + incomingOrdersData.length);
                                                                                                                           
                                                                                                                           var inOrderRef = db.collection("orders").doc(doc.id);
                                                                                                                           
                                                                                                                           inOrderRef.get().then(function(doc) {
                                                                                                                                                 if (doc.exists) {
                                                                                                                                                 console.log("Order data:", doc.data());
                                                                                                                                                 var orderData = doc.data();
                                                                                                                                                 
                                                                                                                                                 var orderHours = pad(orderData.placed_at.toDate().getHours(), 2);
                                                                                                                                                 var orderMins = pad(orderData.placed_at.toDate().getMinutes(), 2);
                                                                                                                                                 var activeHours = tConvert(orderData.hours_order.substring(0, 2) + ":00") + " - " + tConvert(orderData.hours_order.substring(3, 5) + ":00");
                                                                                                                                                 console.log(activeHours);
                                                                                                                                                 
                                                                                                                                                 var an_order = {
                                                                                                                                                 id: orderData.order_id,
                                                                                                                                                 placed_at: tConvert(orderHours + ":" + orderMins),
                                                                                                                                                 active_between: activeHours,
                                                                                                                                                 current_price: orderData.total_price,
                                                                                                                                                 items: orderData.foods,
                                                                                                                                                 status: orderData.status_ready,
                                                                                                                                                 };
                                                                                                                                                 console.log(an_order);
                                                                                                                                                 console.log("show order ^");
                                                                                                                                                 //  incomingOrdersData.push(an_order);
                                                                                                                                                 console.log(incomingOrdersData);
                                                                                                                                                 //table.redraw(true);
                                                                                                                                                 incomingOrdersData.push(an_order);
                                                                                                                                                 
                                                                                                                                                 // console.log('shifted');
                                                                                                                                                 
                                                                                                                                                 } else {
                                                                                                                                                 // doc.data() will be undefined in this case
                                                                                                                                                 console.log("No such document!");
                                                                                                                                                 }
                                                                                                                                                 }).catch(function(error) {
                                                                                                                                                          console.log("Error getting document:", error);
                                                                                                                                                          });
                                                                                                                           
                                                                                                                           
                                                                                                                           
                                                                                                                           });
                                                                                                     })
                                                                      .catch(function(error) {
                                                                             console.log("Error getting documents: ", error);
                                                                             });
                                                                      
                                                                      });
                                       
                                       }
                                       
                                       
                                       if(document.URL.indexOf("history.html") != -1){
                                       
                                       // display table:
                                       
                                       //create Tabulator on DOM element with id "example-table"
                                       var allOrdersData = [];
                                       
                                       var tableAll = new Tabulator("#history-table", {
                                                                    height:"100%", // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
                                                                    reactiveData:true, //enable reactive data
                                                                    data:allOrdersData, //assign data to table
                                                                    layout:"fitColumns", //fit columns to width of table (optional)
                                                                    columns:[ //DeffitDataine Table Columns
                                                                             {formatter:"rownum", align:"center", width:20},
                                                                             {title:"Order Number", field:"id"},
                                                                             {title:"Order Placed At", field:"placed_at"},
                                                                             {title:"Order Active Between", field:"active_between"},
                                                                             {title:"Current Price $CAD", field:"current_price", sorter:"string"},
                                                                             {title:"Status Ready", field:"status", formatter:"tickCross", align:"center", sorter:"boolean"},
                                                                             ],
                                                                    rowFormatter:function(row){
                                                                    //create and style holder elements
                                                                    var holderEl = document.createElement("div");
                                                                    var tableEl = document.createElement("div");
                                                                    
                                                                    holderEl.style.boxSizing = "border-box";
                                                                    holderEl.style.padding = "10px 30px 10px 10px";
                                                                    holderEl.style.borderTop = "1px solid #333";
                                                                    holderEl.style.borderBotom = "1px solid #333";
                                                                    holderEl.style.background = "#ddd";
                                                                    
                                                                    tableEl.style.border = "1px solid #333";
                                                                    
                                                                    holderEl.appendChild(tableEl);
                                                                    
                                                                    row.getElement().appendChild(holderEl);
                                                                    
                                                                    var subTable = new Tabulator(tableEl, {
                                                                                                 layout:"fitColumns",
                                                                                                 data:row.getData().items,
                                                                                                 columns:[
                                                                                                          {title:"Food Name", field:"name"},
                                                                                                          {title:"Quantity", field:"quantity"},
                                                                                                          {title:"Price", field:"initial_price"},
                                                                                                          {title:"Toppings", field:"toppings"},
                                                                                                          {title:"Comments", field:"comments"},
                                                                                                          ]
                                                                                                 })
                                                                    },
                                                                    rowClick:function(e, row){ //trigger an alert message when the row is clicked
                                                                    //  alert("Row " + row.getData().id + " Clicked!!!!");
                                                                    console.log("Row " + row.getData().id + " Clicked!!!!");
                                                                    },
                                                                    });
                                       
                                       //Trigger sort when "Trigger Sort" button is clicked
                                       $("#sort-trigger").click(function(){
                                                                tableAll.setSort($("#sort-field").val(), $("#sort-direction").val());
                                                                });
                                       
                                       var totalOrdersListener = db.collection("restaurants").doc(user.uid).collection("private").doc(user.uid);
                                       
                                       totalOrdersListener.onSnapshot(function(doc) {
                                                                      //console.log("Current data: ", doc.data());
                                                                      // console.log(doc.data().total_orders);
                                                                      
                                                                      console.log("listener for # total orders set");
                                                                      // tableIncoming.clearData();
                                                                      var ordersRef = db.collection("restaurants").doc(user.uid).collection("private").doc(user.uid).collection("orders");
                                                                      
                                                                      ordersRef.get().then(function(querySnapshot) {
                                                                                           
                                                                                           querySnapshot.forEach(function(doc) {
                                                                                                                 // doc.data() is never undefined for query doc snapshots
                                                                                                                 console.log(doc.id, " => ", doc.data());
                                                                                                                 
                                                                                                                 // Order Number, Order Placed At, Order Active Between, Current Price, Items, Toppings, Comments, Status
                                                                                                                 console.log("getting incoming orders")
                                                                                                                 console.log(allOrdersData);
                                                                                                                 for(var i = 0; i < allOrdersData.length; i++){
                                                                                                                 allOrdersData.pop();
                                                                                                                 console.log("popping");
                                                                                                                 }
                                                                                                                 console.log("done popping" + allOrdersData.length);
                                                                                                                 
                                                                                                                 var inOrderRef = db.collection("orders").doc(doc.id);
                                                                                                                 
                                                                                                                 inOrderRef.get().then(function(doc) {
                                                                                                                                       if (doc.exists) {
                                                                                                                                       console.log("Order data:", doc.data());
                                                                                                                                       var orderData = doc.data();
                                                                                                                                       
                                                                                                                                       var orderHours = pad(orderData.placed_at.toDate().getHours(), 2);
                                                                                                                                       var orderMins = pad(orderData.placed_at.toDate().getMinutes(), 2);
                                                                                                                                       var activeHours = tConvert(orderData.hours_order.substring(0, 2) + ":00") + " - " + tConvert(orderData.hours_order.substring(3, 5) + ":00");
                                                                                                                                       console.log(activeHours);
                                                                                                                                       
                                                                                                                                       var an_order = {
                                                                                                                                       id: orderData.order_id,
                                                                                                                                       placed_at: tConvert(orderHours + ":" + orderMins),
                                                                                                                                       active_between: activeHours,
                                                                                                                                       current_price: orderData.total_price,
                                                                                                                                       items: orderData.foods,
                                                                                                                                       status: orderData.status_ready,
                                                                                                                                       };
                                                                                                                                       console.log(an_order);
                                                                                                                                       console.log("show order ^");
                                                                                                                                       //  incomingOrdersData.push(an_order);
                                                                                                                                       console.log(allOrdersData);
                                                                                                                                       //table.redraw(true);
                                                                                                                                       allOrdersData.push(an_order);
                                                                                                                                       
                                                                                                                                       // console.log('shifted');
                                                                                                                                       
                                                                                                                                       } else {
                                                                                                                                       // doc.data() will be undefined in this case
                                                                                                                                       console.log("No such document!");
                                                                                                                                       }
                                                                                                                                       }).catch(function(error) {
                                                                                                                                                console.log("Error getting document:", error);
                                                                                                                                                });
                                                                                                                 
                                                                                                                 
                                                                                                                 
                                                                                                                 });
                                                                                           })
                                                                      .catch(function(error) {
                                                                             console.log("Error getting documents: ", error);
                                                                             });
                                                                      
                                                                      });
                                       
                                       }
                                       
                                       
                                       
                                       // ...
                                       } else {
                                       // User is signed out.
                                       // ...
                                       if(document.URL.indexOf("signin.html") == -1 && document.URL.indexOf("signup.html") == -1){
                                       window.location.href = "signin.html";
                                       }
                                       
                                       }
                                       });
    
}

function discountsSwitch(event){
    console.log(event);
    console.log("disc");
}

function ready_food(db, user, cell){
    console.log(cell);
    console.log(cell.getRow().getData().id);
    
    // set status of food to ready:
    var orderUpdateRef = db.collection("orders").doc("wbc_transc_" + cell.getRow().getData().id);
    var incomingUpdateRef = db.collection("restaurants").doc(user.uid).collection("private").doc(user.uid).collection("orders").doc("wbc_transc_" + cell.getRow().getData().id);
    
    orderUpdateRef.update({
                          "status_ready": cell.getValue(),
                          })
    .then(function() {
          //  console.log("Status successfully updated!");
          incomingUpdateRef.update({
                                   "incoming": !cell.getValue(),
                                   })
          .then(function() {
                console.log("Status successfully updated!");
                });
          });
    
}

function logoutUser(){
    
    firebase.auth().signOut().then(function() {
                                   // Sign-out successful.
                                   setTimeout( function() {
                                              // code that must be executed after pause
                                              window.location.href = "signin.html";
                                              }, 1000 );
                                   }, function(error) {
                                   // An error happened.
                                   });
    
}

function registerUser(db){
    console.log("registering...");
    
    var name = $('#r_name').val();
    var email = $('#r_email').val();
    var trofi_code = $('#trofi_code').val();
    var password = $('#r_password').val();
    var c_password = $('#r_confirm_password').val();
    
    if (name === "" || email === "" || trofi_code === "" || password === "" || c_password === "") {
        $('#r_err_message').text("All fields must be filled in!").show();
    }
    else if(password != c_password){
        $('#r_err_message').text("Passwords do not match!").show();
    }
    else{
        
        var codeRef = db.collection("general").doc("trofi-verification");
        
        codeRef.get().then(function(doc) {
                           if (doc.exists) {
                           console.log("Document data:", doc.data());
                           if(doc.data().accepted_codes.includes(trofi_code) == true){
                           
                           //  console.log("verified");
                           
                           firebase.auth().createUserWithEmailAndPassword(email, password).then(function(){
                                                                                                
                                                                                                // firestore create user
                                                                                                var user = firebase.auth().currentUser;
                                                                                                $('#r_err_message').hide();
                                                                                                $('#r_succ_message').text("Creating restaurant profile...").show();
                                                                                                $('#r_loading').show();
                                                                                                
                                                                                                const resRef = db.collection("restaurants").doc(user.uid);
                                                                                                const resPrivateRef = resRef.collection('private').doc(user.uid);
                                                                                                
                                                                                                const moreInfoRef = resRef.collection('more-info').doc('details');
                                                                                                const logsRef = resRef.collection('logs');
                                                                                                
                                                                                                const initHoursRef = resRef.collection('hours');
                                                                                                const init0HoursRef = initHoursRef.doc("0");
                                                                                                const init1HoursRef = initHoursRef.doc("1");
                                                                                                const init2HoursRef = initHoursRef.doc("2");
                                                                                                const init3HoursRef = initHoursRef.doc("3");
                                                                                                const init4HoursRef = initHoursRef.doc("4");
                                                                                                const init5HoursRef = initHoursRef.doc("5");
                                                                                                const init6HoursRef = initHoursRef.doc("6");
                                                                                                const init7HoursRef = initHoursRef.doc("7");
                                                                                                const init8HoursRef = initHoursRef.doc("8");
                                                                                                const init9HoursRef = initHoursRef.doc("9");
                                                                                                const init10HoursRef = initHoursRef.doc("10");
                                                                                                const init11HoursRef = initHoursRef.doc("11");
                                                                                                const init12HoursRef = initHoursRef.doc("12");
                                                                                                const init13HoursRef = initHoursRef.doc("13");
                                                                                                const init14HoursRef = initHoursRef.doc("14");
                                                                                                const init15HoursRef = initHoursRef.doc("15");
                                                                                                const init16HoursRef = initHoursRef.doc("16");
                                                                                                const init17HoursRef = initHoursRef.doc("17");
                                                                                                const init18HoursRef = initHoursRef.doc("18");
                                                                                                const init19HoursRef = initHoursRef.doc("19");
                                                                                                const init20HoursRef = initHoursRef.doc("20");
                                                                                                const init21HoursRef = initHoursRef.doc("21");
                                                                                                const init22HoursRef = initHoursRef.doc("22");
                                                                                                const init23HoursRef = initHoursRef.doc("23");
                                                                                                
                                                                                                
                                                                                                
                                                                                                resPrivateRef.get().then(function(doc) {
                                                                                                                         if (doc.exists) {
                                                                                                                         console.log("Document data:", doc.data());
                                                                                                                         
                                                                                                                         } else {
                                                                                                                         // doc.data() will be undefined in this case
                                                                                                                         //  console.log("No such document!");
                                                                                                                         
                                                                                                                         // Add a new document in collection "cities"
                                                                                                                         resRef.set({
                                                                                                                                    all_discounts_active: false,
                                                                                                                                    restaurant_name: "",
                                                                                                                                    restaurant_logo: "",
                                                                                                                                    menu: [],
                                                                                                                                    })
                                                                                                                         .then(function() {
                                                                                                                               //console.log("Document successfully written!");
                                                                                                                               
                                                                                                                               resPrivateRef.set({
                                                                                                                                                 accepted_code: trofi_code,
                                                                                                                                                 name: name,
                                                                                                                                                 allow_in: false,
                                                                                                                                                 payment_id: "",
                                                                                                                                                 total_orders: 0,
                                                                                                                                                 credit_card_percentage: 0,
                                                                                                                                                 credit_card_constant: 0,
                                                                                                                                                 orders: [],
                                                                                                                                                 })
                                                                                                                               .then(function() {
                                                                                                                                     // console.log("Document successfully written!");
                                                                                                                                     
                                                                                                                                     init0HoursRef.set({
                                                                                                                                                       start_id: 0,
                                                                                                                                                       operating_cost: 0,
                                                                                                                                                       current_contributed: 0,
                                                                                                                                                       hour_is_active: false,
                                                                                                                                                       discounts: [ {
                                                                                                                                                                   is_active: true,
                                                                                                                                                                   percent_discount: 0,
                                                                                                                                                                   needed_contribution: 0,
                                                                                                                                                                   }
                                                                                                                                                                   ],
                                                                                                                                                       foods_active: []
                                                                                                                                                       })
                                                                                                                                     .then(function() {
                                                                                                                                           //  console.log("Document successfully written!");
                                                                                                                                           
                                                                                                                                           init1HoursRef.set({
                                                                                                                                                             start_id: 1,
                                                                                                                                                             operating_cost: 0,
                                                                                                                                                             current_contributed: 0,
                                                                                                                                                             hour_is_active: false,
                                                                                                                                                             discounts: [ {
                                                                                                                                                                         is_active: true,
                                                                                                                                                                         percent_discount: 0,
                                                                                                                                                                         needed_contribution: 0,
                                                                                                                                                                         }
                                                                                                                                                                         ],
                                                                                                                                                             foods_active: []
                                                                                                                                                             })
                                                                                                                                           .then(function() {
                                                                                                                                                 //  console.log("Document successfully written!");
                                                                                                                                                 
                                                                                                                                                 init2HoursRef.set({
                                                                                                                                                                   start_id: 2,
                                                                                                                                                                   operating_cost: 0,
                                                                                                                                                                   current_contributed: 0,
                                                                                                                                                                   hour_is_active: false,
                                                                                                                                                                   discounts: [ {
                                                                                                                                                                               is_active: true,
                                                                                                                                                                               percent_discount: 0,
                                                                                                                                                                               needed_contribution: 0,
                                                                                                                                                                               }
                                                                                                                                                                               ],
                                                                                                                                                                   foods_active: []
                                                                                                                                                                   })
                                                                                                                                                 .then(function() {
                                                                                                                                                       //  console.log("Document successfully written!");
                                                                                                                                                       
                                                                                                                                                       init3HoursRef.set({
                                                                                                                                                                         start_id: 3,
                                                                                                                                                                         operating_cost: 0,
                                                                                                                                                                         current_contributed: 0,
                                                                                                                                                                         hour_is_active: false,
                                                                                                                                                                         discounts: [ {
                                                                                                                                                                                     is_active: true,
                                                                                                                                                                                     percent_discount: 0,
                                                                                                                                                                                     needed_contribution: 0,
                                                                                                                                                                                     }
                                                                                                                                                                                     ],
                                                                                                                                                                         foods_active: []
                                                                                                                                                                         })
                                                                                                                                                       .then(function() {
                                                                                                                                                             //  console.log("Document successfully written!");
                                                                                                                                                             
                                                                                                                                                             init4HoursRef.set({
                                                                                                                                                                               start_id: 4,
                                                                                                                                                                               operating_cost: 0,
                                                                                                                                                                               current_contributed: 0,
                                                                                                                                                                               hour_is_active: false,
                                                                                                                                                                               discounts: [ {
                                                                                                                                                                                           is_active: true,
                                                                                                                                                                                           percent_discount: 0,
                                                                                                                                                                                           needed_contribution: 0,
                                                                                                                                                                                           }
                                                                                                                                                                                           ],
                                                                                                                                                                               foods_active: []
                                                                                                                                                                               })
                                                                                                                                                             .then(function() {
                                                                                                                                                                   //  console.log("Document successfully written!");
                                                                                                                                                                   
                                                                                                                                                                   init5HoursRef.set({
                                                                                                                                                                                     start_id: 5,
                                                                                                                                                                                     operating_cost: 0,
                                                                                                                                                                                     current_contributed: 0,
                                                                                                                                                                                     hour_is_active: false,
                                                                                                                                                                                     discounts: [ {
                                                                                                                                                                                                 is_active: true,
                                                                                                                                                                                                 percent_discount: 0,
                                                                                                                                                                                                 needed_contribution: 0,
                                                                                                                                                                                                 }
                                                                                                                                                                                                 ],
                                                                                                                                                                                     foods_active: []
                                                                                                                                                                                     })
                                                                                                                                                                   .then(function() {
                                                                                                                                                                         //  console.log("Document successfully written!");
                                                                                                                                                                         
                                                                                                                                                                         init6HoursRef.set({
                                                                                                                                                                                           start_id: 6,
                                                                                                                                                                                           operating_cost: 0,
                                                                                                                                                                                           current_contributed: 0,
                                                                                                                                                                                           hour_is_active: false,
                                                                                                                                                                                           discounts: [ {
                                                                                                                                                                                                       is_active: true,
                                                                                                                                                                                                       percent_discount: 0,
                                                                                                                                                                                                       needed_contribution: 0,
                                                                                                                                                                                                       }
                                                                                                                                                                                                       ],
                                                                                                                                                                                           foods_active: []
                                                                                                                                                                                           })
                                                                                                                                                                         .then(function() {
                                                                                                                                                                               //  console.log("Document successfully written!");
                                                                                                                                                                               
                                                                                                                                                                               init7HoursRef.set({
                                                                                                                                                                                                 start_id: 7,
                                                                                                                                                                                                 operating_cost: 0,
                                                                                                                                                                                                 current_contributed: 0,
                                                                                                                                                                                                 hour_is_active: false,
                                                                                                                                                                                                 discounts: [ {
                                                                                                                                                                                                             is_active: true,
                                                                                                                                                                                                             percent_discount: 0,
                                                                                                                                                                                                             needed_contribution: 0,
                                                                                                                                                                                                             }
                                                                                                                                                                                                             ],
                                                                                                                                                                                                 foods_active: []
                                                                                                                                                                                                 })
                                                                                                                                                                               .then(function() {
                                                                                                                                                                                     //  console.log("Document successfully written!");
                                                                                                                                                                                     
                                                                                                                                                                                     init8HoursRef.set({
                                                                                                                                                                                                       start_id: 8,
                                                                                                                                                                                                       operating_cost: 0,
                                                                                                                                                                                                       current_contributed: 0,
                                                                                                                                                                                                       hour_is_active: false,
                                                                                                                                                                                                       discounts: [ {
                                                                                                                                                                                                                   is_active: true,
                                                                                                                                                                                                                   percent_discount: 0,
                                                                                                                                                                                                                   needed_contribution: 0,
                                                                                                                                                                                                                   }
                                                                                                                                                                                                                   ],
                                                                                                                                                                                                       foods_active: []
                                                                                                                                                                                                       })
                                                                                                                                                                                     .then(function() {
                                                                                                                                                                                           //  console.log("Document successfully written!");
                                                                                                                                                                                           
                                                                                                                                                                                           init9HoursRef.set({
                                                                                                                                                                                                             start_id: 9,
                                                                                                                                                                                                             operating_cost: 0,
                                                                                                                                                                                                             current_contributed: 0,
                                                                                                                                                                                                             hour_is_active: false,
                                                                                                                                                                                                             discounts: [ {
                                                                                                                                                                                                                         is_active: true,
                                                                                                                                                                                                                         percent_discount: 0,
                                                                                                                                                                                                                         needed_contribution: 0,
                                                                                                                                                                                                                         }
                                                                                                                                                                                                                         ],
                                                                                                                                                                                                             foods_active: []
                                                                                                                                                                                                             })
                                                                                                                                                                                           .then(function() {
                                                                                                                                                                                                 //  console.log("Document successfully written!");
                                                                                                                                                                                                 
                                                                                                                                                                                                 init10HoursRef.set({
                                                                                                                                                                                                                    start_id: 10,
                                                                                                                                                                                                                    operating_cost: 0,
                                                                                                                                                                                                                    current_contributed: 0,
                                                                                                                                                                                                                    hour_is_active: false,
                                                                                                                                                                                                                    discounts: [ {
                                                                                                                                                                                                                                is_active: true,
                                                                                                                                                                                                                                percent_discount: 0,
                                                                                                                                                                                                                                needed_contribution: 0,
                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                ],
                                                                                                                                                                                                                    foods_active: []
                                                                                                                                                                                                                    })
                                                                                                                                                                                                 .then(function() {
                                                                                                                                                                                                       // console.log("Document successfully written!");
                                                                                                                                                                                                       
                                                                                                                                                                                                       init11HoursRef.set({
                                                                                                                                                                                                                          start_id: 11,
                                                                                                                                                                                                                          operating_cost: 0,
                                                                                                                                                                                                                          current_contributed: 0,
                                                                                                                                                                                                                          hour_is_active: false,
                                                                                                                                                                                                                          discounts: [ {
                                                                                                                                                                                                                                      is_active: true,
                                                                                                                                                                                                                                      percent_discount: 0,
                                                                                                                                                                                                                                      needed_contribution: 0,
                                                                                                                                                                                                                                      }
                                                                                                                                                                                                                                      ],
                                                                                                                                                                                                                          foods_active: []
                                                                                                                                                                                                                          })
                                                                                                                                                                                                       .then(function() {
                                                                                                                                                                                                             // console.log("Document successfully written!");
                                                                                                                                                                                                             
                                                                                                                                                                                                             init12HoursRef.set({
                                                                                                                                                                                                                                start_id: 12,
                                                                                                                                                                                                                                operating_cost: 0,
                                                                                                                                                                                                                                current_contributed: 0,
                                                                                                                                                                                                                                hour_is_active: false,
                                                                                                                                                                                                                                discounts: [ {
                                                                                                                                                                                                                                            is_active: true,
                                                                                                                                                                                                                                            percent_discount: 0,
                                                                                                                                                                                                                                            needed_contribution: 0,
                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                            ],
                                                                                                                                                                                                                                foods_active: []
                                                                                                                                                                                                                                })
                                                                                                                                                                                                             .then(function() {
                                                                                                                                                                                                                   // console.log("Document successfully written!");
                                                                                                                                                                                                                   
                                                                                                                                                                                                                   init13HoursRef.set({
                                                                                                                                                                                                                                      start_id: 13,
                                                                                                                                                                                                                                      operating_cost: 0,
                                                                                                                                                                                                                                      current_contributed: 0,
                                                                                                                                                                                                                                      hour_is_active: false,
                                                                                                                                                                                                                                      discounts: [ {
                                                                                                                                                                                                                                                  is_active: true,
                                                                                                                                                                                                                                                  percent_discount: 0,
                                                                                                                                                                                                                                                  needed_contribution: 0,
                                                                                                                                                                                                                                                  }
                                                                                                                                                                                                                                                  ],
                                                                                                                                                                                                                                      foods_active: []
                                                                                                                                                                                                                                      })
                                                                                                                                                                                                                   .then(function() {
                                                                                                                                                                                                                         // console.log("Document successfully written!");
                                                                                                                                                                                                                         
                                                                                                                                                                                                                         init14HoursRef.set({
                                                                                                                                                                                                                                            start_id: 14,
                                                                                                                                                                                                                                            operating_cost: 0,
                                                                                                                                                                                                                                            current_contributed: 0,
                                                                                                                                                                                                                                            hour_is_active: false,
                                                                                                                                                                                                                                            discounts: [ {
                                                                                                                                                                                                                                                        is_active: true,
                                                                                                                                                                                                                                                        percent_discount: 0,
                                                                                                                                                                                                                                                        needed_contribution: 0,
                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                        ],
                                                                                                                                                                                                                                            foods_active: []
                                                                                                                                                                                                                                            })
                                                                                                                                                                                                                         .then(function() {
                                                                                                                                                                                                                               // console.log("Document successfully written!");
                                                                                                                                                                                                                               
                                                                                                                                                                                                                               init15HoursRef.set({
                                                                                                                                                                                                                                                  start_id: 15,
                                                                                                                                                                                                                                                  operating_cost: 0,
                                                                                                                                                                                                                                                  current_contributed: 0,
                                                                                                                                                                                                                                                  hour_is_active: false,
                                                                                                                                                                                                                                                  discounts: [ {
                                                                                                                                                                                                                                                              is_active: true,
                                                                                                                                                                                                                                                              percent_discount: 0,
                                                                                                                                                                                                                                                              needed_contribution: 0,
                                                                                                                                                                                                                                                              }
                                                                                                                                                                                                                                                              ],
                                                                                                                                                                                                                                                  foods_active: []
                                                                                                                                                                                                                                                  })
                                                                                                                                                                                                                               .then(function() {
                                                                                                                                                                                                                                     // console.log("Document successfully written!");
                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                     init16HoursRef.set({
                                                                                                                                                                                                                                                        start_id: 16,
                                                                                                                                                                                                                                                        operating_cost: 0,
                                                                                                                                                                                                                                                        current_contributed: 0,
                                                                                                                                                                                                                                                        hour_is_active: false,
                                                                                                                                                                                                                                                        discounts: [ {
                                                                                                                                                                                                                                                                    is_active: true,
                                                                                                                                                                                                                                                                    percent_discount: 0,
                                                                                                                                                                                                                                                                    needed_contribution: 0,
                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                    ],
                                                                                                                                                                                                                                                        foods_active: []
                                                                                                                                                                                                                                                        })
                                                                                                                                                                                                                                     .then(function() {
                                                                                                                                                                                                                                           // console.log("Document successfully written!");
                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                           init17HoursRef.set({
                                                                                                                                                                                                                                                              start_id: 17,
                                                                                                                                                                                                                                                              operating_cost: 0,
                                                                                                                                                                                                                                                              current_contributed: 0,
                                                                                                                                                                                                                                                              hour_is_active: false,
                                                                                                                                                                                                                                                              discounts: [ {
                                                                                                                                                                                                                                                                          is_active: true,
                                                                                                                                                                                                                                                                          percent_discount: 0,
                                                                                                                                                                                                                                                                          needed_contribution: 0,
                                                                                                                                                                                                                                                                          }
                                                                                                                                                                                                                                                                          ],
                                                                                                                                                                                                                                                              foods_active: []
                                                                                                                                                                                                                                                              })
                                                                                                                                                                                                                                           .then(function() {
                                                                                                                                                                                                                                                 // console.log("Document successfully written!");
                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                 init18HoursRef.set({
                                                                                                                                                                                                                                                                    start_id: 18,
                                                                                                                                                                                                                                                                    operating_cost: 0,
                                                                                                                                                                                                                                                                    current_contributed: 0,
                                                                                                                                                                                                                                                                    hour_is_active: false,
                                                                                                                                                                                                                                                                    discounts: [ {
                                                                                                                                                                                                                                                                                is_active: true,
                                                                                                                                                                                                                                                                                percent_discount: 0,
                                                                                                                                                                                                                                                                                needed_contribution: 0,
                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                ],
                                                                                                                                                                                                                                                                    foods_active: []
                                                                                                                                                                                                                                                                    })
                                                                                                                                                                                                                                                 .then(function() {
                                                                                                                                                                                                                                                       // console.log("Document successfully written!");
                                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                                       init19HoursRef.set({
                                                                                                                                                                                                                                                                          start_id: 19,
                                                                                                                                                                                                                                                                          operating_cost: 0,
                                                                                                                                                                                                                                                                          current_contributed: 0,
                                                                                                                                                                                                                                                                          hour_is_active: false,
                                                                                                                                                                                                                                                                          discounts: [ {
                                                                                                                                                                                                                                                                                      is_active: true,
                                                                                                                                                                                                                                                                                      percent_discount: 0,
                                                                                                                                                                                                                                                                                      needed_contribution: 0,
                                                                                                                                                                                                                                                                                      }
                                                                                                                                                                                                                                                                                      ],
                                                                                                                                                                                                                                                                          foods_active: []
                                                                                                                                                                                                                                                                          })
                                                                                                                                                                                                                                                       .then(function() {
                                                                                                                                                                                                                                                             // console.log("Document successfully written!");
                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                             init20HoursRef.set({
                                                                                                                                                                                                                                                                                start_id: 20,
                                                                                                                                                                                                                                                                                operating_cost: 0,
                                                                                                                                                                                                                                                                                current_contributed: 0,
                                                                                                                                                                                                                                                                                hour_is_active: false,
                                                                                                                                                                                                                                                                                discounts: [ {
                                                                                                                                                                                                                                                                                            is_active: true,
                                                                                                                                                                                                                                                                                            percent_discount: 0,
                                                                                                                                                                                                                                                                                            needed_contribution: 0,
                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                            ],
                                                                                                                                                                                                                                                                                foods_active: []
                                                                                                                                                                                                                                                                                })
                                                                                                                                                                                                                                                             .then(function() {
                                                                                                                                                                                                                                                                   // console.log("Document successfully written!");
                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                   init21HoursRef.set({
                                                                                                                                                                                                                                                                                      start_id: 21,
                                                                                                                                                                                                                                                                                      operating_cost: 0,
                                                                                                                                                                                                                                                                                      current_contributed: 0,
                                                                                                                                                                                                                                                                                      hour_is_active: false,
                                                                                                                                                                                                                                                                                      discounts: [ {
                                                                                                                                                                                                                                                                                                  is_active: true,
                                                                                                                                                                                                                                                                                                  percent_discount: 0,
                                                                                                                                                                                                                                                                                                  needed_contribution: 0,
                                                                                                                                                                                                                                                                                                  }
                                                                                                                                                                                                                                                                                                  ],
                                                                                                                                                                                                                                                                                      foods_active: []
                                                                                                                                                                                                                                                                                      })
                                                                                                                                                                                                                                                                   .then(function() {
                                                                                                                                                                                                                                                                         // console.log("Document successfully written!");
                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                         init22HoursRef.set({
                                                                                                                                                                                                                                                                                            start_id: 22,
                                                                                                                                                                                                                                                                                            operating_cost: 0,
                                                                                                                                                                                                                                                                                            current_contributed: 0,
                                                                                                                                                                                                                                                                                            hour_is_active: false,
                                                                                                                                                                                                                                                                                            discounts: [ {
                                                                                                                                                                                                                                                                                                        is_active: true,
                                                                                                                                                                                                                                                                                                        percent_discount: 0,
                                                                                                                                                                                                                                                                                                        needed_contribution: 0,
                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                        ],
                                                                                                                                                                                                                                                                                            foods_active: []
                                                                                                                                                                                                                                                                                            })
                                                                                                                                                                                                                                                                         .then(function() {
                                                                                                                                                                                                                                                                               // console.log("Document successfully written!");
                                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                               init23HoursRef.set({
                                                                                                                                                                                                                                                                                                  start_id: 23,
                                                                                                                                                                                                                                                                                                  operating_cost: 0,
                                                                                                                                                                                                                                                                                                  current_contributed: 0,
                                                                                                                                                                                                                                                                                                  hour_is_active: false,
                                                                                                                                                                                                                                                                                                  discounts: [ {
                                                                                                                                                                                                                                                                                                              is_active: true,
                                                                                                                                                                                                                                                                                                              percent_discount: 0,
                                                                                                                                                                                                                                                                                                              needed_contribution: 0,
                                                                                                                                                                                                                                                                                                              }
                                                                                                                                                                                                                                                                                                              ],
                                                                                                                                                                                                                                                                                                  foods_active: []
                                                                                                                                                                                                                                                                                                  })
                                                                                                                                                                                                                                                                               .then(function() {
                                                                                                                                                                                                                                                                                     // console.log("Document successfully written!");
                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                     moreInfoRef.set({
                                                                                                                                                                                                                                                                                                     restaurant_desc: "",
                                                                                                                                                                                                                                                                                                     address: "",
                                                                                                                                                                                                                                                                                                     contact_email: "",
                                                                                                                                                                                                                                                                                                     contact_phone: "",
                                                                                                                                                                                                                                                                                                     })
                                                                                                                                                                                                                                                                                     .then(function() {
                                                                                                                                                                                                                                                                                           //console.log("Document successfully written!");
                                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                           logsRef.doc("00-00-0000").set({
                                                                                                                                                                                                                                                                                                                         discounts: [],
                                                                                                                                                                                                                                                                                                                         })
                                                                                                                                                                                                                                                                                           .then(function() {
                                                                                                                                                                                                                                                                                                 console.log("Restaurant successfully written!");
                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                 firebase.auth().signOut().then(function() {
                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                $('#r_err_message').hide();
                                                                                                                                                                                                                                                                                                                                $('#r_loading').hide();
                                                                                                                                                                                                                                                                                                                                $('#r_succ_message').text("Successfully Registered! Redirecting you to login page...").show();
                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                // Sign-out successful.''
                                                                                                                                                                                                                                                                                                                                setTimeout( function() {
                                                                                                                                                                                                                                                                                                                                           // code that must be executed after pause
                                                                                                                                                                                                                                                                                                                                           window.location.href = "signin.html";
                                                                                                                                                                                                                                                                                                                                           }, 3000 );
                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                }).catch(function(error) {
                                                                                                                                                                                                                                                                                                                                         // An error happened.
                                                                                                                                                                                                                                                                                                                                         });
                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                 })
                                                                                                                                                                                                                                                                                           .catch(function(error) {
                                                                                                                                                                                                                                                                                                  console.error("Error writing document: ", error);
                                                                                                                                                                                                                                                                                                  });
                                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                           })
                                                                                                                                                                                                                                                                                     .catch(function(error) {
                                                                                                                                                                                                                                                                                            console.error("Error writing document: ", error);
                                                                                                                                                                                                                                                                                            });
                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                     })
                                                                                                                                                                                                                                                                               .catch(function(error) {
                                                                                                                                                                                                                                                                                      console.error("Error writing document: ", error);
                                                                                                                                                                                                                                                                                      });
                                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                               })
                                                                                                                                                                                                                                                                         .catch(function(error) {
                                                                                                                                                                                                                                                                                console.error("Error writing document: ", error);
                                                                                                                                                                                                                                                                                });
                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                         })
                                                                                                                                                                                                                                                                   .catch(function(error) {
                                                                                                                                                                                                                                                                          console.error("Error writing document: ", error);
                                                                                                                                                                                                                                                                          });
                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                   })
                                                                                                                                                                                                                                                             .catch(function(error) {
                                                                                                                                                                                                                                                                    console.error("Error writing document: ", error);
                                                                                                                                                                                                                                                                    });
                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                             })
                                                                                                                                                                                                                                                       .catch(function(error) {
                                                                                                                                                                                                                                                              console.error("Error writing document: ", error);
                                                                                                                                                                                                                                                              });
                                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                                       })
                                                                                                                                                                                                                                                 .catch(function(error) {
                                                                                                                                                                                                                                                        console.error("Error writing document: ", error);
                                                                                                                                                                                                                                                        });
                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                 })
                                                                                                                                                                                                                                           .catch(function(error) {
                                                                                                                                                                                                                                                  console.error("Error writing document: ", error);
                                                                                                                                                                                                                                                  });
                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                           })
                                                                                                                                                                                                                                     .catch(function(error) {
                                                                                                                                                                                                                                            console.error("Error writing document: ", error);
                                                                                                                                                                                                                                            });
                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                     })
                                                                                                                                                                                                                               .catch(function(error) {
                                                                                                                                                                                                                                      console.error("Error writing document: ", error);
                                                                                                                                                                                                                                      });
                                                                                                                                                                                                                               
                                                                                                                                                                                                                               })
                                                                                                                                                                                                                         .catch(function(error) {
                                                                                                                                                                                                                                console.error("Error writing document: ", error);
                                                                                                                                                                                                                                });
                                                                                                                                                                                                                         
                                                                                                                                                                                                                         })
                                                                                                                                                                                                                   .catch(function(error) {
                                                                                                                                                                                                                          console.error("Error writing document: ", error);
                                                                                                                                                                                                                          });
                                                                                                                                                                                                                   
                                                                                                                                                                                                                   })
                                                                                                                                                                                                             .catch(function(error) {
                                                                                                                                                                                                                    console.error("Error writing document: ", error);
                                                                                                                                                                                                                    });
                                                                                                                                                                                                             
                                                                                                                                                                                                             })
                                                                                                                                                                                                       .catch(function(error) {
                                                                                                                                                                                                              console.error("Error writing document: ", error);
                                                                                                                                                                                                              });
                                                                                                                                                                                                       
                                                                                                                                                                                                       })
                                                                                                                                                                                                 .catch(function(error) {
                                                                                                                                                                                                        console.error("Error writing document: ", error);
                                                                                                                                                                                                        });
                                                                                                                                                                                                 
                                                                                                                                                                                                 
                                                                                                                                                                                                 })
                                                                                                                                                                                           .catch(function(error) {
                                                                                                                                                                                                  console.error("Error writing document: ", error);
                                                                                                                                                                                                  });
                                                                                                                                                                                           
                                                                                                                                                                                           
                                                                                                                                                                                           })
                                                                                                                                                                                     .catch(function(error) {
                                                                                                                                                                                            console.error("Error writing document: ", error);
                                                                                                                                                                                            });
                                                                                                                                                                                     
                                                                                                                                                                                     
                                                                                                                                                                                     })
                                                                                                                                                                               .catch(function(error) {
                                                                                                                                                                                      console.error("Error writing document: ", error);
                                                                                                                                                                                      });
                                                                                                                                                                               
                                                                                                                                                                               
                                                                                                                                                                               })
                                                                                                                                                                         .catch(function(error) {
                                                                                                                                                                                console.error("Error writing document: ", error);
                                                                                                                                                                                });
                                                                                                                                                                         
                                                                                                                                                                         
                                                                                                                                                                         })
                                                                                                                                                                   .catch(function(error) {
                                                                                                                                                                          console.error("Error writing document: ", error);
                                                                                                                                                                          });
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   })
                                                                                                                                                             .catch(function(error) {
                                                                                                                                                                    console.error("Error writing document: ", error);
                                                                                                                                                                    });
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             })
                                                                                                                                                       .catch(function(error) {
                                                                                                                                                              console.error("Error writing document: ", error);
                                                                                                                                                              });
                                                                                                                                                       
                                                                                                                                                       
                                                                                                                                                       })
                                                                                                                                                 .catch(function(error) {
                                                                                                                                                        console.error("Error writing document: ", error);
                                                                                                                                                        });
                                                                                                                                                 
                                                                                                                                                 
                                                                                                                                                 })
                                                                                                                                           .catch(function(error) {
                                                                                                                                                  console.error("Error writing document: ", error);
                                                                                                                                                  });
                                                                                                                                           
                                                                                                                                           
                                                                                                                                           })
                                                                                                                                     .catch(function(error) {
                                                                                                                                            console.error("Error writing document: ", error);
                                                                                                                                            });
                                                                                                                                     
                                                                                                                                     
                                                                                                                                     
                                                                                                                                     })
                                                                                                                               .catch(function(error) {
                                                                                                                                      console.error("Error writing document: ", error);
                                                                                                                                      });
                                                                                                                               
                                                                                                                               
                                                                                                                               })
                                                                                                                         .catch(function(error) {
                                                                                                                                console.error("Error writing document: ", error);
                                                                                                                                });
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         }
                                                                                                                         }).catch(function(error) {
                                                                                                                                  console.log("Error getting document:", error);
                                                                                                                                  });
                                                                                                
                                                                                                }).catch(function(error) {
                                                                                                         // Handle Errors here.
                                                                                                         var errorCode = error.code;
                                                                                                         var errorMessage = error.message;
                                                                                                         // ...
                                                                                                         if (errorCode == 'auth/weak-password') {
                                                                                                         $('#r_err_message').text("The password is too weak.").show();
                                                                                                         }
                                                                                                         else if(errorCode == 'auth/email-already-in-use'){
                                                                                                         $('#r_err_message').text("Email already in use.").show();
                                                                                                         }
                                                                                                         else {
                                                                                                         $('#r_err_message').text(errorMessage).show();
                                                                                                         }
                                                                                                         
                                                                                                         });
                           
                           }
                           else{
                           $('#r_err_message').text("Invalid Trofi Code!").show();
                           }
                           
                           
                           } else {
                           // doc.data() will be undefined in this case
                           console.log("No such document:", error);
                           }
                           }).catch(function(error) {
                                    console.log("Error getting document:", error);
                                    });
    }
    
    
    
}

function loginUser(db){
    console.log("login in...");
    
    var email = $('#l_email').val();
    var password = $('#l_password').val();
    var rememberMe = $('#remember_me').is(":checked");
    console.log("remember");
    console.log(rememberMe);
    
    if (email === "" || password === "") {
        $('#l_err_message').text("All fields must be filled in!").show();
        $('#l_succ_message').hide();
        $('#l_loading').hide();
    }
    else{
        
        $('#l_err_message').hide();
        $('#l_loading').show();
        $('#l_succ_message').text("Attempting signing in...").show();
        firebase.auth().signInWithEmailAndPassword(email, password).then(function(){
                                                                         console.log("signed in");
                                                                         var user = firebase.auth().currentUser;
                                                                         const resRef = db.collection("restaurants").doc(user.uid);
                                                                         const resPrivateRef = resRef.collection('private').doc(user.uid);
                                                                         
                                                                         resPrivateRef.get().then(function(doc) {
                                                                                                  if (doc.exists) {
                                                                                                  //console.log("Document data:", doc.data());
                                                                                                  
                                                                                                  if(doc.data().allow_in == true){
                                                                                                  $('#l_err_message').hide();
                                                                                                  $('#l_loading').hide();
                                                                                                  $('#l_succ_message').text("Successfully signed in! Redirecting you to dashboard...").show();
                                                                                                  
                                                                                                  localStorage.setItem("remember_me_trofi",rememberMe);
                                                                                                  
                                                                                                  
                                                                                                  // Sign-out successful.''
                                                                                                  setTimeout( function() {
                                                                                                             // code that must be executed after pause
                                                                                                             window.location.href = "index.html";
                                                                                                             }, 1500 );
                                                                                                  }
                                                                                                  else{
                                                                                                  $('#l_succ_message').hide();
                                                                                                  $('#l_loading').hide();
                                                                                                  $('#l_err_message').text("Trofi has not verified your account yet. Please wait to receive an email.").show();
                                                                                                  
                                                                                                  // sign out without navigating pages
                                                                                                  firebase.auth().signOut().then(function() {
                                                                                                                                 // Sign-out successful.
                                                                                                                                 
                                                                                                                                 //  return false;
                                                                                                                                 
                                                                                                                                 }, function(error) {
                                                                                                                                 // An error happened.
                                                                                                                                 $('#l_succ_message').hide();
                                                                                                                                 $('#l_loading').hide();
                                                                                                                                 $('#l_err_message').text(error).show();
                                                                                                                                 });
                                                                                                  
                                                                                                  
                                                                                                  }
                                                                                                  
                                                                                                  } else {
                                                                                                  // doc.data() will be undefined in this case
                                                                                                  //   console.log("No such document!");
                                                                                                  }
                                                                                                  }).catch(function(error) {
                                                                                                           //  console.log("Error getting document:", error);
                                                                                                           $('#l_succ_message').hide();
                                                                                                           $('#l_loading').hide();
                                                                                                           $('#l_err_message').text(error).show();
                                                                                                           });
                                                                         
                                                                         
                                                                         
                                                                         }).catch(function(error) {
                                                                                  // Handle Errors here.
                                                                                  var errorCode = error.code;
                                                                                  var errorMessage = error.message;
                                                                                  $('#l_succ_message').hide();
                                                                                  $('#l_loading').hide();
                                                                                  $('#l_err_message').text(errorMessage).show();
                                                                                  // ...
                                                                                  });
        
        
        
    }
}

function pad(n, width, z) {
    z = z || '0';
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function tConvert (time) {
    // Check correct time format and split into components
    time = time.toString ().match (/^([01]\d|2[0-3])(:)([0-5]\d)(:[0-5]\d)?$/) || [time];
    
    if (time.length > 1) { // If time format correct
        time = time.slice (1);  // Remove full string match value
        time[5] = +time[0] < 12 ? 'AM' : 'PM'; // Set AM/PM
        time[0] = +time[0] % 12 || 12; // Adjust hours
    }
    return time.join (''); // return adjusted time or original string
}
