import unittest
from solution import appearance, merge_intervals


class TestMergeFunction(unittest.TestCase):
    def test_merge_no_overlap(self):
        no_overlap = [-1, 0, 1, 2, 3, 4, 5, 6, 99, 100]
        expected = [(-1, 0), (1, 2), (3, 4), (5, 6), (99, 100)]
        merged = merge_intervals(no_overlap)
        self.assertEqual(expected, merged)

    def test_zero_length(self):
        zero_length = [-1, -1, 0, 1, 2, 2, 3, 4, 4, 4]
        expected = [(0, 1), (3, 4)]
        merged = merge_intervals(zero_length)
        self.assertEqual(expected, merged)

    def test_merge_partial_overlap(self):
        partial_overlap = [-1, 1, 1, 2, 3, 5, 4, 7, 6, 8, 9, 10]
        expected = [(-1, 2), (3, 8), (9, 10)]
        merged = merge_intervals(partial_overlap)
        self.assertEqual(expected, merged)

    def test_merge_one_inside_another(self):
        one_inside_another = [-1, 2, -1, 0, 3, 7, 4, 5, 8, 10, 9, 10]
        expected = [(-1, 2), (3, 7), (8, 10)]
        merged = merge_intervals(one_inside_another)
        self.assertEqual(expected, merged)

    def test_merge_mixed(self):
        mixed = [-1, 2, 0, 2, 1, 4, 1, 4, 1, 5, 7, 10, 7, 8, 6, 10]
        expected = [(-1, 5), (6, 10)]
        merged = merge_intervals(mixed)
        self.assertEqual(expected, merged)


class TestAppearanceFunction(unittest.TestCase):
    def test_weak_conditions(self):
        """No overlaps"""
        intervals = {
            'lesson': [1594663200, 1594666800],
            'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
            'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
        }
        expected = 3117
        calculated = appearance(intervals)
        self.assertEqual(expected, calculated)

    def test_interior_overlap(self):
        intervals = {
            'lesson': [0, 1000000000000000],
            'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734,
                      1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875,
                      1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
            'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]
        }
        expected = 3651
        calculated = appearance(intervals)
        self.assertEqual(expected, calculated)

    def test_boundary_overlap(self):
        intervals = {
            'lesson': [159469_3000, 159469_4000],
            'pupil': [1594692033, 1594696347],
            'tutor': [1594692017, 1594692066, 1594692068, 1594696341]
        }
        expected = 1000
        calculated = appearance(intervals)
        self.assertEqual(expected, calculated)

    def test_mixed(self):
        intervals = {
            'lesson': [1594702800, 1594706400],
            'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734,
                      1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875,
                      1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
            'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]
        }
        expected = 3577
        calculated = appearance(intervals)
        self.assertEqual(expected, calculated)


if __name__ == '__main__':
    unittest.main()
