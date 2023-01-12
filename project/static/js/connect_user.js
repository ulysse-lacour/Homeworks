$(document).ready(function () {
  var login_FormData = new FormData();
  var typing = false;
  $(function () {
    $(window).keypress(function (e) {
      var ev = e || window.event;
      var key = ev.keyCode || ev.which;
      if (typing == false) {
        if (key == 13) {
          typing = true;
          $(".main_page").attr("style", "visibility: hidden");
          $(".login_page").attr("style", "visibility: visible");
          $(".select_color_input").attr("style", "visibility: hidden");
          $("#password").focus();
        }
      } else {
        if (key == 13) {
          var password = $("#password").val();
          login_FormData.append("password", password);
          login_FormData.append("name", "GODESS");
          var req = {
            url: "https://homeworks.ulysselacour.com/login",
            method: "post",
            processData: false,
            contentType: false,
            data: login_FormData,
            success: function (data) {
              location.reload();
            },
            error: function (xhr, ajaxOptions, thrownError) {
              alert(xhr.responseText);
              location.reload();
            },
          };
          var promise = $.ajax(req);
        }
      }
    });
  });
});
