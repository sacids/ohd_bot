//pending and approved mandate value
$.getJSON('api/dashboard/mandate-values', (data) => {
    if (data.error == false) {
        var arr_month = [];
        var arr_total = [];
        var arr_approved = [];
        var arr_pending = [];

        for (k = 0; k < data.chart.length; k++) {
            arr_month.push(data.chart[k].month);
            arr_total.push(data.chart[k].total);
            arr_pending.push(data.chart[k].pending);
            arr_approved.push(data.chart[k].approved);
        }

        var options = {
            series: [
                {
                    name: "All",
                    data: arr_total
                },
                {
                    name: "Approved",
                    data: arr_approved
                },
                {
                    name: "Pending",
                    data: arr_pending
                },
            ],
            // chart: {
            //     height: 320,
            //     type: "line",
            //     toolbar: "false",
            //     dropShadow: {
            //         enabled: !0,
            //         color: "#000",
            //         top: 18,
            //         left: 7,
            //         blur: 8,
            //         opacity: .8
            //     }
            // },
            chart: {
                type: 'bar',
                height: 350,
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: false,
                    columnWidth: '75%',
                    endingShape: 'rounded',
                    dataLabels: {
                        position: 'bottom'
                    },
                }
            },
            dataLabels: {
                enabled: !1
            },
            stroke: {
                show: true,
                width: 2,
                colors: ['transparent']
            },
            fill: {
                opacity: 1
            },
            yaxis: {
                labels: {
                    formatter: function (value) {
                        return value.toLocaleString();
                    }
                },
            },
            xaxis: {
                labels: {
                    show: true,
                    rotate: -45,
                    rotateAlways: false,
                },
                crosshair: true,
                categories: arr_month,
            },
            colors: ["#1565C0", "#66BB6A", "#F44336"],
            // stroke: {
            //     curve: "smooth",
            //     width: 3
            // }
        };

        //render chart  
        var chart = new ApexCharts(document.querySelector("#consent-value-chart"), options);
        chart.render();
    }
});


//pending and approved mandate percentage
$.getJSON('api/dashboard/mandate-percentages', (data) => {
    if (data.error == false) {
        //charts
        var options = {
            series: [data.pending, data.approved],
            chart: {
                type: "donut",
                height: 340,
            },
            labels: ["Pending", "Approved"],
            colors: ["#F44336", "#66BB6A"],
            legend: {
                show: !1
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: "70%"
                    }
                }
            }
        };

        //render chart
        var chart = new ApexCharts(document.querySelector("#consent-rate-chart"), options);
        chart.render()
    }
});

//pending and approved by payment channel
$.getJSON('api/dashboard/consent-per-channel', (data) => {
    if (data.error == false) {

        var arr_channels = [];
        var arr_approved = [];
        var arr_pending = [];

        for (k = 0; k < data.chart.length; k++) {
            arr_channels.push(data.chart[k].name);
            arr_pending.push(data.chart[k].pending);
            arr_approved.push(data.chart[k].approved);
        }

        //charts
        var options = {
            series: [{
                name: "Approved",
                data: arr_approved
            }, {
                name: "Pending",
                data: arr_pending
            }],
            chart: {
                type: 'bar',
                height: 320,
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: true,
                    dataLabels: {
                        position: 'bottom'
                    },
                }
            },
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: arr_channels,
            },
            labels: ["Approved", "Pending"],
            colors: ["#66BB6A", "#F44336"],
        };

        //render chart  
        var chart = new ApexCharts(document.querySelector("#consent-channel-chart"), options);
        chart.render();
    }
});

//on CLICK 
$('#select-month').on('change', function (e) {
    e.preventDefault;

    //variables
    var monthName = $(this).val();

    $.getJSON('api/dashboard/consent-per-channel', { month: monthName }, (data) => {
        if (data.error == false) {

            var arr_channels = [];
            var arr_approved = [];
            var arr_pending = [];

            for (k = 0; k < data.chart.length; k++) {
                arr_channels.push(data.chart[k].name);
                arr_pending.push(data.chart[k].pending);
                arr_approved.push(data.chart[k].approved);
            }

            //charts
            var options = {
                series: [
                    {
                        name: "Approved",
                        data: arr_approved
                    },
                    {
                        name: "Pending",
                        data: arr_pending
                    }],
                chart: {
                    type: 'bar',
                    height: 320,
                },
                plotOptions: {
                    bar: {
                        borderRadius: 4,
                        horizontal: true,
                        dataLabels: {
                            position: 'bottom'
                        },
                    }
                },
                dataLabels: {
                    enabled: false
                },
                xaxis: {
                    categories: arr_channels,
                },
                labels: ["Approved", "Pending"],
                colors: ["#66BB6A", "#F44336"],
            };

            //render chart
            var chart = new ApexCharts(document.querySelector("#consent-channel-chart"), options);
            chart.render();
        }
    });

});
