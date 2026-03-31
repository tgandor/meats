<?php

namespace App\Http\Controllers;

use App\Models\PushSubscription;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class PushSubscriptionController extends Controller
{
    public function store(Request $request)
    {
        $request->validate([
            'endpoint' => 'required|url|max:2000',
            'public_key' => 'required|string|max:200',
            'auth_token' => 'required|string|max:100',
        ]);

        PushSubscription::updateOrCreate(
            ['user_id' => Auth::id(), 'public_key' => $request->public_key],
            [
                'endpoint' => $request->endpoint,
                'auth_token' => $request->auth_token,
            ]
        );

        return response()->json(['status' => 'subscribed']);
    }

    public function destroy(Request $request)
    {
        $request->validate(['endpoint' => 'required|string|max:2000']);

        PushSubscription::where('user_id', Auth::id())
            ->where('endpoint', $request->endpoint)
            ->delete();

        return response()->json(['status' => 'unsubscribed']);
    }
}
