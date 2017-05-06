#USAGE: ./configure-wifi-rpi.sh [path to raspbian image] [wifi SSID] [wifi password]


CURRENT=`pwd`
FILENAME=$1

WHERE=/tmp/$(basename $FILENAME)
mkdir $WHERE

STARTSECTOR=$(file $FILENAME |awk 'BEGIN {RS="startsector"} NR >1 {print $0*512}' | tr ' ' "\n" | head -n 1)

echo "mounting image: $FILENAME ..."
sudo mount -o loop,offset=$STARTSECTOR $FILENAME $WHERE

cd $WHERE


echo "enabling i2c ..."
sed -i '/^#.*i2c.*/s/^#//' config.txt
cat config.txt
echo "enabled i2c"

cd $CURRENT

echo "unmounting image: $FILENAME ..."
sudo umount $WHERE

rmdir $WHERE