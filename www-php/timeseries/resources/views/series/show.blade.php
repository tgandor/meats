<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center flex-wrap gap-2">
            <div>
                <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">
                    {{ $series->name }}
                    @if($series->unit) <span class="text-sm font-normal text-gray-500">[{{ $series->unit }}]</span> @endif
                </h2>
                <div class="flex gap-1 mt-1 flex-wrap">
                    <span class="text-xs px-1.5 py-0.5 rounded {{ $series->is_monotonic ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700' }}">
                        {{ $series->is_monotonic ? 'monotoniczna' : 'swobodna' }}
                    </span>
                    @foreach($series->tags as $tag)
                        <span class="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-1.5 py-0.5 rounded">{{ $tag->name }}</span>
                    @endforeach
                    @if(auth()->user()->is_admin && $series->user_id !== auth()->id())
                        <span class="text-xs bg-yellow-100 text-yellow-700 px-1.5 py-0.5 rounded">właściciel: {{ $series->user->name }}</span>
                    @endif
                </div>
            </div>
            <div class="flex gap-2">
                <a href="{{ route('measurements.export', $series) }}" class="px-3 py-1.5 text-sm bg-green-600 text-white rounded hover:bg-green-700">↓ CSV</a>
                <a href="{{ route('series.edit', $series) }}" class="px-3 py-1.5 text-sm bg-yellow-500 text-white rounded hover:bg-yellow-600">Edytuj</a>
                <a href="{{ route('series.index') }}" class="px-3 py-1.5 text-sm bg-gray-500 text-white rounded hover:bg-gray-600">← Wróć</a>
            </div>
        </div>
    </x-slot>

    {{-- Chart --}}
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 mb-6">
        <div class="flex justify-between items-center mb-2">
            <h3 class="font-medium text-gray-700 dark:text-gray-300">Wykres</h3>
            <select id="chartRange" class="text-sm border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded">
                <option value="all">Wszystkie dane</option>
                <option value="30">Ostatnie 30 dni</option>
                <option value="90">Ostatnie 90 dni</option>
                <option value="365">Ostatni rok</option>
            </select>
        </div>
        <canvas id="seriesChart" height="120"></canvas>
    </div>

    {{-- Add measurement --}}
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 mb-6" x-data="addMeasurementForm()">
        <h3 class="font-medium text-gray-700 dark:text-gray-300 mb-3">Dodaj pomiar</h3>
        <form method="POST" action="{{ route('measurements.store', $series) }}" class="flex flex-wrap gap-3 items-end">
            @csrf
            <div>
                <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Wartość ({{ $series->unit ?: '—' }}) *</label>
                <input type="number" name="value" id="measureValue" step="any" required
                       x-model="formValue"
                       @input.debounce.500ms="fetchPreview"
                       class="border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md shadow-sm w-36">
            </div>
            <div>
                <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Data i czas *</label>
                <input type="text" name="measured_at" id="measuredAt" required
                       class="border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md shadow-sm w-44"
                       x-init="flatpickr($el)">
            </div>
            <div class="flex-1 min-w-32">
                <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Notatka</label>
                <input type="text" name="note" maxlength="255"
                       class="w-full border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md shadow-sm">
            </div>
            <button type="submit" class="px-4 py-2 bg-indigo-600 text-white text-sm rounded hover:bg-indigo-700">Zapisz</button>
        </form>

        {{-- Prediction / outlier info --}}
        <div class="mt-2 text-sm" x-show="preview !== null">
            <template x-if="preview">
                <div :class="preview.is_outlier ? 'text-red-600 dark:text-red-400' : 'text-gray-500 dark:text-gray-400'">
                    <template x-if="preview.predicted !== null">
                        <span>Prognoza: <strong x-text="preview.predicted"></strong> {{ $series->unit }}</span>
                    </template>
                    <template x-if="preview.is_outlier">
                        <span class="ml-2 font-semibold">⚠ Outlier! z = <span x-text="preview.z_score"></span>σ (próg: {{ $series->outlier_sigma }}σ)</span>
                    </template>
                    <template x-if="!preview.is_outlier && preview.z_score !== null">
                        <span class="ml-2 text-green-600 dark:text-green-400">✓ W normie (z = <span x-text="preview.z_score"></span>σ)</span>
                    </template>
                </div>
            </template>
        </div>
    </div>

    {{-- Measurements table --}}
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <table class="min-w-full text-sm divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 dark:text-gray-300 font-medium">Data/czas</th>
                    <th class="px-4 py-2 text-right text-xs text-gray-500 dark:text-gray-300 font-medium">Wartość</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 dark:text-gray-300 font-medium">Notatka</th>
                    <th class="px-4 py-2"></th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
                @forelse($measurements as $m)
                    <tr class="hover:bg-gray-50 dark:hover:bg-gray-750">
                        <td class="px-4 py-2 text-gray-700 dark:text-gray-300 tabular-nums">{{ $m->measured_at->format('Y-m-d H:i') }}</td>
                        <td class="px-4 py-2 text-right font-mono text-gray-900 dark:text-white">{{ rtrim(rtrim(number_format($m->value, 4), '0'), '.') }} {{ $series->unit }}</td>
                        <td class="px-4 py-2 text-gray-500 dark:text-gray-400">{{ $m->note }}</td>
                        <td class="px-4 py-2 text-right">
                            <form method="POST" action="{{ route('measurements.destroy', [$series, $m]) }}" onsubmit="return confirm('Usunąć ten pomiar?')">
                                @csrf @method('DELETE')
                                <button type="submit" class="text-xs text-red-500 hover:text-red-700">usuń</button>
                            </form>
                        </td>
                    </tr>
                @empty
                    <tr><td colspan="4" class="px-4 py-6 text-center text-gray-400">Brak pomiarów</td></tr>
                @endforelse
            </tbody>
        </table>
        @if($measurements->hasPages())
            <div class="p-3">{{ $measurements->links() }}</div>
        @endif
    </div>

    <script>
    // Pass measurement data to Chart.js
    const rawData = @json($series->measurements()->orderBy('measured_at')->get(['measured_at','value'])->map(fn($m) => ['x' => $m->measured_at->toIso8601String(), 'y' => (float)$m->value]));

    function buildChart(data) {
        const ctx = document.getElementById('seriesChart').getContext('2d');
        if (window._seriesChart) window._seriesChart.destroy();
        window._seriesChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: '{{ addslashes($series->name) }} ({{ addslashes($series->unit) }})',
                    data: data,
                    borderColor: 'rgb(99, 102, 241)',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 2,
                    pointRadius: data.length <= 100 ? 3 : 0,
                    tension: 0.2,
                    fill: true,
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: { type: 'time', time: { tooltipFormat: 'yyyy-MM-dd HH:mm' } },
                    y: { title: { display: true, text: '{{ addslashes($series->unit) }}' } }
                },
                plugins: { legend: { display: false } }
            }
        });
    }

    buildChart(rawData);

    document.getElementById('chartRange').addEventListener('change', function() {
        const days = parseInt(this.value);
        if (!days) { buildChart(rawData); return; }
        const cutoff = new Date();
        cutoff.setDate(cutoff.getDate() - days);
        buildChart(rawData.filter(p => new Date(p.x) >= cutoff));
    });

    function addMeasurementForm() {
        return {
            formValue: '',
            preview: null,
            fetchPreview() {
                if (!this.formValue) { this.preview = null; return; }
                fetch('{{ route('measurements.preview', $series) }}?value=' + encodeURIComponent(this.formValue), {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                }).then(r => r.json()).then(d => { this.preview = d; });
            }
        };
    }
    </script>
</x-app-layout>
