<?php

namespace App\Http\Controllers;

use App\Models\Series;
use App\Models\Tag;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class SeriesController extends Controller
{
    public function index()
    {
        $query = Auth::user()->is_admin
            ? Series::with(['user', 'tags', 'latestMeasurement'])
            : Auth::user()->series()->with(['tags', 'latestMeasurement']);

        $series = $query->orderBy('name')->get();

        return view('series.index', compact('series'));
    }

    public function create()
    {
        $tags = Tag::orderBy('name')->get();
        return view('series.create', compact('tags'));
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:100',
            'unit' => 'nullable|string|max:30',
            'description' => 'nullable|string|max:500',
            'is_monotonic' => 'boolean',
            'sampling_interval_hours' => 'nullable|numeric|min:0.1',
            'outlier_sigma' => 'required|numeric|min:1|max:10',
            'tags' => 'nullable|array',
            'tags.*' => 'string|max:50',
        ]);

        $series = Auth::user()->series()->create([
            'name' => $validated['name'],
            'unit' => $validated['unit'] ?? '',
            'description' => $validated['description'] ?? null,
            'is_monotonic' => $request->boolean('is_monotonic'),
            'sampling_interval_hours' => $validated['sampling_interval_hours'] ?? null,
            'outlier_sigma' => $validated['outlier_sigma'],
        ]);

        $this->syncTags($series, $validated['tags'] ?? []);

        return redirect()->route('series.show', $series)
            ->with('success', 'Seria "' . $series->name . '" została utworzona.');
    }

    public function show(Series $series)
    {
        $this->authorizeAccess($series);

        $measurements = $series->measurements()
            ->orderBy('measured_at', 'desc')
            ->paginate(50);

        return view('series.show', compact('series', 'measurements'));
    }

    public function edit(Series $series)
    {
        $this->authorizeAccess($series);
        $tags = Tag::orderBy('name')->get();

        return view('series.edit', compact('series', 'tags'));
    }

    public function update(Request $request, Series $series)
    {
        $this->authorizeAccess($series);

        $validated = $request->validate([
            'name' => 'required|string|max:100',
            'unit' => 'nullable|string|max:30',
            'description' => 'nullable|string|max:500',
            'is_monotonic' => 'boolean',
            'sampling_interval_hours' => 'nullable|numeric|min:0.1',
            'outlier_sigma' => 'required|numeric|min:1|max:10',
            'tags' => 'nullable|array',
            'tags.*' => 'string|max:50',
        ]);

        $series->update([
            'name' => $validated['name'],
            'unit' => $validated['unit'] ?? '',
            'description' => $validated['description'] ?? null,
            'is_monotonic' => $request->boolean('is_monotonic'),
            'sampling_interval_hours' => $validated['sampling_interval_hours'] ?? null,
            'outlier_sigma' => $validated['outlier_sigma'],
        ]);

        $this->syncTags($series, $validated['tags'] ?? []);

        return redirect()->route('series.show', $series)
            ->with('success', 'Seria zaktualizowana.');
    }

    public function destroy(Series $series)
    {
        $this->authorizeAccess($series);
        $name = $series->name;
        $series->delete();

        return redirect()->route('series.index')
            ->with('success', '"' . $name . '" usunięta.');
    }

    private function authorizeAccess(Series $series): void
    {
        $user = Auth::user();
        if (! $user->is_admin && $series->user_id !== $user->id) {
            abort(403);
        }
    }

    private function syncTags(Series $series, array $tagNames): void
    {
        $tagIds = collect($tagNames)
            ->filter()
            ->map(fn (string $name) => Tag::firstOrCreate(['name' => trim($name)])->id)
            ->unique()
            ->toArray();

        $series->tags()->sync($tagIds);
    }
}
