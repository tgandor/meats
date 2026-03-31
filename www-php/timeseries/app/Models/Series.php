<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Series extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id', 'name', 'unit', 'description', 'is_monotonic',
        'sampling_interval_hours', 'outlier_sigma',
    ];

    protected function casts(): array
    {
        return [
            'is_monotonic' => 'boolean',
            'sampling_interval_hours' => 'float',
            'outlier_sigma' => 'float',
        ];
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function measurements(): HasMany
    {
        return $this->hasMany(Measurement::class)->orderBy('measured_at');
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class, 'series_tags');
    }

    public function latestMeasurement()
    {
        return $this->hasOne(Measurement::class)->latestOfMany('measured_at');
    }

    public function isDueForMeasurement(): bool
    {
        if (! $this->sampling_interval_hours) {
            return false;
        }
        $latest = $this->latestMeasurement;
        if (! $latest) {
            return true;
        }
        $nextDue = $latest->measured_at->addHours($this->sampling_interval_hours);

        return now()->gte($nextDue);
    }
}
