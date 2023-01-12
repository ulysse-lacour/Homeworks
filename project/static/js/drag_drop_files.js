$(document).ready(function () {
  var formData = new FormData();
  var files = [];

  window.addEventListener(
    "dragover",
    function (e) {
      e = e || event;
      if (!e.target.classList.contains(".images_div")) {
        e.preventDefault();
      }
    },
    false
  );
  window.addEventListener(
    "drop",
    function (e) {
      e = e || event;
      e.preventDefault();
    },
    false
  );

  var dragHandler = function (evt) {
    evt.preventDefault();
  };

  var dragLeaver = function (evt) {
    evt.preventDefault();
  };

  var dropHandler = function (evt) {
    evt.preventDefault();
    $(".index_text").attr("style", "visibility: hidden");
    $(".index_block").removeClass("crossed");
    $("#scroll_title").addClass("uploading");
    $("#scroll_title").attr("style", "visibility: hidden");
    $("#not_scroll_title").attr("style", "visibility: hidden");
    $(".images_details_form").attr("style", "visibility: visible");

    files = evt.originalEvent.dataTransfer.files;
    formData.append("files[]", files[0]);
  };

  var dropHandlerSet = {
    dragleave: dragLeaver,
    drop: dropHandler,
  };

  $(".drop-box").on(dropHandlerSet);
  $(".submit_button").click(function () {
    var empty_field = false;
    $("form :input").each(function () {
      var input = $(this);
      if (input.val() == "") {
        empty_field = true;
      } else if (input.val() == null) {
        empty_field = true;
      }
    });
    if (!empty_field) {
      $("#uploading").attr("style", "visibility: visible");
      $(".field").attr("style", "visibility: hidden");
      var artist_name = document.getElementById("artist_name").value;
      var color = document.getElementById("select_color_upload").value;
      var email = document.getElementById("artist_email").value;
      var insta = document.getElementById("insta").value;
      if (insta.substring(0, 1) != "@") {
        insta = "@" + insta;
      }
      formData.append("artist_name", artist_name);
      formData.append("artist_email", email);
      formData.append("insta", insta);
      formData.append("color", color);
      formData.append("files[]", files[0]);
      var req = {
        url: "https://homeworks.ulysselacour.com/upload",
        method: "post",
        processData: false,
        contentType: false,
        data: formData,
        success: function (data) {
          window.location.href =
            "https://homeworks.ulysselacour.com/color/" + color;
        },
        error: function (xhr, ajaxOptions, thrownError) {
          alert(xhr.responseText);
          location.reload();
        },
      };
      var promise = $.ajax(req);
    }
  });
});
