<?php

namespace App\Http\Controllers;

use App\Models\Measurement;
use App\Models\Series;
use App\Services\OutlierDetector;
use App\Services\PredictionService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class MeasurementController extends Controller
{
    public function store(Request $request, Series $series)
    {
        $this->authorizeAccess($series);

        $validated = $request->validate([
            'value' => 'required|numeric',
            'measured_at' => 'required|date',
            'note' => 'nullable|string|max:255',
        ]);

        $measurement = $series->measurements()->create([
            'value' => $validated['value'],
            'measured_at' => $validated['measured_at'],
            'note' => $validated['note'] ?? null,
        ]);

        if ($request->expectsJson()) {
            return response()->json(['measurement' => $measurement]);
        }

        return redirect()->route('series.show', $series)
            ->with('success', 'Pomiar dodany.');
    }

    public function preview(Request $request, Series $series)
    {
        $this->authorizeAccess($series);

        $value = (float) $request->input('value');

        $prediction = app(PredictionService::class)
            ->predict($series, now()->timestamp);

        $zScore = app(OutlierDetector::class)->zScore($series, $value);
        $isOutlier = $zScore !== null && $zScore > $series->outlier_sigma;

        return response()->json([
            'predicted' => $prediction !== null ? round($prediction, 4) : null,
            'z_score' => $zScore !== null ? round($zScore, 2) : null,
            'is_outlier' => $isOutlier,
            'outlier_sigma' => $series->outlier_sigma,
        ]);
    }

    public function destroy(Series $series, Measurement $measurement)
    {
        $this->authorizeAccess($series);

        if ($measurement->series_id !== $series->id) {
            abort(404);
        }

        $measurement->delete();

        return redirect()->route('series.show', $series)
            ->with('success', 'Pomiar usunięty.');
    }

    public function export(Series $series)
    {
        $this->authorizeAccess($series);

        $measurements = $series->measurements()
            ->orderBy('measured_at')
            ->get(['measured_at', 'value', 'note']);

        $filename = preg_replace('/[^a-z0-9_-]/i', '_', $series->name) . '_export.csv';

        $headers = [
            'Content-Type' => 'text/csv; charset=UTF-8',
            'Content-Disposition' => 'attachment; filename="' . $filename . '"',
        ];

        $callback = function () use ($measurements, $series) {
            $fh = fopen('php://output', 'w');
            fputs($fh, "\xEF\xBB\xBF"); // UTF-8 BOM for Excel
            fputcsv($fh, ['datetime', 'value (' . $series->unit . ')', 'note']);
            foreach ($measurements as $m) {
                fputcsv($fh, [
                    $m->measured_at->toDateTimeString(),
                    (string) $m->value,
                    $m->note ?? '',
                ]);
            }
            fclose($fh);
        };

        return response()->stream($callback, 200, $headers);
    }

    private function authorizeAccess(Series $series): void
    {
        $user = Auth::user();
        if (! $user->is_admin && $series->user_id !== $user->id) {
            abort(403);
        }
    }
}
