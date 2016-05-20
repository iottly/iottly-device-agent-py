#USAGE: ./configure-wifi-rpi.sh [path to raspbian image] [wifi SSID] [wifi password]


CURRENT=`pwd`
FILENAME=$1
SSID=$2
PASSWORD=$3
WHERE=/tmp/$(basename $FILENAME)
mkdir $WHERE

STARTSECTOR=$(file $FILENAME|awk 'BEGIN {RS="startsector"} NR >1 {print $0*512}' | tr ' ' "\n" | awk 'BEGIN {max=$0} NF {max=(max>$0)?max:$0} END {print max}')

echo "mounting image: $FILENAME ..."
sudo mount -o loop,offset=$STARTSECTOR $FILENAME $WHERE

cd $WHERE

echo "modifying wpa_supplicant.conf ..."
sudo bash -c 'cat >> etc/wpa_supplicant/wpa_supplicant.conf' <<- EOM 

network={
    ssid="$SSID"
    psk="$PASSWORD"
}
EOM

echo "NEW wpa_supplicant.conf:"
sudo cat etc/wpa_supplicant/wpa_supplicant.conf


cd $CURRENT

echo "unmounting image: $FILENAME ..."
sudo umount $WHERE

rmdir $WHERE