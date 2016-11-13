RES=stat
printf "" > $RES
for x in 1 2 3 4 5 6
do
    printf "level$x:\n" >> $RES
    #printf "0 $x\n" >> $RES
    FILES=./bookworms/level$x/*
    for f in $FILES
    do
        #printf "%s: " "${f##*/}" >> $RES
        ./main < "$f" >> $RES
    done
    printf "\n" >> $RES
done

