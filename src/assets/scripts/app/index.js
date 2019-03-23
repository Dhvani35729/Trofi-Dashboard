import * as $ from 'jquery';

export default (function () {

  console.log("app scripts :)");


  $('#register_user').on('click', e => {
    registerUser();
    e.preventDefault();
  });

  $('#login_user').on('click', e => {
    loginUser();
    e.preventDefault();
  });

}());

function registerUser(){
  console.log("registering...");

}

function loginUser(){
  console.log("login in...");

}
