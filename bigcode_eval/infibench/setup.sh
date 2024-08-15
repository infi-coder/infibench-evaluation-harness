# setting up javascript and typescript env
sudo apt-get install -y nodejs npm
mkdir ~/.npm-global
npm config set prefix `~/.npm-global`
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
source ~/.profile
npm i jsdom@17.0.0 -g
npm install typescript -g
export NODE_PATH=$(npm root --quiet -g)
# setup c++ env:
sudo apt-get install -y libboost-all-dev
# setup c# env:
sudo apt-get install -y mono-complete
# setup go env:
sudo apt-get install -y golang-go
# setup java env:
sudo apt-get install -y default-jdk
# setup r env:
apt-get install -y r-base
apt-get install -y r-base-dev
apt-get install -y libssl-dev
apt-get install -y libfontconfig1-dev
apt-get install -y libcurl4-openssl-dev
apt-get install -y libxml2-dev
apt-get install -y libharfbuzz-dev
apt-get install -y libfribidi-dev
apt-get install -y libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev
Rscript -e 'install.packages("assert")'
Rscript -e 'install.packages("stringr")'
Rscript -e 'install.packages("tidyverse")'
Rscript -e 'install.packages("dplyr")'
Rscript -e 'install.packages("data.table")'
