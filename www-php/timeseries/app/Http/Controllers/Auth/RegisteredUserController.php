<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Models\Invitation;
use App\Models\User;
use Illuminate\Auth\Events\Registered;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\Rules;
use Illuminate\View\View;

class RegisteredUserController extends Controller
{
    /**
     * Display the invitation-based registration view.
     */
    public function create(Request $request): View
    {
        $token = $request->query('token', '');
        $invitation = Invitation::where('token', $token)->whereNull('used_at')->firstOrFail();
        return view('auth.register', compact('invitation'));
    }

    /**
     * Handle an incoming registration request via invitation token.
     */
    public function store(Request $request): RedirectResponse
    {
        $request->validate([
            'token' => ['required', 'string'],
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'string', 'lowercase', 'email', 'max:255', 'unique:' . User::class],
            'password' => ['required', 'confirmed', Rules\Password::defaults()],
        ]);

        $invitation = Invitation::where('token', $request->token)
            ->whereNull('used_at')
            ->firstOrFail();

        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password),
        ]);

        $invitation->update(['used_at' => now()]);

        event(new Registered($user));
        Auth::login($user);

        return redirect()->route('series.index');
    }
}
