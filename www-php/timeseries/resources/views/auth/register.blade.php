@if(isset($invitation))
    @include('invitations.register')
@else
    <x-guest-layout>
        <div class="text-center text-gray-600 dark:text-gray-400 py-8">
            <p>Rejestracja możliwa tylko przez zaproszenie.</p>
            <a href="{{ route('login') }}" class="text-indigo-600 hover:underline mt-2 inline-block">← Zaloguj się</a>
        </div>
    </x-guest-layout>
@endif
