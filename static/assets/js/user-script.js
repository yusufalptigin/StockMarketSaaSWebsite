$(function() {
    $(".navbar-toggler").on("click", function(e) {
        $(".tm-header").toggleClass("show");
        e.stopPropagation();
      });
    
      $("html").click(function(e) {
        var header = document.getElementById("tm-header");
    
        if (!header.contains(e.target)) {
          $(".tm-header").removeClass("show");
        }
      });
    
      $("#tm-nav .nav-link").click(function(e) {
        $(".tm-header").removeClass("show");
      });
});

var settings = {url: "https://stockwizard.herokuapp.com/api/v1.0/manager/", method: 'GET'};

var selectors = {
  NAME: 'a:not(.code) .tm-post-title',
  PRICE: 'p.tm-pt-30',
  CHANGE: '.change',
  CODE: '.code .tm-post-title'
};

$.ajax(settings).done(function (response) {
  console.log(response);

  Object.keys(response.response).forEach(function (type) {
      response.response[type].forEach(function (value, index) {
          var articleLenght = $('.col-12.col-md-6.tm-post').length;
          var className = '';

          if (type === 'PRICE' || type === 'CHANGE') {
              if (Number(value) < 0 && type === 'CHANGE') {
                  className = 'red';
              } else if (type === 'CHANGE') {
                  className = 'green';
              } else {
                  className = '';
              }

              value = (type + ': ' + value);
          } else {
              className = '';
          }

          if (articleLenght > index) {
              $('.col-12.col-md-6.tm-post:eq(' + index + ')').show()
                  .find(selectors[type]).text(value).addClass(className);
          } else {
              var cloneElement = $('.col-12.col-md-6.tm-post:eq(0)').clone();

              cloneElement.find(selectors[type]).text(value).addClass(className);

              cloneElement.show().insertAfter('.col-12.col-md-6.tm-post:eq(0)');
              stockCode = cloneElement.find('h2')[0].firstChild.nodeValue.trim()
              cloneElement.find('buy').on('click', 
              () => {$.ajax({url: "https://stockwizard.herokuapp.com/api/v1.0/manager/buy/" + stockCode + ":1", method: 'POST'}).done(
                  (response) => {if (response['response'] == true) {alert("Transaction successful.")} else {alert("Transaction failed.")} }) ;})
          }
      });
  });
});
