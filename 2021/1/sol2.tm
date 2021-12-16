; a solution to https://adventofcode.com/2021/day/1 part 2
; designed to run on my personal tm simulator (source here: https://github.com/spencerteiknsmith/tm-simulator)
; or on http://morphett.info/turing/ (I modelled mine after that site, so they accept the same input format)
; the language spec is well described on Morphett's site.
; the web version is great for debugging, but I had to build my own to actually run AoC at speed
;
; the tm simulator does not work well with whitespace characters
; so the input is changed to have replacement characters:
; replace newlines with `/` and spaces with `~`: 
; `$ tr "\n " "/~" < web_input.txt > tm_input.txt`

; I used a fair few abbreviations to keep state names short.
; some of the possibly less-obvious abbreviations I used are:
;
; cmp=compare
; dec=decrement/decrease
; inc=increment/increase
; refl=reflect
;
; if a group of letters do not spell a word or abbreviation,
; then the letters individually probably mean the following:
;
; l=left
; r=right
; d=digit
; c=count(er)
;
; letters standing alone are necessarily so -- they can be:
;
; direction commands (l/r)
; English words (I/a)
; tape characters (explained below)
;
; tape alphabet
; =============
; 0123456789 ; digits (for input and final counting)
; QWERTYUIOP ; marked digits (while processing input)
; /~         ; newline/space (newlines are in input, space is used as 'eraser' (separate from blank cells))
; ><=        ; decrease/increase/equality unary counters
; ^#         ; tape dividers/end markers
; asd        ; marked newlines (used between #s currently being compared)

; everything after a `;` is a comment as far as the simulators see it.
; the braces and indentation are merely for convenience in reading
; and getting VSCode to let me collapse blocks

; setup initial marks {
    ; mark beginning, also marking the first 'comparison' as a decrease.
    ; this smooths later operations by making the first comparison look
    ; just like the rest.
    0 * * l mark_init_>
    mark_init_> _ > l mark_head
    mark_head _ ^ r setup_find_end

    ; and making sure there is a terminal /
    setup_find_end _ * l check_/end
    setup_find_end * * r setup_find_end
    check_/end / * l setup_return_home
    check_/end * * r setup_add_/end
    setup_add_/end _ / l setup_return_home

    ; and return to the beginning
    setup_return_home > * r start_new_compare
    setup_return_home * * l setup_return_home
;}


; scan and set </> for each pair {
    ; mark the newlines between left val and right val {
        start_new_compare * * r find_\n_0
        find_\n_0 / a r find_\n_1
        find_\n_0 * * r find_\n_0
        find_\n_1 / s r find_\n_2
        find_\n_1 * * r find_\n_1
        find_\n_2 / d l return_to_l_val
        find_\n_2 * * r find_\n_2
        return_to_l_val < * r ldc0
        return_to_l_val > * r ldc0
        return_to_l_val = * r ldc0
        return_to_l_val * * l return_to_l_val
    ;}
    ; count # digits in left val {
        ; there are no zero-length numbers
        ldc0 * * r ldc1

        ldc1 a * r ld1pass
        ldc1 * * r ldc2

        ldc2 a * r ld2pass
        ldc2 * * r ldc3

        ldc3 a * r ld3pass
        ldc3 * * r ldc4

        ldc4 a * r ld4pass
        ; only need to support 4-digit numbers for my input
        ; this will crash on larger
    ;}

    ; pass over to right num {
        ld1pass d * r ld1rdc0
        ld1pass * * r ld1pass
        
        ld2pass d * r ld2rdc0
        ld2pass * * r ld2pass
        
        ld3pass d * r ld3rdc0
        ld3pass * * r ld3pass
        
        ld4pass d * r ld4rdc0
        ld4pass * * r ld4pass
    ;}

    ; count # digits in right val {
        ld1rdc0 _ * * accumulate
        ld1rdc0 * * r ld1rdc1
        ld2rdc0 _ * * accumulate
        ld2rdc0 * * r ld2rdc1
        ld3rdc0 _ * * accumulate
        ld3rdc0 * * r ld3rdc1
        ld4rdc0 _ * * accumulate
        ld4rdc0 * * r ld4rdc1

        ld1rdc1 / * l rich_cmp
        ld1rdc1 * * l dc_inc
        ld2rdc1 / * l dc_dec
        ld2rdc1 * * r ld2rdc2
        ld3rdc1 / * l dc_dec
        ld3rdc1 * * r ld3rdc2
        ld4rdc1 / * l dc_dec
        ld4rdc1 * * r ld4rdc2

        ld2rdc2 / * l rich_cmp
        ld2rdc2 * * l dc_inc
        ld3rdc2 / * l dc_dec
        ld3rdc2 * * r ld3rdc3
        ld4rdc2 / * l dc_dec
        ld4rdc2 * * r ld4rdc3

        ld3rdc3 / * l rich_cmp
        ld3rdc3 * * l dc_inc
        ld4rdc3 / * l dc_dec
        ld4rdc3 * * r ld4rdc4

        ld4rdc4 / * l rich_cmp
        ; only up to 4 digits ..
    ;}

    ; if digit count differed, mark >/< immediately {
        dc_inc d / l dc_inc
        dc_inc s / l dc_inc
        dc_inc a < r start_new_compare
        dc_inc * * l dc_inc

        dc_dec d / l dc_dec
        dc_dec s / l dc_dec
        dc_dec a > r start_new_compare
        dc_dec * * l dc_dec
    ;}

    ; otherwise, we need rich comparison {
        ; setup by going to left edge of right value
        rich_cmp d * r find_rd
        rich_cmp * * l rich_cmp

        ; find first unmarked digit in right {
            find_rd / * l unmark_marks
            find_rd 0 P l rd0find_ld
            find_rd 1 Q l rd1find_ld
            find_rd 2 W l rd2find_ld
            find_rd 3 E l rd3find_ld
            find_rd 4 R l rd4find_ld
            find_rd 5 T l rd5find_ld
            find_rd 6 Y l rd6find_ld
            find_rd 7 U l rd7find_ld
            find_rd 8 I l rd8find_ld
            find_rd 9 O l rd9find_ld
            find_rd * * r find_rd
        ;}

        ; find first unerased digit in left {
            rd0find_ld > * r rd0cmp
            rd0find_ld < * r rd0cmp
            rd0find_ld = * r rd0cmp
            rd0find_ld ~ * r rd0cmp
            rd0find_ld * * l rd0find_ld

            rd1find_ld > * r rd1cmp
            rd1find_ld < * r rd1cmp
            rd1find_ld = * r rd1cmp
            rd1find_ld ~ * r rd1cmp
            rd1find_ld * * l rd1find_ld

            rd2find_ld > * r rd2cmp
            rd2find_ld < * r rd2cmp
            rd2find_ld = * r rd2cmp
            rd2find_ld ~ * r rd2cmp
            rd2find_ld * * l rd2find_ld

            rd3find_ld > * r rd3cmp
            rd3find_ld < * r rd3cmp
            rd3find_ld = * r rd3cmp
            rd3find_ld ~ * r rd3cmp
            rd3find_ld * * l rd3find_ld

            rd4find_ld > * r rd4cmp
            rd4find_ld < * r rd4cmp
            rd4find_ld = * r rd4cmp
            rd4find_ld ~ * r rd4cmp
            rd4find_ld * * l rd4find_ld

            rd5find_ld > * r rd5cmp
            rd5find_ld < * r rd5cmp
            rd5find_ld = * r rd5cmp
            rd5find_ld ~ * r rd5cmp
            rd5find_ld * * l rd5find_ld

            rd6find_ld > * r rd6cmp
            rd6find_ld < * r rd6cmp
            rd6find_ld = * r rd6cmp
            rd6find_ld ~ * r rd6cmp
            rd6find_ld * * l rd6find_ld

            rd7find_ld > * r rd7cmp
            rd7find_ld < * r rd7cmp
            rd7find_ld = * r rd7cmp
            rd7find_ld ~ * r rd7cmp
            rd7find_ld * * l rd7find_ld

            rd8find_ld > * r rd8cmp
            rd8find_ld < * r rd8cmp
            rd8find_ld = * r rd8cmp
            rd8find_ld ~ * r rd8cmp
            rd8find_ld * * l rd8find_ld

            rd9find_ld > * r rd9cmp
            rd9find_ld < * r rd9cmp
            rd9find_ld = * r rd9cmp
            rd9find_ld ~ * r rd9cmp
            rd9find_ld * * l rd9find_ld        
        ;}

        ; perform the comparison {
            rd0cmp 0 ~ r find_r_val_for_new_digit
            rd0cmp * ~ r mark_dec

            rd1cmp 0 ~ r mark_inc
            rd1cmp 1 ~ r find_r_val_for_new_digit
            rd1cmp * ~ r mark_dec

            rd2cmp 0 ~ r mark_inc
            rd2cmp 1 ~ r mark_inc
            rd2cmp 2 ~ r find_r_val_for_new_digit
            rd2cmp * ~ r mark_dec

            rd3cmp 0 ~ r mark_inc
            rd3cmp 1 ~ r mark_inc
            rd3cmp 2 ~ r mark_inc
            rd3cmp 3 ~ r find_r_val_for_new_digit
            rd3cmp * ~ r mark_dec

            rd4cmp 0 ~ r mark_inc
            rd4cmp 1 ~ r mark_inc
            rd4cmp 2 ~ r mark_inc
            rd4cmp 3 ~ r mark_inc
            rd4cmp 4 ~ r find_r_val_for_new_digit
            rd4cmp * ~ r mark_dec

            rd5cmp 9 ~ r mark_dec
            rd5cmp 8 ~ r mark_dec
            rd5cmp 7 ~ r mark_dec
            rd5cmp 6 ~ r mark_dec
            rd5cmp 5 ~ r find_r_val_for_new_digit
            rd5cmp * ~ r mark_inc

            rd6cmp 9 ~ r mark_dec
            rd6cmp 8 ~ r mark_dec
            rd6cmp 7 ~ r mark_dec
            rd6cmp 6 ~ r find_r_val_for_new_digit
            rd6cmp * ~ r mark_inc

            rd7cmp 9 ~ r mark_dec
            rd7cmp 8 ~ r mark_dec
            rd7cmp 7 ~ r find_r_val_for_new_digit
            rd7cmp * ~ r mark_inc

            rd8cmp 9 ~ r mark_dec
            rd8cmp 8 ~ r find_r_val_for_new_digit
            rd8cmp * ~ r mark_inc

            rd9cmp 9 ~ r find_r_val_for_new_digit
            rd9cmp * ~ r mark_inc            
        ;}

        ; if unequal, mark >/< {
            mark_inc a < r find_rd_end
            mark_inc * * r mark_inc
            
            mark_dec a > r find_rd_end
            mark_dec * * r mark_dec

            find_rd_end / * l unmark_marks
            find_rd_end * * r find_rd_end
        ;}

        ; otherwise go back to right val to repeat {
            find_r_val_for_new_digit d * r find_rd
            find_r_val_for_new_digit * * r find_r_val_for_new_digit
        ;}

        ; unmark the temporary marks made for this comparison
        ; (QWE-Pasd) in right num and set for next compare {
            unmark_marks Q 1 l unmark_marks
            unmark_marks W 2 l unmark_marks
            unmark_marks E 3 l unmark_marks
            unmark_marks R 4 l unmark_marks
            unmark_marks T 5 l unmark_marks
            unmark_marks Y 6 l unmark_marks
            unmark_marks U 7 l unmark_marks
            unmark_marks I 8 l unmark_marks
            unmark_marks O 9 l unmark_marks
            unmark_marks P 0 l unmark_marks
            unmark_marks d / l unmark_marks
            unmark_marks s / l unmark_marks
            ; if we see a at this stage it is because >/< was not set
            unmark_marks a = r start_new_compare
            unmark_marks < * r start_new_compare
            unmark_marks > * r start_new_compare
            unmark_marks * * l unmark_marks
        ;}
    ;}
;}

; accumulate `<`s into a readable value {
    accumulate _ # l <c0
    accumulate # * l <c0
    accumulate * * l accumulate

    ; scan left looking for 10 `<`s {
        <c0 < _ l <c1
        <c0 ^ _ r ones_place0
        <c0 # * l <c0
        <c0 * _ l <c0

        <c1 < _ l <c2
        <c1 ^ _ r ones_place1
        <c1 * _ l <c1

        <c2 < _ l <c3
        <c2 ^ _ r ones_place2
        <c2 * _ l <c2

        <c3 < _ l <c4
        <c3 ^ _ r ones_place3
        <c3 * _ l <c3

        <c4 < _ l <c5
        <c4 ^ _ r ones_place4
        <c4 * _ l <c4

        <c5 < _ l <c6
        <c5 ^ _ r ones_place5
        <c5 * _ l <c5

        <c6 < _ l <c7
        <c6 ^ _ r ones_place6
        <c6 * _ l <c6

        <c7 < _ l <c8
        <c7 ^ _ r ones_place7
        <c7 * _ l <c7

        <c8 < _ l <c9
        <c8 ^ _ r ones_place8
        <c8 * _ l <c8

        <c9 < _ r add10
        <c9 ^ _ r ones_place9
        <c9 * _ l <c9
    ;}

    ; add in multiples of 10 w/carry {
        add10 # * r inc1
        add10 * * r add10

        inc1 _ 1 l accumulate
        inc1 0 1 l accumulate
        inc1 1 2 l accumulate
        inc1 2 3 l accumulate
        inc1 3 4 l accumulate
        inc1 4 5 l accumulate
        inc1 5 6 l accumulate
        inc1 6 7 l accumulate
        inc1 7 8 l accumulate
        inc1 8 9 l accumulate
        inc1 9 0 r inc1
    ;}

    ; set one's place {
        ones_place0 # 0 r find_next_digit
        ones_place0 * * r ones_place0

        ones_place1 # 1 r find_next_digit
        ones_place1 * * r ones_place1

        ones_place2 # 2 r find_next_digit
        ones_place2 * * r ones_place2

        ones_place3 # 3 r find_next_digit
        ones_place3 * * r ones_place3

        ones_place4 # 4 r find_next_digit
        ones_place4 * * r ones_place4

        ones_place5 # 5 r find_next_digit
        ones_place5 * * r ones_place5

        ones_place6 # 6 r find_next_digit
        ones_place6 * * r ones_place6

        ones_place7 # 7 r find_next_digit
        ones_place7 * * r ones_place7

        ones_place8 # 8 r find_next_digit
        ones_place8 * * r ones_place8

        ones_place9 # 9 r find_next_digit
        ones_place9 * * r ones_place9
    ;}

    ; reflect the # (it was built backwards) {
        find_next_digit ~ * r find_next_digit
        find_next_digit _ * l cleanup
        find_next_digit 0 ~ l refl0
        find_next_digit 1 ~ l refl1
        find_next_digit 2 ~ l refl2
        find_next_digit 3 ~ l refl3
        find_next_digit 4 ~ l refl4
        find_next_digit 5 ~ l refl5
        find_next_digit 6 ~ l refl6
        find_next_digit 7 ~ l refl7
        find_next_digit 8 ~ l refl8
        find_next_digit 9 ~ l refl9

        refl0 _ 0 r find_gap
        refl0 * * l refl0

        refl1 _ 1 r find_gap
        refl1 * * l refl1

        refl2 _ 2 r find_gap
        refl2 * * l refl2

        refl3 _ 3 r find_gap
        refl3 * * l refl3

        refl4 _ 4 r find_gap
        refl4 * * l refl4

        refl5 _ 5 r find_gap
        refl5 * * l refl5

        refl6 _ 6 r find_gap
        refl6 * * l refl6

        refl7 _ 7 r find_gap
        refl7 * * l refl7

        refl8 _ 8 r find_gap
        refl8 * * l refl8

        refl9 _ 9 r find_gap
        refl9 * * l refl9

        find_gap ~ * r find_next_digit
        find_gap * * r find_gap

        cleanup ~ _ l cleanup
        cleanup * * * halt
    ;}
;}
