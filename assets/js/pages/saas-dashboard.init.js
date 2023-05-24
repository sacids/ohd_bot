/******/ (function () { // webpackBootstrap
  var __webpack_exports__ = {};
  /*!***************************************************!*\
    !*** ./resources/js/pages/saas-dashboard.init.js ***!
    \***************************************************/
  var options = {
    series: [{
      name: "Approved",
      data: [31, 40, 36, 51, 49, 72, 69, 56, 68, 82, 68, 76]
    },
    {
      name: "Pending",
      data: [12, 20, 16, 41, 29, 62, 49, 66, 48, 72, 48, 76]
    }
    ],
    chart: {
      height: 320,
      type: "line",
      toolbar: "false",
      dropShadow: {
        enabled: !0,
        color: "#000",
        top: 18,
        left: 7,
        blur: 8,
        opacity: .2
      }
    },
    dataLabels: {
      enabled: !1
    },
    colors: ["#2E7D32", "#B71C1C"],
    stroke: {
      curve: "smooth",
      width: 3
    }
  },
    chart = new ApexCharts(document.querySelector("#line-chart"), options);
  chart.render();


  //donut chart
  options = {
    series: [60, 40],
    chart: {
      type: "donut",
      height: 260,
    },
    labels: ["Approved", "Pending"],
    colors: ["#388E3C", "#C62828"],
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
  (chart = new ApexCharts(document.querySelector("#donut-chart"), options)).render();

  var options = {
    series: [{
      name: "Approved",
      data: [44, 55, 41, 64]
    }, {
      name: "Pending",
      data: [53, 32, 33, 52]
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
      categories: ['NMB Bank', 'Vodacom', 'Tigo Pesa', 'Airtel'],
    },
    labels: ["Approved", "Pending"],
    colors: ["#388E3C", "#C62828"],
  };

  var chart = new ApexCharts(document.querySelector("#bar-chart"), options);
  chart.render();

  //radio
  var radialoptions1 = {
    series: [37],
    chart: {
      type: "radialBar",
      width: 60,
      height: 60,
      sparkline: {
        enabled: !0
      }
    },
    dataLabels: {
      enabled: !1
    },
    colors: ["#556ee6"],
    plotOptions: {
      radialBar: {
        hollow: {
          margin: 0,
          size: "60%"
        },
        track: {
          margin: 0
        },
        dataLabels: {
          show: !1
        }
      }
    }
  },
    radialchart1 = new ApexCharts(document.querySelector("#radialchart-1"), radialoptions1);
  radialchart1.render();
  var radialoptions2 = {
    series: [72],
    chart: {
      type: "radialBar",
      width: 60,
      height: 60,
      sparkline: {
        enabled: !0
      }
    },
    dataLabels: {
      enabled: !1
    },
    colors: ["#34c38f"],
    plotOptions: {
      radialBar: {
        hollow: {
          margin: 0,
          size: "60%"
        },
        track: {
          margin: 0
        },
        dataLabels: {
          show: !1
        }
      }
    }
  },
    radialchart2 = new ApexCharts(document.querySelector("#radialchart-2"), radialoptions2);
  radialchart2.render();
  var radialoptions3 = {
    series: [54],
    chart: {
      type: "radialBar",
      width: 60,
      height: 60,
      sparkline: {
        enabled: !0
      }
    },
    dataLabels: {
      enabled: !1
    },
    colors: ["#f46a6a"],
    plotOptions: {
      radialBar: {
        hollow: {
          margin: 0,
          size: "60%"
        },
        track: {
          margin: 0
        },
        dataLabels: {
          show: !1
        }
      }
    }
  },
    radialchart3 = new ApexCharts(document.querySelector("#radialchart-3"), radialoptions3);
  radialchart3.render();
  /******/
})()
  ;