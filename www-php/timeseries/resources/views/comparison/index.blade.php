<x-app-layout>
    <x-slot name="header">
        <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">Porównaj serie</h2>
    </x-slot>

    <form method="GET" action="{{ route('comparison.index') }}" x-data="{ mode: '{{ $mode }}' }">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 mb-4 flex flex-wrap gap-4 items-end">
            <div class="flex-1 min-w-48">
                <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Serie (Ctrl+klik = multi)</label>
                <select name="ids[]" multiple size="6"
                        class="w-full border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md shadow-sm text-sm">
                    @foreach($allSeries as $s)
                        <option value="{{ $s->id }}" {{ in_array($s->id, $selected) ? 'selected' : '' }}>
                            {{ $s->name }} @if($s->unit)[{{ $s->unit }}]@endif
                            @if(auth()->user()->is_admin) ({{ $s->user->name }}) @endif
                        </option>
                    @endforeach
                </select>
            </div>
            <div>
                <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Tryb</label>
                <select name="mode" x-model="mode" class="border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md shadow-sm text-sm">
                    <option value="values">Wartości</option>
                    <option value="derivative">Pochodna (zmiana / godz.)</option>
                </select>
            </div>
            <button type="submit" class="px-4 py-2 bg-indigo-600 text-white text-sm rounded hover:bg-indigo-700">Pokaż wykres</button>
        </div>
    </form>

    @if(!empty($selected) && !empty($chartData))
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
            <h3 class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-3">
                {{ $mode === 'derivative' ? 'Pochodna (zmiana/godz.)' : 'Porównanie wartości' }}
            </h3>
            <canvas id="compareChart" height="100"></canvas>
        </div>

        <script>
        const compareData = @json($chartData);
        const colors = [
            'rgb(99,102,241)', 'rgb(244,63,94)', 'rgb(34,197,94)',
            'rgb(251,146,60)', 'rgb(14,165,233)', 'rgb(168,85,247)',
        ];
        const ctx = document.getElementById('compareChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                datasets: compareData.map((ds, i) => ({
                    label: ds.label,
                    data: ds.data,
                    borderColor: colors[i % colors.length],
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: ds.data.length <= 100 ? 3 : 0,
                    tension: 0.2,
                }))
            },
            options: {
                responsive: true,
                scales: {
                    x: { type: 'time', time: { tooltipFormat: 'yyyy-MM-dd HH:mm' } }
                }
            }
        });
        </script>
    @elseif(!empty($selected))
        <p class="text-gray-500 dark:text-gray-400 text-sm">Wybrane serie nie mają wspólnych danych.</p>
    @else
        <p class="text-gray-400 dark:text-gray-500 text-sm">Wybierz co najmniej jedną serię z listy powyżej.</p>
    @endif
</x-app-layout>
