import * as $ from 'jquery';
import * as firebase from 'firebase';
import 'firebase/firestore';

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
  console.log(rememberMe)
  if(rememberMe != 'true'){
    console.log('here');
    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION)
  }
  else{
   firebase.auth().setPersistence(firebase.auth.Auth.Persistence.LOCAL)
  }

  if(document.URL.indexOf("signin.html") != -1 || document.URL.indexOf("signup.html") != -1){
  window.location.href = "index.html";
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
  }
  else{


      firebase.auth().signInWithEmailAndPassword(email, password).then(function(){
        console.log("signed in");
        var user = firebase.auth().currentUser;
        const resRef = db.collection("restaurants").doc(user.uid);
        const resPrivateRef = resRef.collection('private').doc(user.uid);

        resPrivateRef.get().then(function(doc) {
            if (doc.exists) {
                //console.log("Document data:", doc.data());

                if(doc.data().allow_in == true){
                  $('l_err_message').hide();
                  $('#l_loading').hide();
                  $('#l_succ_message').text("Successfully signed in! Redirecting you to dashboard...").show();

                  localStorage.setItem("remember_me_trofi",rememberMe);


                                   // Sign-out successful.''
                 setTimeout( function() {
                                     // code that must be executed after pause
                       window.location.href = "index.html";
                 }, 3000 );
                }
                else{
                  $('#l_err_message').text("Trofi has not verified your account yet. Please wait to receive an email.").show();

                  // sign out without navigating pages
                  firebase.auth().signOut().then(function() {
                  // Sign-out successful.

                    //  return false;

                }, function(error) {
                  // An error happened.
                    $('#l_err_message').text(error).show();
                });


                }

            } else {
                // doc.data() will be undefined in this case
              //   console.log("No such document!");
            }
        }).catch(function(error) {
          //  console.log("Error getting document:", error);
              $('#l_err_message').text(error).show();
        });



      }).catch(function(error) {
          // Handle Errors here.
          var errorCode = error.code;
          var errorMessage = error.message;
            $('#l_err_message').text(errorMessage).show();
          // ...
        });



    }





}
