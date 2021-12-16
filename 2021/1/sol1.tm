; alphabet
; ========
; 0123456789 ; digits
; QWERTYUIOP ; marked digits
; /~         ; whitespace
; ><=        ; decrease/increase/equality markers
; ^#         ; tape dividers/markers

; setup initial marks {
    ; mark beginning, including the first "transition" as a decrease
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
    setup_return_home > * r ldc0
    setup_return_home * * l setup_return_home
;}


; scan and set </> for each pair {
    ; count # digits in left val {
        ; crash on zero-length numbers
        ldc0 * * r ldc1

        ldc1 / * r ld1rdc0
        ldc1 * * r ldc2

        ldc2 / * r ld2rdc0
        ldc2 * * r ldc3

        ldc3 / * r ld3rdc0
        ldc3 * * r ldc4

        ldc4 / * r ld4rdc0
        ; only need to support 4-digit numbers for my input, crash on larger
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
        dc_inc / < r ldc0
        dc_inc * * l dc_inc

        dc_dec / > r ldc0
        dc_dec * * l dc_dec
    ;}

    ; otherwise, we need rich comparison {
        ; setup by going to middle
        rich_cmp / * r find_rd
        rich_cmp * * l rich_cmp

        ; find first unmarked digit in right ;{
            find_rd / * l unmark_rds ; mid will be / (not <>) in this case, can mark as eq
            find_rd 0 P l rd0find_mid
            find_rd 1 Q l rd1find_mid
            find_rd 2 W l rd2find_mid
            find_rd 3 E l rd3find_mid
            find_rd 4 R l rd4find_mid
            find_rd 5 T l rd5find_mid
            find_rd 6 Y l rd6find_mid
            find_rd 7 U l rd7find_mid
            find_rd 8 I l rd8find_mid
            find_rd 9 O l rd9find_mid
            find_rd * * r find_rd
        ;}

        ; walk back left then find same in left {
            rd0find_mid / * l rd0find_ld
            rd0find_mid * * l rd0find_mid
            rd0find_ld > * r rd0cmp
            rd0find_ld < * r rd0cmp
            rd0find_ld ~ * r rd0cmp
            rd0find_ld * * l rd0find_ld

            rd1find_mid / * l rd1find_ld
            rd1find_mid * * l rd1find_mid
            rd1find_ld > * r rd1cmp
            rd1find_ld < * r rd1cmp
            rd1find_ld ~ * r rd1cmp
            rd1find_ld * * l rd1find_ld

            rd2find_mid / * l rd2find_ld
            rd2find_mid * * l rd2find_mid
            rd2find_ld > * r rd2cmp
            rd2find_ld < * r rd2cmp
            rd2find_ld ~ * r rd2cmp
            rd2find_ld * * l rd2find_ld

            rd3find_mid / * l rd3find_ld
            rd3find_mid * * l rd3find_mid
            rd3find_ld > * r rd3cmp
            rd3find_ld < * r rd3cmp
            rd3find_ld ~ * r rd3cmp
            rd3find_ld * * l rd3find_ld

            rd4find_mid / * l rd4find_ld
            rd4find_mid * * l rd4find_mid
            rd4find_ld > * r rd4cmp
            rd4find_ld < * r rd4cmp
            rd4find_ld ~ * r rd4cmp
            rd4find_ld * * l rd4find_ld

            rd5find_mid / * l rd5find_ld
            rd5find_mid * * l rd5find_mid
            rd5find_ld > * r rd5cmp
            rd5find_ld < * r rd5cmp
            rd5find_ld ~ * r rd5cmp
            rd5find_ld * * l rd5find_ld

            rd6find_mid / * l rd6find_ld
            rd6find_mid * * l rd6find_mid
            rd6find_ld > * r rd6cmp
            rd6find_ld < * r rd6cmp
            rd6find_ld ~ * r rd6cmp
            rd6find_ld * * l rd6find_ld

            rd7find_mid / * l rd7find_ld
            rd7find_mid * * l rd7find_mid
            rd7find_ld > * r rd7cmp
            rd7find_ld < * r rd7cmp
            rd7find_ld ~ * r rd7cmp
            rd7find_ld * * l rd7find_ld

            rd8find_mid / * l rd8find_ld
            rd8find_mid * * l rd8find_mid
            rd8find_ld > * r rd8cmp
            rd8find_ld < * r rd8cmp
            rd8find_ld ~ * r rd8cmp
            rd8find_ld * * l rd8find_ld

            rd9find_mid / * l rd9find_ld
            rd9find_mid * * l rd9find_mid
            rd9find_ld > * r rd9cmp
            rd9find_ld < * r rd9cmp
            rd9find_ld ~ * r rd9cmp
            rd9find_ld * * l rd9find_ld        
        ;}

        ; perform the comparison {
            rd0cmp 0 ~ r find_mid_nd
            rd0cmp * ~ r mark_dec

            rd1cmp 0 ~ r mark_inc
            rd1cmp 1 ~ r find_mid_nd
            rd1cmp * ~ r mark_dec

            rd2cmp 0 ~ r mark_inc
            rd2cmp 1 ~ r mark_inc
            rd2cmp 2 ~ r find_mid_nd
            rd2cmp * ~ r mark_dec

            rd3cmp 0 ~ r mark_inc
            rd3cmp 1 ~ r mark_inc
            rd3cmp 2 ~ r mark_inc
            rd3cmp 3 ~ r find_mid_nd
            rd3cmp * ~ r mark_dec

            rd4cmp 0 ~ r mark_inc
            rd4cmp 1 ~ r mark_inc
            rd4cmp 2 ~ r mark_inc
            rd4cmp 3 ~ r mark_inc
            rd4cmp 4 ~ r find_mid_nd
            rd4cmp * ~ r mark_dec

            rd5cmp 9 ~ r mark_dec
            rd5cmp 8 ~ r mark_dec
            rd5cmp 7 ~ r mark_dec
            rd5cmp 6 ~ r mark_dec
            rd5cmp 5 ~ r find_mid_nd
            rd5cmp * ~ r mark_inc

            rd6cmp 9 ~ r mark_dec
            rd6cmp 8 ~ r mark_dec
            rd6cmp 7 ~ r mark_dec
            rd6cmp 6 ~ r find_mid_nd
            rd6cmp * ~ r mark_inc

            rd7cmp 9 ~ r mark_dec
            rd7cmp 8 ~ r mark_dec
            rd7cmp 7 ~ r find_mid_nd
            rd7cmp * ~ r mark_inc

            rd8cmp 9 ~ r mark_dec
            rd8cmp 8 ~ r find_mid_nd
            rd8cmp * ~ r mark_inc

            rd9cmp 9 ~ r find_mid_nd
            rd9cmp * ~ r mark_inc            
        ;}

        ; if unequal, mark >/< immediately {
            mark_inc / < r find_rd_end
            mark_inc * * r mark_inc
            
            mark_dec / > r find_rd_end
            mark_dec * * r mark_dec

            find_rd_end / * l unmark_rds
            find_rd_end * * r find_rd_end
        ;}

        ; otherwise go back to middle to repeat {
            find_mid_nd / * r find_rd
            find_mid_nd * * r find_mid_nd
        ;}

        ; unmark digits in right num and set for next compare {
            unmark_rds Q 1 l unmark_rds
            unmark_rds W 2 l unmark_rds
            unmark_rds E 3 l unmark_rds
            unmark_rds R 4 l unmark_rds
            unmark_rds T 5 l unmark_rds
            unmark_rds Y 6 l unmark_rds
            unmark_rds U 7 l unmark_rds
            unmark_rds I 8 l unmark_rds
            unmark_rds O 9 l unmark_rds
            unmark_rds P 0 l unmark_rds
            unmark_rds / = r ldc0
            unmark_rds < * r ldc0
            unmark_rds > * r ldc0
            unmark_rds * * l unmark_rds
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
        ones_place0 # 0 r nextdig
        ones_place0 * * r ones_place0

        ones_place1 # 1 r nextdig
        ones_place1 * * r ones_place1

        ones_place2 # 2 r nextdig
        ones_place2 * * r ones_place2

        ones_place3 # 3 r nextdig
        ones_place3 * * r ones_place3

        ones_place4 # 4 r nextdig
        ones_place4 * * r ones_place4

        ones_place5 # 5 r nextdig
        ones_place5 * * r ones_place5

        ones_place6 # 6 r nextdig
        ones_place6 * * r ones_place6

        ones_place7 # 7 r nextdig
        ones_place7 * * r ones_place7

        ones_place8 # 8 r nextdig
        ones_place8 * * r ones_place8

        ones_place9 # 9 r nextdig
        ones_place9 * * r ones_place9
    ;}

    ; reflect the # (it was build backwards) {
        nextdig ~ * r nextdig
        nextdig _ * l cleanup
        nextdig 0 ~ l refl0
        nextdig 1 ~ l refl1
        nextdig 2 ~ l refl2
        nextdig 3 ~ l refl3
        nextdig 4 ~ l refl4
        nextdig 5 ~ l refl5
        nextdig 6 ~ l refl6
        nextdig 7 ~ l refl7
        nextdig 8 ~ l refl8
        nextdig 9 ~ l refl9

        refl0 _ 0 r findmid
        refl0 * * l refl0

        refl1 _ 1 r findmid
        refl1 * * l refl1

        refl2 _ 2 r findmid
        refl2 * * l refl2

        refl3 _ 3 r findmid
        refl3 * * l refl3

        refl4 _ 4 r findmid
        refl4 * * l refl4

        refl5 _ 5 r findmid
        refl5 * * l refl5

        refl6 _ 6 r findmid
        refl6 * * l refl6

        refl7 _ 7 r findmid
        refl7 * * l refl7

        refl8 _ 8 r findmid
        refl8 * * l refl8

        refl9 _ 9 r findmid
        refl9 * * l refl9

        findmid ~ * r nextdig
        findmid * * r findmid

        cleanup ~ _ l cleanup
        cleanup * * * halt
    ;}
;}
