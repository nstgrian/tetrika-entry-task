def merge_intervals(timestamps: list[int]) -> list[tuple[int, int]]:
    if not timestamps or len(timestamps) % 2 != 0:
        return []

    intervals = [(timestamps[i], timestamps[i + 1]) for i in range(0, len(timestamps), 2)]
    intervals.sort()

    merged = []
    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            if current_start != current_end:
                merged.append((current_start, current_end))
            current_start, current_end = start, end
    if current_start != current_end:
        merged.append((current_start, current_end))
    return merged


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start = intervals['lesson'][0]
    lesson_end = intervals['lesson'][1]
    pupil_intervals = merge_intervals(intervals['pupil'])
    tutor_intervals = merge_intervals(intervals['tutor'])

    p_start = next((i for i, (start, end) in enumerate(pupil_intervals) if end >= lesson_start), len(pupil_intervals))
    p_end = next((i for i in range(len(pupil_intervals) - 1, -1, -1) if pupil_intervals[i][0] <= lesson_end), -1) + 1
    pupil_intervals = pupil_intervals[p_start:p_end]

    t_start = next((i for i, (start, end) in enumerate(tutor_intervals) if end >= lesson_start), len(tutor_intervals))
    t_end = next((i for i in range(len(tutor_intervals) - 1, -1, -1) if tutor_intervals[i][0] <= lesson_end), -1) + 1
    tutor_intervals = tutor_intervals[t_start:t_end]

    if not pupil_intervals or not tutor_intervals:
        return 0

    pupil_intervals[0] = (max(pupil_intervals[0][0], lesson_start), pupil_intervals[0][1])
    pupil_intervals[-1] = (pupil_intervals[-1][0], min(pupil_intervals[-1][1], lesson_end))

    tutor_intervals[0] = (max(tutor_intervals[0][0], lesson_start), tutor_intervals[0][1])
    tutor_intervals[-1] = (tutor_intervals[-1][0], min(tutor_intervals[-1][1], lesson_end))

    total_overlap = 0
    i, j = 0, 0
    while i < len(pupil_intervals) and j < len(tutor_intervals):
        pupil_start, pupil_end = pupil_intervals[i]
        tutor_start, tutor_end = tutor_intervals[j]

        overlap_start = max(pupil_start, tutor_start)
        overlap_end = min(pupil_end, tutor_end)

        if overlap_start <= overlap_end:
            total_overlap += overlap_end - overlap_start

        if pupil_end < tutor_end:
            i += 1
        else:
            j += 1

    return total_overlap
