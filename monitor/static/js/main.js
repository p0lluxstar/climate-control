import { updateLastData } from './dataLast.js';
import { updateGraphData } from './dataGraph.js';

// Запускаем обновление данных в блоке last
setTimeout(() => {
    updateLastData();
}, 1000);

// Запускаем обновление данных в блоке chart
setTimeout(() => {
    updateGraphData();
}, 1000);
