
from math import *

# conventions:
# 2D point: (x, y) tuple
# 2D line: (A, B, C) tuple, Ax + By + C == 0
# 2D circle: (x0, y0, R), hypot(x-x0, y-y0) == R

def bisector(a, b):
    """2D line equidistant to points 'a' and 'b'."""
    return (2*(b[0]-a[0]), 2*(b[1]-a[1]), a[0]*a[0] + a[1]*a[1] - b[0]*b[0] - b[1]*b[1])

def line_intersection(l1, l2):
    """Return common point in two lines or None if parallel."""
    (A1, B1, C1), (A2, B2, C2) = l1, l2
    W = A1 * B2 - B1 * A2
    if abs(W) < 1e-6:
        return None
    Wx = C1 * B2 - B1 * C2
    Wy = A1 * C2 - C1 * A2
    return (Wx/W, Wy/W)

def points_distance(a, b):
    """Euclidian."""
    return hypot(a[0]-b[0], a[1]-b[1])

def circle_through_points(a, b, c):
    """Circle through 'a', 'b' and 'c' or None if colinear."""
    center = line_intersection(bisector(a, b), bisector(b, c))
    if center is None:
        return None
    return center + (points_distance(a, center),)

def circular_segment_radius_theta(chord, sagitta):
    """Return radius and inner angle theta for given arc chord and sagitta."""
    c = circle_through_points((0, 0), (0.5*chord, sagitta), (chord, 0))
    if c is None:
        return None, None
    R = c[2]
    theta = 2*asin(0.5*chord/R)
    return R, theta

def circular_segment_area(chord, sagitta):
    """Compute area of segment sector given chord and sagitta lengths."""
    R, theta = circular_segment_radius_theta(chord, sagitta)
    if R is None:
        return None
    return 0.5 * R * R * (theta - sin(theta))

if __name__ == '__main__':
    print "Examples of circular segments:"
    for c, s in [(90, 10), (110, 20)]:
        print "Chord = %3d, Sagitta = %d:" % (c, s)
        A = circular_segment_area(c, s)
        R, th = circular_segment_radius_theta(c, s)
        print "\tArea: %7.2f (avg. h: %5.2f), R=%6.2f, th=%.2f(%.1f deg), arc length: %5.1f" % (
                       A,             A/c,      R,        th,  th*180/pi,             th*R
        )
