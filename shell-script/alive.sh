for i in {1..254}
do
  ping -c 1 192.168.0.$i &>/dev/null && echo 192.168.0.$i is alive &
done
