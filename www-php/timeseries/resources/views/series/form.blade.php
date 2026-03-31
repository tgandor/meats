@php
    $isEdit = isset($series);
    $action = $isEdit ? route('series.update', $series) : route('series.store');
    $existingTags = $isEdit ? $series->tags->pluck('name')->toArray() : [];
@endphp

<x-app-layout>
    <x-slot name="header">
        <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">
            {{ $isEdit ? 'Edytuj serię: ' . $series->name : 'Nowa seria czasowa' }}
        </h2>
    </x-slot>

    <div class="max-w-2xl">
        <form method="POST" action="{{ $action }}" x-data="seriesForm({{ json_encode($existingTags) }})">
            @csrf
            @if($isEdit) @method('PUT') @endif

            @if($errors->any())
                <div class="mb-4 bg-red-100 dark:bg-red-900 border border-red-400 text-red-800 dark:text-red-200 px-4 py-2 rounded">
                    <ul class="list-disc list-inside text-sm">
                        @foreach($errors->all() as $error)
                            <li>{{ $error }}</li>
                        @endforeach
                    </ul>
                </div>
            @endif

            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 space-y-4">
                {{-- Name --}}
                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" for="name">Nazwa *</label>
                    <input type="text" id="name" name="name" value="{{ old('name', $series->name ?? '') }}"
                           required maxlength="100"
                           class="w-full border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500">
                </div>

                {{-- Unit --}}
                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" for="unit">Jednostka</label>
                    <input type="text" id="unit" name="unit" value="{{ old('unit', $series->unit ?? '') }}"
                           maxlength="30" placeholder="np. kWh, kg, °C"
                           class="w-full border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md shadow-sm">
                </div>

                {{-- Description --}}
                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" for="description">Opis</label>
                    <textarea id="description" name="description" rows="2" maxlength="500"
                              class="w-full border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md shadow-sm">{{ old('description', $series->description ?? '') }}</textarea>
                </div>

                {{-- Is monotonic --}}
                <div class="flex items-center gap-2">
                    <input type="hidden" name="is_monotonic" value="0">
                    <input type="checkbox" id="is_monotonic" name="is_monotonic" value="1"
                           {{ old('is_monotonic', $series->is_monotonic ?? false) ? 'checked' : '' }}
                           class="rounded border-gray-300 text-indigo-600">
                    <label for="is_monotonic" class="text-sm text-gray-700 dark:text-gray-300">
                        Seria monotoniczna (licznik — wartości tylko rosną)
                    </label>
                </div>

                {{-- Sampling interval --}}
                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" for="sampling_interval_hours">
                        Interwał pomiaru (godziny) — pozostaw puste by wyłączyć przypomnienia
                    </label>
                    <input type="number" id="sampling_interval_hours" name="sampling_interval_hours"
                           value="{{ old('sampling_interval_hours', $series->sampling_interval_hours ?? '') }}"
                           step="0.5" min="0.1" placeholder="np. 24"
                           class="w-full border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md shadow-sm">
                </div>

                {{-- Outlier sigma --}}
                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" for="outlier_sigma">
                        Próg outliera (sigma) — {{ old('outlier_sigma', $series->outlier_sigma ?? 3.0) }}σ
                    </label>
                    <input type="range" id="outlier_sigma" name="outlier_sigma"
                           value="{{ old('outlier_sigma', $series->outlier_sigma ?? 3.0) }}"
                           min="1" max="10" step="0.5"
                           class="w-full"
                           oninput="this.previousElementSibling.querySelector('label span') && (document.getElementById('sigma_label').textContent = this.value + 'σ')">
                    <span id="sigma_label" class="text-xs text-gray-500">{{ old('outlier_sigma', $series->outlier_sigma ?? 3.0) }}σ</span>
                    <script>
                        document.getElementById('outlier_sigma').addEventListener('input', function() {
                            document.getElementById('sigma_label').textContent = this.value + 'σ';
                        });
                    </script>
                </div>

                {{-- Tags --}}
                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Tagi</label>
                    <div class="flex flex-wrap gap-1 mb-2">
                        <template x-for="(tag, i) in selectedTags" :key="i">
                            <span class="flex items-center gap-1 bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 text-sm px-2 py-0.5 rounded">
                                <span x-text="tag"></span>
                                <input type="hidden" name="tags[]" :value="tag">
                                <button type="button" @click="removeTag(i)" class="text-indigo-400 hover:text-red-500 font-bold leading-none">&times;</button>
                            </span>
                        </template>
                    </div>
                    <div class="flex gap-2">
                        <input type="text" x-model="newTag" @keydown.enter.prevent="addTag()"
                               placeholder="Wpisz tag i naciśnij Enter lub kliknij istniejący..."
                               list="existing-tags"
                               class="flex-1 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md shadow-sm text-sm">
                        <datalist id="existing-tags">
                            @foreach($tags as $tag)
                                <option value="{{ $tag->name }}">
                            @endforeach
                        </datalist>
                        <button type="button" @click="addTag()" class="px-3 py-1 bg-indigo-600 text-white text-sm rounded">Dodaj</button>
                    </div>
                </div>

                <div class="flex justify-end gap-3 pt-2">
                    <a href="{{ $isEdit ? route('series.show', $series) : route('series.index') }}"
                       class="px-4 py-2 text-sm text-gray-600 dark:text-gray-300 hover:underline">Anuluj</a>
                    <button type="submit" class="px-4 py-2 bg-indigo-600 text-white text-sm rounded hover:bg-indigo-700">
                        {{ $isEdit ? 'Zapisz zmiany' : 'Utwórz serię' }}
                    </button>
                </div>
            </div>
        </form>
    </div>

    <script>
    function seriesForm(existingTags) {
        return {
            selectedTags: existingTags || [],
            newTag: '',
            addTag() {
                const t = this.newTag.trim();
                if (t && !this.selectedTags.includes(t)) this.selectedTags.push(t);
                this.newTag = '';
            },
            removeTag(i) { this.selectedTags.splice(i, 1); }
        };
    }
    </script>
</x-app-layout>
