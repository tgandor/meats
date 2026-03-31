import './bootstrap';
import Alpine from 'alpinejs';
import Chart from 'chart.js/auto';
import flatpickr from 'flatpickr';
import { Polish } from 'flatpickr/dist/l10n/pl.js';

window.Alpine = Alpine;
window.Chart = Chart;
window.flatpickr = flatpickr;

// Flatpickr Polish locale default
flatpickr.setDefaults({ locale: Polish, enableTime: true, time_24hr: true, dateFormat: 'Y-m-d H:i' });

Alpine.start();
