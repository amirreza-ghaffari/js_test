
//bar chart
const ctx1 = document.getElementById('barchart').getContext('2d');
const myChart1 = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: ['Developed', 'Planned', 'Undevepoled', 'Total'],
        datasets: [{
            // label: '# of Votes',
            data: [5, 3, 2, 10],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                // 'rgba(153, 102, 255, 0.2)',
                // 'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                // 'rgba(153, 102, 255, 1)',
                // 'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    // plugins:[ChartDataLabels],
    options: {
        plugins: {
            labels: {
                render: 'value',
            },
            legend: {
                display: false,
                labels: {
                    color: 'rgb(255, 99, 132)'
                }
            },
            title: {
                display: true,
                text: 'Number Of Contingencies',
                padding: {
                    top: 10,
                    bottom: 10
                }
            }
        },
        responsive:true,
        maintainAspectRatio:true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});



//trend chart
const ctx2 = document.getElementById('trend').getContext('2d');
const myChart2 = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        datasets: [{
            // label: '# of Votes',
            data: [12, 9, 33, 5, 2, 13],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false,
                labels: {
                    color: 'rgb(255, 99, 132)'
                }
            },
            title: {
                display: true,
                text: 'Number Of Incidents',
                padding: {
                    top: 10,
                    bottom: 10
                }
            }
        },
        responsive:true,
        maintainAspectRatio:true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

//barchart2
const ctx3 = document.getElementById('barchart2').getContext('2d');
const myChart3 = new Chart(ctx3, {
    type: 'bar',
    data: {
        labels: ['Danesh', 'Gandi', 'Plaza', 'Shad Abad','Badamak'],
        datasets: [{
            // label: '# of Votes',
            data: [5, 3, 2, 1,2],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                // 'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                // 'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    // plugins:[ChartDataLabels],
    options: {
        plugins: {
            labels: {
                render: 'value',
            },
            legend: {
                display: false,
                labels: {
                    color: 'rgb(255, 99, 132)'
                }
            },
            title: {
                display: true,
                text: 'Number Of Incidents Per Location',
                padding: {
                    top: 10,
                    bottom: 10
                }
            }
        },
        responsive:true,
        maintainAspectRatio:true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

//barchart3
const ctx4 = document.getElementById('barchart3').getContext('2d');
const myChart4 = new Chart(ctx4, {
    type: 'bar',
    data: {
        labels: ['Close', 'Open', 'Ongoing'],
        datasets: [{
            // label: '# of Votes',
            data: [5, 3, 2, 1,2],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                // 'rgba(75, 192, 192, 0.2)',
                // 'rgba(153, 102, 255, 0.2)',
                // 'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                // 'rgba(75, 192, 192, 1)',
                // 'rgba(153, 102, 255, 1)',
                // 'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    // plugins:[ChartDataLabels],
    options: {
        plugins: {
            labels: {
                render: 'value',
            },
            legend: {
                display: false,
                labels: {
                    color: 'rgb(255, 99, 132)'
                }
            },
            title: {
                display: true,
                text: 'Incident Status',
                padding: {
                    top: 10,
                    bottom: 10
                }
            }
        },
        responsive:true,
        maintainAspectRatio:true,
        scales: {
            y: {
                beginAtZero: true
                // max:20
            }
        }
    }
});

