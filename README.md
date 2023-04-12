# led-display

<p>This is python script to control a single 32x64 LED display</p>
<p>The original plan was an art project for a friend to scroll some favorite quotes.<p>
<p>Currently there are many more functions added to the display:</p>
<ul>
 <li>Time/Day</li>
 <li>Song Lyrics/Poetry</li>
 <li>Crypto Prices</li>
 <li>/r/news Headlines</li>
 <li>gif/image/movie Player</li>
 <li>A moving image of /r/place</li>
 <li>Included Demo's from the hzeller/rpi-rgb-led-matrix git, the repo these scripts utilize. (Game of life, Equalizer, Snake like art)</li>
</ul>
<p>There are also opportunities for interactive games and creations.</p>
<p>Parts List:</p>
<ul>
<li>LED Panel</li>
<li>Raspberry pi zero w</li>
<li>GPIO pi hat</li>
<li>Power adaptor</li>
</ul>

<p>The unit is self contained. Once you plug it in, you can access a hotspot. That will allow you to select a permanent wifi access point for an internet connection.</p>
<p>From a computer or mobile device you can access the webpage to add or remove any media.</p>
<p>Basic Setup:</p>
<ol>
<li>Clone hzeller repo</li>
<li>Clone this repo into the same directory</li>
<li>Install flask</li>
<li>Install supervisor</li>
<li>Create supervisor configuration files</li>
<li>Add media either directly to folders in "install-dir"/static, or using the webpage.</li>
</ol>
<p>I hope you find this useful!</p>
