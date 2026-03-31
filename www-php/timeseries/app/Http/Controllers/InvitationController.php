<?php

namespace App\Http\Controllers;

use App\Models\Invitation;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Str;

class InvitationController extends Controller
{
    public function index()
    {
        $this->requireAdmin();
        $invitations = Invitation::with('creator')->latest()->get();
        return view('invitations.index', compact('invitations'));
    }

    public function store(Request $request)
    {
        $this->requireAdmin();
        $request->validate(['email' => 'nullable|email|max:255']);

        $invitation = Invitation::create([
            'token' => Str::random(48),
            'email' => $request->input('email'),
            'created_by' => Auth::id(),
        ]);

        $link = route('invitation.show', $invitation->token);

        return redirect()->route('invitations.index')
            ->with('invite_link', $link)
            ->with('success', 'Zaproszenie wygenerowane.');
    }

    public function show(string $token)
    {
        $invitation = Invitation::where('token', $token)->whereNull('used_at')->firstOrFail();
        return view('invitations.register', compact('invitation'));
    }

    public function destroy(Invitation $invitation)
    {
        $this->requireAdmin();
        $invitation->delete();
        return redirect()->route('invitations.index')->with('success', 'Zaproszenie usunięte.');
    }

    private function requireAdmin(): void
    {
        if (! Auth::user()?->is_admin) {
            abort(403);
        }
    }
}
