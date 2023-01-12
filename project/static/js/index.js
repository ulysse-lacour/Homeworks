$(document).ready(function () {
  // SELECT FILTER
  let url = new URL(window.location);
  let url_color = url.pathname.split("/")[2];
  let color = "#" + url_color;
  $("#selectField").css("color", color);
  $("#selectField option[value='" + url_color + "']").attr(
    "selected",
    "selected"
  );
  $("#selectField").change(function () {
    if ($("#selectField").val() != "") {
      let color = $("#selectField").val();
      $("#selectField").css("color", "#" + color);
      window.location.href =
        "https://homeworks.ulysselacour.com/color/" + color;
    }
  });

  // SELECT FOR UPLOAD
  $("#select_color_upload").change(function () {
    if ($("#select_color_upload").val() != "") {
      let color = $("#select_color_upload").val();
      $("#select_color_upload").css("color", "#" + color);
    }
  });

  // STICKY TITLE
  var not_scroll_top_position = $("#not_scroll_title").offset().top;
  var not_scroll_height = $("#homeworks_title").height();
  var position_for_scroll = not_scroll_top_position + not_scroll_height / 2;
  $("#scroll_title").css({ position: "fixed", top: position_for_scroll });

  // DESCRIPTION ON HOVER :
  $(".images, .description").hover(
    function () {
      let parent = $(this).parent();
      let div = parent.children(".description");
      div.children(".description_text").attr("style", "opacity: 100;");
    },
    function () {
      let parent = $(this).parent();
      let div = parent.children(".description");
      div.children(".description_text").attr("style", "opacity: 0;");
    }
  );

  // DRAG N DROP HANDLING
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
});
