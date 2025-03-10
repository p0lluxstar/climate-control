// Функция для обновления данных и графика

const horuBtn = document.querySelector('.hour-btn');
const dayBtn = document.querySelector('.day-btn');
const weekBtn = document.querySelector('.week-btn');

document.addEventListener('DOMContentLoaded', function () {
    horuBtn.addEventListener('click', () => updateGraphContainer('hour'));
    dayBtn.addEventListener('click', () => updateGraphContainer('day'));
    weekBtn.addEventListener('click', () => updateGraphContainer('week'));
});

function updateDataContainer() {
    const dataContainer = document.querySelector('.data-container');

    fetch(`api/latest`)
        .then((response) => response.json())
        .then((data) => {
            if (!data || data.length === 0) {
                dataContainer.innerHTML = `<div class="error">Нет данных за выбранный период.</div>`;
                return;
            }

            // Обновляем данные на странице
            dataContainer.innerHTML = `
                <div class="data-last">
                    <span class="title">Последний замер датчика</span>
                    <div class="date">Дата и время: ${data[data.length - 1].created_at}</div>
                    <div class="temperature">Температура: ${data[data.length - 1].temperature}°C</div>
                    <div class="humidity">Влажность: ${data[data.length - 1].humidity}%</div>
                </div>
            `;
        });
}

setTimeout(updateDataContainer, 1000);
// setInterval(updateDataContainer, 10000);

function updateGraphContainer(interval = 'hour') {
    const graphContainer = document.querySelector('.graph-container');
    const graph = document.querySelector('.graph');
    const buttons = document.querySelector('.buttons');
    const showText = interval === 'hour';

    if (interval === 'hour') {
        horuBtn.classList.add('active');
    } else horuBtn.classList.remove('active');

    if (interval === 'day') {
        dayBtn.classList.add('active');
    } else dayBtn.classList.remove('active');

    if (interval === 'week') {
        weekBtn.classList.add('active');
    } else weekBtn.classList.remove('active');

    // Формируем URL в зависимости от интервала
    const url = `/api/${interval}`;

    fetch(url) // Отправляем запрос на сервер
        .then((response) => response.json()) // Преобразуем ответ в JSON
        .then((data) => {
            graph.innerHTML = ``;
            buttons.style.display = 'block';
            buttons.style.position = 'absolute';
            buttons.style.background = 'none';

            // Проверка на наличие ошибки в ответе
            if (data.no_data) {
                buttons.style.position = 'static';
                buttons.style.background = 'rgba(255, 255, 255, 0.5';
                graph.innerHTML = `<div class="error">${data.no_data}</div>`;
                return;
            }

            // Очищаем старый график
            Plotly.purge(graph);

            // Обновляем график
            const dates = data.map((item) => item.created_at);
            const temperatures = data.map((item) => item.temperature);
            const humidities = data.map((item) => item.humidity);

            Plotly.react(
                graph,
                [
                    {
                        x: dates,
                        y: humidities,
                        name: 'Влажность (%)',
                        line: { color: '#319fea' },
                        mode: showText ? 'lines+markers+text' : 'lines+text',
                        text: showText ? humidities.map((h) => `${h}%`) : [],
                        hoverinfo: 'none',
                        textposition: 'top',
                    },
                    {
                        x: dates,
                        y: temperatures,
                        name: 'Температура (°C)',
                        line: { color: '#f65f80' },
                        mode: showText ? 'lines+markers+text' : 'lines+text', // Линии + точки
                        text: showText ? temperatures.map((t) => `${t}°C`) : [],
                        hoverinfo: 'none', // Показать дату, значение и подпись при наведении
                        textposition: 'top', // Позиция текста
                    },
                ],
                {
                    title: {
                        text: 'Серверная №1',
                        font: {
                            size: 20,
                            color: '#333',
                            weight: 'bold',
                        },
                    },
                    xaxis: {
                        title: {
                            text: 'Дата и время',
                            font: {
                                size: 14,
                                color: '#333',
                                weight: 'bold',
                            },
                        },
                        fixedrange: true,
                    },
                    yaxis: {
                        title: {
                            text: 'Значение',
                            font: {
                                size: 14,
                                color: '#333',
                                weight: 'bold',
                            },
                        },
                        fixedrange: true,
                        range: [10, 80],
                        dtick: 10,
                    },
                    legend: {
                        x: 1,
                        y: 2,
                        xanchor: 'right',
                        yanchor: 'top',
                        clickable: false,
                        font: {
                            family: 'Arial, sans-serif',
                            size: 12,
                            color: '#333',
                        },
                        bgcolor: 'rgba(247, 247, 247, 0.5)',
                    },
                    dragmode: 'false',
                    plot_bgcolor: 'rgba(247, 247, 247, 0.5)', // Полупрозрачный фон графика
                    paper_bgcolor: 'rgba(255, 255, 255, 0.5)', // Полупрозрачный фон области графика
                },
                {
                    displayModeBar: false, // Отключаем панель инструментов
                    legendItemClick: false, // Отключает клики по легенде
                    legendItemDoubleClick: false, // Отключает двойной клик по легенде
                }
            );
        })
        .catch((error) => {
            console.error('Ошибка:', error);
            // graphContainer.innerHTML = `<div>Ошибка при получении данных.</div>`;
        });
}

setTimeout(updateGraphContainer, 1000);
// setInterval(updateGraphContainer, 10000);
