// WeakMap для отслеживания состояния остановки у каждого элемента
const stopProgressMap = new WeakMap();

export function startProgressLoader(functionUpdate, element, time) {
    if (!element) {
        console.error('Элемент не найден');
        return;
    }

    const totalTime = time;
    let startTime = Date.now();
    stopProgressMap.set(element, false); // Устанавливаем флаг остановки для конкретного элемента

    function updateProgress() {
        if (stopProgressMap.get(element)) return; // Останавливаем только этот экземпляр

        const currentTime = Date.now();
        const elapsedTime = currentTime - startTime;
        const progress = (elapsedTime / totalTime) * 100;

        element.style.background = `conic-gradient(#f08155 ${progress}%, #e0e0e0 ${progress}%)`;

        if (progress < 100) {
            requestAnimationFrame(updateProgress);
        } else {
            functionUpdate();
        }
    }

    requestAnimationFrame(updateProgress);
}

// Функция для остановки конкретного элемента
export function stopProgressLoader(element) {
    if (!element) return;
    stopProgressMap.set(element, true);
}
