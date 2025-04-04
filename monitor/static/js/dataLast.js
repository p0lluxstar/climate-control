import { startProgressLoader } from './startProgressLoader.js';

const dataContainer = document.querySelector('.data-container');
const dataLast = document.querySelector('.data-last');
const loader = document.querySelector('.loader');
const currentFormattedDate = document.querySelector('.current-formatted-date');
const currentHumidity = document.querySelector('.current-humidity');
const currentTemperature = document.querySelector('.current-temperature');
const progressLastLoader = document.querySelector('.progress-last-loader');
const warningContainer = document.querySelector('.warning-container');
const warningMessege = document.querySelector('.warning-messege');

// Функция для получения и обновления последних данных
export async function updateLastData() {
    loader.style.display = 'none';

    try {
        const response = await fetch(WS_DATA_URL);
        const data = await response.json();

        if (!data || data.length === 0) {
            dataContainer.innerHTML = `<div class="error">No new data available.</div>`;
            return;
        }

        if (data.temperature <= MAX_TEMPERATURE) {
            warningContainer.style.display = 'none';
        } else {
            warningContainer.style.display = 'block';
            warningMessege.textContent = `🔥 Current temperature is higher ${MAX_TEMPERATURE}°C`;
        }

        const currentDate = new Date();
        const localDate = new Date(currentDate.getTime() + 0 * 60 * 60 * 1000);

        const day = String(localDate.getDate()).padStart(2, '0');
        const month = String(localDate.getMonth() + 1).padStart(2, '0'); // Месяцы от 0
        const year = localDate.getFullYear();

        const hours = String(localDate.getHours()).padStart(2, '0');
        const minutes = String(localDate.getMinutes()).padStart(2, '0');
        const seconds = String(localDate.getSeconds()).padStart(2, '0');

        const formattedDate = `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`;

        dataLast.style.display = 'flex';
        currentFormattedDate.innerHTML = `${formattedDate}`;
        currentHumidity.innerHTML = ` ${data.humidity}%`;
        currentTemperature.innerHTML = ` ${data.temperature}°C`;

        startProgressLoader(updateLastData, progressLastLoader, 3000);
    } catch (error) {
        console.error('Error when receiving data:', error);
        dataContainer.innerHTML = `Error when receiving data, in the data-last block`;
    }
}
