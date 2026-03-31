<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">Moje serie czasowe</h2>
            <div class="flex gap-2">
                <a href="{{ route('comparison.index') }}" class="px-3 py-1.5 text-sm bg-indigo-600 text-white rounded hover:bg-indigo-700">Porównaj</a>
                <a href="{{ route('series.create') }}" class="px-3 py-1.5 text-sm bg-green-600 text-white rounded hover:bg-green-700">+ Nowa seria</a>
            </div>
        </div>
    </x-slot>

    @if($series->isEmpty())
        <div class="text-center text-gray-500 dark:text-gray-400 py-16">
            <p class="text-lg">Nie masz jeszcze żadnych serii.</p>
            <a href="{{ route('series.create') }}" class="mt-4 inline-block px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Utwórz pierwszą serię</a>
        </div>
    @else
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            @foreach($series as $s)
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex flex-col gap-2">
                    <div class="flex justify-between items-start">
                        <div>
                            <a href="{{ route('series.show', $s) }}" class="text-lg font-semibold text-blue-600 dark:text-blue-400 hover:underline">{{ $s->name }}</a>
                            @if($s->unit)
                                <span class="ml-1 text-xs text-gray-500">[{{ $s->unit }}]</span>
                            @endif
                        </div>
                        <span class="text-xs px-1.5 py-0.5 rounded {{ $s->is_monotonic ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300' : 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' }}">
                            {{ $s->is_monotonic ? 'monot.' : 'swobodna' }}
                        </span>
                    </div>

                    @if($s->tags->isNotEmpty())
                        <div class="flex flex-wrap gap-1">
                            @foreach($s->tags as $tag)
                                <span class="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-1.5 py-0.5 rounded">{{ $tag->name }}</span>
                            @endforeach
                        </div>
                    @endif

                    @if($s->latestMeasurement)
                        <div class="text-sm text-gray-600 dark:text-gray-300">
                            Ostatni: <strong>{{ number_format($s->latestMeasurement->value, 2) }}</strong> {{ $s->unit }}
                            <span class="text-xs text-gray-400 ml-1">({{ $s->latestMeasurement->measured_at->diffForHumans() }})</span>
                        </div>
                    @else
                        <p class="text-sm text-gray-400 italic">Brak pomiarów</p>
                    @endif

                    @if($s->sampling_interval_hours && $s->isDueForMeasurement())
                        <div class="text-xs text-amber-600 dark:text-amber-400 font-medium">⚠ Przypomnienie: czas na pomiar!</div>
                    @endif

                    @if(auth()->user()->is_admin)
                        <div class="text-xs text-gray-400">właściciel: {{ $s->user->name }}</div>
                    @endif

                    <div class="flex gap-2 mt-auto pt-2 text-sm">
                        <a href="{{ route('series.show', $s) }}" class="text-blue-500 hover:underline">Podgląd</a>
                        <a href="{{ route('series.edit', $s) }}" class="text-yellow-500 hover:underline">Edytuj</a>
                        <a href="{{ route('measurements.export', $s) }}" class="text-green-600 hover:underline">CSV</a>
                        <form method="POST" action="{{ route('series.destroy', $s) }}" onsubmit="return confirm('Na pewno usunąć?')">
                            @csrf @method('DELETE')
                            <button type="submit" class="text-red-500 hover:underline">Usuń</button>
                        </form>
                    </div>
                </div>
            @endforeach
        </div>
    @endif
</x-app-layout>
