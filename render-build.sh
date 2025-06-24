#!/bin/bash
apt-get update && apt-get install -y wget xz-utils curl libfontconfig1
mkdir -p bin
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb
ar x wkhtmltox_0.12.6-1.bionic_amd64.deb
tar -xf data.tar.xz
mv usr/local/bin/wkhtmltopdf bin/wkhtmltopdf
chmod +x bin/wkhtmltopdf
