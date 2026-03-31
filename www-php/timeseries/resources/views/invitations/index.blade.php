<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">Zaproszenia</h2>
        </div>
    </x-slot>

    @if(session('invite_link'))
        <div class="mb-4 bg-blue-100 dark:bg-blue-900 border border-blue-400 text-blue-800 dark:text-blue-200 px-4 py-3 rounded">
            <p class="text-sm font-medium mb-1">Link zaproszeń (skopiuj i przekaż użytkownikowi):</p>
            <code class="text-xs break-all select-all bg-white dark:bg-gray-800 px-2 py-1 rounded block">{{ session('invite_link') }}</code>
        </div>
    @endif

    <div class="mb-6 bg-white dark:bg-gray-800 rounded-lg shadow p-4 max-w-md">
        <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Wygeneruj zaproszenie</h3>
        <form method="POST" action="{{ route('invitations.store') }}" class="flex gap-2">
            @csrf
            <input type="email" name="email" placeholder="E-mail zapraszanego (opcjonalnie)"
                   class="flex-1 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md shadow-sm text-sm">
            <button type="submit" class="px-4 py-2 bg-indigo-600 text-white text-sm rounded hover:bg-indigo-700">Generuj</button>
        </form>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <table class="min-w-full text-sm divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 font-medium">E-mail</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 font-medium">Wygenerowano</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 font-medium">Status</th>
                    <th class="px-4 py-2"></th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
                @forelse($invitations as $inv)
                    <tr>
                        <td class="px-4 py-2 text-gray-700 dark:text-gray-300">{{ $inv->email ?: '—' }}</td>
                        <td class="px-4 py-2 text-gray-500 dark:text-gray-400 tabular-nums">{{ $inv->created_at->format('Y-m-d H:i') }}</td>
                        <td class="px-4 py-2">
                            @if($inv->used_at)
                                <span class="text-green-600 text-xs">Użyte {{ $inv->used_at->format('Y-m-d') }}</span>
                            @else
                                <span class="text-amber-600 text-xs">Oczekuje</span>
                            @endif
                        </td>
                        <td class="px-4 py-2 text-right">
                            @unless($inv->used_at)
                                <button onclick="navigator.clipboard.writeText('{{ route('invitation.show', $inv->token) }}')" class="text-xs text-blue-500 hover:underline mr-2">kopiuj link</button>
                            @endunless
                            <form method="POST" action="{{ route('invitations.destroy', $inv) }}" class="inline" onsubmit="return confirm('Usunąć zaproszenie?')">
                                @csrf @method('DELETE')
                                <button type="submit" class="text-xs text-red-500 hover:underline">usuń</button>
                            </form>
                        </td>
                    </tr>
                @empty
                    <tr><td colspan="4" class="px-4 py-6 text-center text-gray-400">Brak zaproszeń</td></tr>
                @endforelse
            </tbody>
        </table>
    </div>
</x-app-layout>
