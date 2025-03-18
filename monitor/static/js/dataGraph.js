import { startProgressLoader, stopProgressLoader } from './startProgressLoader.js';

// Функция для обновления графика
const graphContainer = document.querySelector('.graph-container');
const horuBtn = document.querySelector('.hour-btn');
const dayBtn = document.querySelector('.day-btn');
const weekBtn = document.querySelector('.week-btn');
const graph = document.querySelector('.graph');
const updateGraphBtn = document.querySelector('.update-graph-btn');
const infoGraphUpdate = document.querySelector('.info-graph-update');
const infoGraph = document.querySelector('.info-graph');
const buttons = document.querySelector('.buttons');
const progressGraphLoader = document.querySelector('.progress-graph-loader');

document.addEventListener('DOMContentLoaded', function () {
    horuBtn.addEventListener('click', () => updateGraphData('hour'));
    dayBtn.addEventListener('click', () => updateGraphData('day'));
    weekBtn.addEventListener('click', () => updateGraphData('week'));
    updateGraphBtn.addEventListener('click', () => updateGraphData('hour'));
});

export async function updateGraphData(interval = 'hour') {
    stopProgressLoader(progressGraphLoader);

    const showText = interval === 'hour';
    horuBtn.classList.toggle('active', interval === 'hour');
    dayBtn.classList.toggle('active', interval === 'day');
    weekBtn.classList.toggle('active', interval === 'week');

    if (interval !== 'hour') {
        infoGraphUpdate.style.display = 'none';
        stopProgressLoader(progressGraphLoader);
    }

    graphContainer.style.display = 'block';
    graph.innerHTML = `<div class="loader"></div>`;
    infoGraph.style.display = 'block';

    const url = `/api/${interval}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        graph.innerHTML = ``;
        buttons.style.display = 'flex';
        buttons.style.gap = '7px';
        buttons.style.position = 'absolute';
        buttons.style.background = 'none';

        if (interval === 'hour') {
            infoGraphUpdate.style.display = 'flex';
            startProgressLoader(updateGraphData, progressGraphLoader, 60000);
        }

        if (data.no_data) {
            buttons.style.position = 'static';
            buttons.style.background = 'rgba(255, 255, 255, 0.5)';
            graph.innerHTML = `<div class="error">${data.no_data}</div>`;
            return;
        }

        // Очищаем старый график
        Plotly.purge(graph);

        // Обновляем график
        const dates = data.map((item) => {
            const date = new Date(item.created_at.replace(' ', 'T') + 'Z'); // Преобразуем в объект Date
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяц (0-11, поэтому +1)
            const day = String(date.getDate()).padStart(2, '0');
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            const seconds = String(date.getSeconds()).padStart(2, '0');

            return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        });

        const temperatures = data.map((item) => item.temperature);
        const humidities = data.map((item) => item.humidity);

        Plotly.react(
            graph,
            [
                {
                    x: dates,
                    y: humidities,
                    name: 'Humidity (%)',
                    line: { color: '#319fea' },
                    mode: showText ? 'lines+markers+text' : 'lines+text',
                    text: showText ? humidities.map((h) => `${h}%`) : [],
                    hoverinfo: 'none', // Показать дату, значение и подпись при наведении
                    textposition: 'top', // Позиция текста
                },
                {
                    x: dates,
                    y: temperatures,
                    name: 'Temperature (°C)',
                    line: { color: '#f65f80' },
                    mode: showText ? 'lines+markers+text' : 'lines+text',
                    text: showText ? temperatures.map((t) => `${t}°C`) : [],
                    hoverinfo: 'none',
                    textposition: 'top',
                },
            ],
            {
                title: {
                    text: 'Server room',
                    font: { size: 20, color: '#333', weight: 'bold' },
                },
                xaxis: {
                    title: {
                        text: 'Date and time',
                        font: { size: 14, color: '#333', weight: 'bold' },
                    },
                    fixedrange: true,
                },
                yaxis: {
                    title: { text: 'Meaning', font: { size: 14, color: '#333', weight: 'bold' } },
                    fixedrange: true,
                    range: [10, 70],
                    tickvals: [20, 30, 40, 50, 60],
                    dtick: 10,
                },
                legend: {
                    x: 1,
                    y: 2,
                    xanchor: 'right',
                    yanchor: 'top',
                    clickable: false,
                    font: { family: 'Arial, sans-serif', size: 12, color: '#333' },
                    bgcolor: 'rgba(247, 247, 247, 0.5)',
                },
                dragmode: false,
                plot_bgcolor: 'rgba(247, 247, 247, 0.5)',
                paper_bgcolor: 'rgba(255, 255, 255, 0)',
                margin: {
                    t: 0,
                    l: 50,
                    r: 50,
                    b: 50,
                },
            },
            {
                displayModeBar: false, // Отключаем панель инструментов
                legendItemClick: false, // Отключает клики по легенде
                legendItemDoubleClick: false, // Отключает двойной клик по легенде
            }
        );
    } catch (error) {
        console.error('Error when receiving data:', error);
        graphContainer.innerHTML = 'Error when receiving data.';
    }
}
