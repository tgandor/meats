<?php

namespace App\Services;

use App\Models\Series;

class OutlierDetector
{
    private const WINDOW = 30;

    /**
     * Returns z-score of $value against recent measurements.
     * Returns null if there are fewer than 3 data points (not enough baseline).
     */
    public function zScore(Series $series, float $value): ?float
    {
        $values = $series->measurements()
            ->latest('measured_at')
            ->limit(self::WINDOW)
            ->pluck('value')
            ->map(fn ($v) => (float) $v);

        if ($values->count() < 3) {
            return null;
        }

        $n = $values->count();
        $mean = $values->sum() / $n;
        $variance = $values->map(fn ($v) => ($v - $mean) ** 2)->sum() / $n;
        $stddev = sqrt($variance);

        if ($stddev < 1e-9) {
            return 0.0;
        }

        return abs($value - $mean) / $stddev;
    }

    public function isOutlier(Series $series, float $value): bool
    {
        $z = $this->zScore($series, $value);

        return $z !== null && $z > $series->outlier_sigma;
    }
}
