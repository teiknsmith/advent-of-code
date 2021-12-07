data BiList a = BiList [a] [a]
instance Show a => Show (BiList a) where
    show (BiList neg pos) = show $ (reverse (take 2 $ tail neg)) ++ (take 3 pos)

at :: BiList a -> Int -> a
at (BiList neg pos) idx = if idx < 0 then neg!!(-idx) else pos!!idx

initBiList :: a -> [a] -> BiList a
initBiList fillel l = BiList ([fillel] ++ (reverse neg) ++ cycle [fillel]) (pos ++ cycle [fillel])
    where (neg, pos) = splitAt ((length l) `div` 2) l

data State = State {cells :: BiList (BiList (BiList Bool)), range :: (Int, Int, Int) } deriving (Show)

evolutions :: State -> [State]
evolutions state = state:(evolutions (evolve state))

evolve :: State -> State
evolve s = s

parseState :: String -> State
parseState input = State {cells = initBiList blank2 [init], range = (1, h, w)}
    where blank2 = initBiList blank1 [blank1]
          blank1 = initBiList False [False]
          (init, h, w) = parse2d input

parse2d :: String -> (BiList (BiList Bool), Int, Int)
parse2d input = (initBiList (initBiList False [False]) $ map parse1d inlines, length inlines, length $ head inlines)
    where inlines = lines input

parse1d :: String -> BiList Bool
parse1d input = initBiList False $ map (=='#') input

confined :: 

numActive :: State -> Int
numActive s = sum(map sum grid)
    where grid = cells s
          (d, h, w) = range s

solveA :: String -> String
solveA = (++ "\n") . show . numActive . (!!5) . evolutions . parseState

main = interact solveA