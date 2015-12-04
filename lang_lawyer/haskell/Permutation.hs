-- module Permutation

selections []     = []
selections (x:xs) = (x,xs) : [ (y,x:ys) | (y,ys) <- selections xs ]

permutations :: [a] -> [[a]]
permutations [] = [[]]
permutations xs =
    [ (y : ys)
    | (y, zs) <- selections xs
    , ys <- permutations zs
    ]
