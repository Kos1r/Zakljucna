// loged.js - Celotna logika za graf

document.addEventListener('DOMContentLoaded', function() {
    const chartElement = document.getElementById('visitsChart');
    
    if (chartElement) {
        // Preberemo podatke iz data- atributov, ki jih je pripravil Flask/Jinja
        const labels = JSON.parse(chartElement.getAttribute('data-labels'));
        const values = JSON.parse(chartElement.getAttribute('data-values'));

        const ctx = chartElement.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Obiski',
                    data: values,
                    backgroundColor: '#d9534f',
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { 
                        beginAtZero: true, 
                        grid: { color: '#333' }, 
                        ticks: { color: '#888' } 
                    },
                    x: { 
                        grid: { display: false }, 
                        ticks: { color: '#888' } 
                    }
                },
                plugins: { 
                    legend: { display: false } 
                }
            }
        });
    }
});