read -p "Please input the length: " len
for i in `seq 1 $len`
do
    for j in `seq $i $len`
    do
       echo -n "* "
    done
    echo " "
done
