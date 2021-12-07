solvea :: String -> String
solvea s = show $ sum $ map (\c -> if c == '(' then 1 else (-1)) s

main = interact solvea