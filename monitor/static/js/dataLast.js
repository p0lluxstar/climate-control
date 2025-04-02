import { startProgressLoader } from './startProgressLoader.js';

const dataContainer = document.querySelector('.data-container');
const dataLast = document.querySelector('.data-last');
const loader = document.querySelector('.loader');
const currentFormattedDate = document.querySelector('.current-formatted-date');
const currentHumidity = document.querySelector('.current-humidity');
const currentTemperature = document.querySelector('.current-temperature');
const progressLastLoader = document.querySelector('.progress-last-loader');

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

        const currentDate = new Date();
        const localDate = new Date(currentDate.getTime() + 3 * 60 * 60 * 1000);
        const formattedDate = localDate.toISOString().replace('T', ' ').slice(0, 19);

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
