<?php

use App\Http\Controllers\ComparisonController;
use App\Http\Controllers\InvitationController;
use App\Http\Controllers\MeasurementController;
use App\Http\Controllers\ProfileController;
use App\Http\Controllers\PushSubscriptionController;
use App\Http\Controllers\SeriesController;
use Illuminate\Support\Facades\Route;

Route::get('/', fn () => redirect()->route('series.index'));

Route::middleware(['auth'])->group(function () {
    // Dashboard redirect
    Route::get('/dashboard', fn () => redirect()->route('series.index'))->name('dashboard');

    // Profile (Breeze)
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');

    // Series CRUD
    Route::resource('series', SeriesController::class);

    // Measurements
    Route::post('series/{series}/measurements', [MeasurementController::class, 'store'])->name('measurements.store');
    Route::get('series/{series}/measurements/preview', [MeasurementController::class, 'preview'])->name('measurements.preview');
    Route::delete('series/{series}/measurements/{measurement}', [MeasurementController::class, 'destroy'])->name('measurements.destroy');
    Route::get('series/{series}/export', [MeasurementController::class, 'export'])->name('measurements.export');

    // Comparison
    Route::get('/compare', [ComparisonController::class, 'index'])->name('comparison.index');

    // Invitations (admin)
    Route::get('/invitations', [InvitationController::class, 'index'])->name('invitations.index');
    Route::post('/invitations', [InvitationController::class, 'store'])->name('invitations.store');
    Route::delete('/invitations/{invitation}', [InvitationController::class, 'destroy'])->name('invitations.destroy');

    // Push
    Route::post('/push/subscribe', [PushSubscriptionController::class, 'store'])->name('push.subscribe');
    Route::post('/push/unsubscribe', [PushSubscriptionController::class, 'destroy'])->name('push.unsubscribe');
});

// Invitation registration (public routes by token)
Route::get('/invite/{token}', [InvitationController::class, 'show'])->name('invitation.show');

require __DIR__.'/auth.php';
