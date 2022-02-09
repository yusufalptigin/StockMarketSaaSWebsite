(function (self) {
    var selectors = {
        NAME: 'a:not(.code) .tm-post-title',
        PRICE: 'p.tm-pt-30',
        CHANGE: '.change',
        CODE: '.code .tm-post-title',
        PROFIT: '.Profit',
        QUANTITY: '.Quantity'
    };
    var settings = {
        homepage: {
            url: 'https://stockwizard.herokuapp.com/api/v1.0/viewer/stocks/info',
            method: 'GET',
            headers: {
                Authorization: 'Basic dGVzdDp0ZXN0'
            },
        },
        performancepage: {
            url: 'https://stockwizard.herokuapp.com/api/v1.0/manager/',
            method: 'GET'
        }
    };
    var endpoints = ['Nasdaq', 'XU30', 'Cryptos', 'Pairs'];
    var selectorsTable = {
        XU30: 'XU',
        Nasdaq: 'NASDAQ',
        Cryptos: 'CRYPTOS',
        Pairs: 'PAIRS',

    };

    self.init = function () {
        if (location.pathname.indexOf('info') > -1) {
            self.addBuySellEvent('buy');
            self.createTable(settings.homepage);
        } else if (location.pathname.indexOf('adviceToUser') > -1) {
            self.createAdviceTable();
        } else if (location.pathname.indexOf('advice') > -1) {
            self.createAdvicepageTable();
        } else if (location.pathname.indexOf('post') > -1) {
            self.addBuySellEvent('sell');
            self.createTable(settings.performancepage);
        }
    };

    self.createAdviceTable = function () {
        $.ajax({
            url: 'https://stockwizard.herokuapp.com/api/v1.0/manager/advice',
            method: 'GET'
        }).done(function (response) {
            Object.entries(response).forEach(function (column, index) {
                if (column[0] !== 'cat') {
                    var headerNames = {
                        daily_best: 'Daily Best',
                        month_worst: 'Monthly - Worst Performance',
                        month_best: 'Monthly - Best Performance',
                        month_avg: 'Monthly - Average Performance'
                    };

                    $('.user-table-header .column:eq(' + (index - 1) + ')').text(headerNames[column[0]]);

                    (column[1] || []).forEach(function (dataArray) {
                        dataArray.forEach(function (data) {
                            if (typeof data !== 'number') {
                                var cloneColumnItem = $('.column-item:eq(0)').clone();

                                cloneColumnItem.text(data);

                                $('.user-table-body .column:eq(' + (index - 1) + ')').append(cloneColumnItem);
                            }
                        });
                    });
                } else {
                    $('.user-table-main-header').text("Most suitable stock category for you is: " + column[1]);
                }
            });
        });
    };

    self.addBuySellEvent = function (action) {
        $('div.row.tm-row').off('click', '.' + action).on('click', '.' + action, function () {
            var code = $(this).parents('.col-12.col-md-6.tm-post').find('.code').text().trim();

            if (code) {
                $.ajax({
                    url: 'https://stockwizard.herokuapp.com/api/v1.0/manager/' + action + '/' + code + ':1',
                    method: 'POST'
                }).done(function () {
                    alert('You performed ' + code + ': ' + action + ' successfully!');

                    setTimeout(function () {
                        if (action === 'sell') {
                            self.createTable(settings.performancepage);
                        }
                    }, 500);
                });
            } else {
                alert('code not found');
            }
        });
    };

    self.createTable = function (config) {
        $('.col-12.col-md-6.tm-post:not(:first)').remove();

        $.ajax(config).done(function (response) {
            console.log(response);

            Object.keys(response.response).forEach(function (type) {
                if (((response || {}).response || {})[type] === null) {
                    $('.col-12.col-md-6.tm-post:first').text('You don\'t have any stocks!');
                } else {
                    (((response || {}).response || {})[type] || []).forEach(function (value, index) {
                        var articleLenght = $('.col-12.col-md-6.tm-post').length;
                        var className = '';

                        value = typeof value === 'string' ? value.trim() : value;

                        if (type === 'PRICE' || type === 'CHANGE' || type === 'PROFIT' || type === 'QUANTITY') {
                            if (Number(value) < 0 && (type === 'CHANGE' || type === 'PROFIT')) {
                                className = 'red';
                            } else if (Number(value) > 0 && (type === 'CHANGE' || type === 'PROFIT')) {
                                className = 'green';
                            } else {
                                className = '';
                            }

                            value = (type + ': ' + Number(value).toFixed(4));
                        } else {
                            className = '';
                        }

                        if (articleLenght > index) {
                            $('.col-12.col-md-6.tm-post:eq(' + index + ')').show()
                                .find(selectors[type]).text(value).removeClass('red green').addClass(className);
                        } else {
                            var cloneElement = $('.col-12.col-md-6.tm-post:eq(0)').clone();

                            cloneElement.find(selectors[type]).text(value).removeClass('red green').addClass(className);

                            cloneElement.show().insertAfter('.col-12.col-md-6.tm-post:last');
                        }
                    });
                }
            });
        });
    };

    self.createAdvicepageTable = function () {
        endpoints.forEach(function (endpoint) {
            var tableSettings = {
                url: 'https://stockwizard.herokuapp.com/api/v1.0/viewer/mavResult/' + endpoint,
                method: 'GET',
            };

            $.ajax(tableSettings).done(function (response) {
                console.log(response);

                response.stockList.forEach(function (stockArray, stockIndex) {
                    stockArray.forEach(function (stock, index) {
                        var colorclass = '';

                        if (stock === 'Buy') {
                            colorclass = 'green';
                        } else if (stock === 'Sell') {
                            colorclass = 'red';
                        } else {
                            colorclass = '';
                        }

                        if ($('table.' + selectorsTable[endpoint] + ' tbody tr:eq(' + stockIndex + ')').length) {
                            $('table.' + selectorsTable[endpoint] + ' tbody tr:eq(' + stockIndex + ') td:eq(' + index + ')')
                                .text(stock).removeClass('red green').addClass(colorclass);
                        } else {
                            var clonedRow = $('table.' + selectorsTable[endpoint] + ' tbody tr:eq(0)').clone();

                            clonedRow.find('td:eq(' + index + ')').text(stock).removeClass('red green').addClass(colorclass);

                            clonedRow.show().insertAfter('table.' + selectorsTable[endpoint] + ' tbody tr:last');
                        }
                    });
                });
            });
        });
    };

    self.init();
})({});

$(function () {
    $(".navbar-toggler").on("click", function (e) {
        $(".tm-header").toggleClass("show");
        e.stopPropagation();
    });

    $("html").click(function (e) {
        var header = document.getElementById("tm-header");

        if (!header.contains(e.target)) {
            $(".tm-header").removeClass("show");
        }
    });

    $("#tm-nav .nav-link").click(function (e) {
        $(".tm-header").removeClass("show");
    });
});