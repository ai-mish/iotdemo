#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

export DFESP_HOME=/opt/sas/viya/home/SASEventStreamProcessingEngine/6.1
export SASTK=/opt/sas/viya/home/SASFoundation/sasexe
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DFESP_HOME/lib:${SASTK}:$DFESP_HOME/ssl/lib
export TKPATH=$DFESP_HOME/lib/tk.940m3

export PATH=$PATH:$DFESP_HOME/bin
export DFESP_SSLPATH=$DFESP_HOME/ssl/lib
export DFESP_JAVA_TRUSTSTORE=/opt/sas/viya/config/etc/SASSecurityCertificateFramework/cacerts/trustedcerts.jks
export SSLCALISTLOC=/opt/sas/viya/config/etc/SASSecurityCertificateFramework/cacerts/trustedcerts.pem

OBJDET="$SOURCE/objectdetection-server.py"
exec python $OBJDET $@
