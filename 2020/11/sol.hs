firsteq :: [[String]] ->  [String]
firsteq (x:y:rest) = if x == y then x else firsteq (y:rest)

evolutions :: [String] -> [[String]]
evolutions state = state:(evolutions (evolve' state))

evolve :: [String] -> [String]
evolve a = map evolveLine (tripZipPadded "" a)

tripZip a b c = zip a (zip b c)
tripZipPadded pad a = tripZip ([pad] ++ a) a ((tail a) ++ [pad])

evolveLine :: (String, (String, String)) -> String
evolveLine ("", (main, below)) = evolveLine ([' ',' '..], (main, below))
evolveLine (above, (main, "")) = evolveLine (above, (main, [' ',' '..]))
evolveLine (above, (main, below)) = map evolveChar (tripZip (tripZipPadded ' ' above) (tripZipPadded ' ' main) (tripZipPadded ' ' below))

evolveChar :: ((Char, (Char, Char)), ((Char, (Char, Char)), (Char, (Char, Char)))) -> Char
evolveChar ((ul, (um, ur)), ((l, (me, r)), (dl, (dm, dr)))) = let c = count '#' [ul,um,ur,l,r,dl,dm,dr]
       in if me == '.' then '.' else (if c == 0 then '#' else (if c >= 4 then 'L' else me))

evolve' :: [String] -> [String]
evolve' a = map (evolveLine' a) $ zip [0..] a

evolveLine' :: [String] -> (Int, String) -> String
evolveLine' state (i, row) = map (evolveChar' state (i, row)) $ zip [0..] row

evolveChar' :: [String] -> (Int, String) -> (Int, Char) -> Char
evolveChar' state (i, row) (j, me)
    | me == '.' = '.'
    | otherwise = let c = numNeighbs state i j
          in if c == 0 then '#' else (if c >= 5 then 'L' else me)

numNeighbs :: [String] -> Int -> Int -> Int
numNeighbs state i j = sum $ map (\n -> if n == '#' then 1 else 0) [scanForSeat state (i + deli, j + delj) (deli, delj) | (deli, delj) <- [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]]

scanForSeat :: [String] -> (Int, Int) -> (Int, Int) -> Char
scanForSeat state (i, j) (deli, delj)
    | i < 0 || j < 0 || (i >= length state) || (j >= length (state !! 0)) = '.'
    | otherwise = let here = (state!!i)!!j
          in if here == '.' then (scanForSeat state (i + deli, j + delj) (deli, delj)) else here

count2 :: Char -> [String] -> Int
count2 needle (hay:haystack) = (count needle hay) + (count2 needle haystack)
count2 _ _ = 0

count :: Char -> String -> Int
count needle (hay:haystack) = (if hay == needle then 1 else 0) + (count needle haystack)
count _ _ = 0

stabilize :: [String] -> [String]
stabilize state = firsteq (evolutions state)

main = interact (\input -> (show $ count2 '#' $ stabilize (lines input)) ++ "\n")
