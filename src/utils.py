def is_crossing_line(line_start, line_end, point_prev, point_curr):
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    A = line_start
    B = line_end
    C = point_prev
    D = point_curr
    
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
