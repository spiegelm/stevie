#!/bin/bash

#ID=9156
for ID in 13594
do

Z=8
WIDTH=350
HEIGHT=525

X0=0
X0_start=0
let X0_delta=40 #64
let X0_max=320+10

Y0=0
Y0_delta=40 #90 #128
let Y0_max=480+10

URL_PREFIX="http://example.com/"
FILENAME="nope.jpg"
HTML="tiles_$ID.html"

date

echo '<html><head><link rel="stylesheet" href="style_portrait.css"></head><body><table>' > $HTML

while [ $Y0 -lt $Y0_max ]; do
    let X0=X0_start

    echo '<tr>' >> $HTML

	while [ $X0 -lt $X0_max ]; do
        URL="$URL_PREFIX?id=$ID&x1=0&x0=$X0&y1=0&y0=$Y0&z=$Z&width=$WIDTH&height=$HEIGHT"
        FILENAME="down/$Y0$X0.jpg"

        echo $URL
        curl -s $URL > $FILENAME

        echo "<td><img src='$FILENAME'/></td>" >> $HTML
        
		let X0=X0+X0_delta
	done

    echo '</tr>' >> $HTML
    
	let Y0=Y0+Y0_delta
done

date

done

