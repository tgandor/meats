<?php

namespace App\Http\Controllers;

use App\Models\Series;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class ComparisonController extends Controller
{
    public function index(Request $request)
    {
        $allSeries = Auth::user()->is_admin
            ? Series::with('user')->orderBy('name')->get()
            : Auth::user()->series()->orderBy('name')->get();

        $selected = $request->input('ids', []);
        $mode = $request->input('mode', 'values'); // 'values' | 'derivative'

        $chartData = [];
        if (! empty($selected)) {
            foreach ($selected as $id) {
                $series = $allSeries->find($id);
                if (! $series) {
                    continue;
                }

                $points = $series->measurements()
                    ->orderBy('measured_at')
                    ->get(['measured_at', 'value']);

                if ($mode === 'derivative') {
                    $data = $this->computeDerivative($points);
                } else {
                    $data = $points->map(fn ($p) => [
                        'x' => $p->measured_at->toIso8601String(),
                        'y' => (float) $p->value,
                    ])->values()->toArray();
                }

                $chartData[] = [
                    'label' => $series->name . ($series->unit ? ' (' . $series->unit . ')' : ''),
                    'data' => $data,
                ];
            }
        }

        return view('comparison.index', compact('allSeries', 'selected', 'mode', 'chartData'));
    }

    private function computeDerivative($points): array
    {
        $result = [];
        $prev = null;
        foreach ($points as $p) {
            if ($prev !== null) {
                $dt = $p->measured_at->timestamp - $prev->measured_at->timestamp;
                if ($dt > 0) {
                    $dy = (float) $p->value - (float) $prev->value;
                    $result[] = [
                        'x' => $p->measured_at->toIso8601String(),
                        'y' => round($dy / ($dt / 3600), 6), // per hour
                    ];
                }
            }
            $prev = $p;
        }

        return $result;
    }
}
