<?php

namespace App\Services;

use App\Models\Series;
use Illuminate\Support\Collection;

class PredictionService
{
    private const WINDOW = 20;

    public function predict(Series $series, float $atTimestamp): ?float
    {
        $points = $series->measurements()
            ->latest('measured_at')
            ->limit(self::WINDOW)
            ->get(['value', 'measured_at'])
            ->sortBy('measured_at')
            ->values();

        if ($points->count() < 2) {
            return $points->last()?->value;
        }

        return $series->is_monotonic
            ? $this->linearRegression($points, $atTimestamp)
            : $this->ema($points, $atTimestamp);
    }

    /**
     * Simple linear regression using Unix timestamps as X axis.
     */
    private function linearRegression(Collection $points, float $targetTs): float
    {
        $n = $points->count();
        $xs = $points->map(fn ($p) => (float) $p->measured_at->timestamp)->values();
        $ys = $points->map(fn ($p) => (float) $p->value)->values();

        $sumX = $xs->sum();
        $sumY = $ys->sum();
        $sumXY = 0;
        $sumX2 = 0;
        for ($i = 0; $i < $n; $i++) {
            $sumXY += $xs[$i] * $ys[$i];
            $sumX2 += $xs[$i] * $xs[$i];
        }

        $denom = $n * $sumX2 - $sumX * $sumX;
        if ($denom == 0) {
            return $ys->last();
        }
        $slope = ($n * $sumXY - $sumX * $sumY) / $denom;
        $intercept = ($sumY - $slope * $sumX) / $n;

        return $slope * $targetTs + $intercept;
    }

    /**
     * Exponential Moving Average; returns last EMA as point prediction.
     * For non-monotonic series we don't extrapolate across time, just predict
     * "next value will be similar to recent trend."
     */
    private function ema(Collection $points, float $targetTs): float
    {
        $alpha = 0.3;
        $ema = (float) $points->first()->value;
        foreach ($points->skip(1) as $point) {
            $ema = $alpha * (float) $point->value + (1 - $alpha) * $ema;
        }

        return $ema;
    }
}
