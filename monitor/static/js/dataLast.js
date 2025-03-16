// Функция для получения и обновления последних данных
export async function updateLastData() {
    const dataContainer = document.querySelector('.data-container');

    try {
        const response = await fetch(WS_DATA_URL);
        const data = await response.json();

        if (!data || data.length === 0) {
            dataContainer.innerHTML = `<div class="error">No new data available.</div>`;
            return;
        }

        const currentDate = new Date();
        const localDate = new Date(currentDate.getTime() + 3 * 60 * 60 * 1000);
        const formattedDate = localDate.toISOString().replace('T', ' ').slice(0, 19);

        dataContainer.innerHTML = `
            <div class="data-last">
                <div class="title-container">
                    <div class="title">Last sensor measurement</div>
                    <div class="progress-loader">
                        <div class="progress"></div>
                    </div>
                </div>    
                <div class="date">Date and time: ${formattedDate}</div>
                <div class="humidity">Current humidity:<span>${data.humidity}%</span></div>
                <div class="temperature">Current temperature:<span>${data.temperature}°C</span></div>
            </div>
        `;

        // Запускаем прогресс-лоадер
        startProgressLoader();
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
        dataContainer.innerHTML = `Ошибка при получении данных`;
    }
}

// Функция для запуска прогресс-лоадера
export function startProgressLoader() {
    const progressLoader = document.querySelector('.progress-loader');
    // const progressText = document.querySelector('.progress');

    const totalTime = 3000; // Время одного цикла в миллисекундах (30 секунд)
    let startTime = Date.now();

    function updateProgress() {
        const currentTime = Date.now();
        const elapsedTime = currentTime - startTime;
        const progress = (elapsedTime / totalTime) * 100;

        progressLoader.style.background = `conic-gradient(#f08155 ${progress}%, #e0e0e0 ${progress}%)`;
        // progressText.textContent = `${Math.round(progress)}%`;

        if (progress < 100) {
            requestAnimationFrame(updateProgress); // Продолжаем анимацию
        } else {
            // Когда прогресс достигает 100%, отправляем новый запрос и обновляем данные
            updateLastData();
        }
    }

    requestAnimationFrame(updateProgress); // Запускаем анимацию
}
