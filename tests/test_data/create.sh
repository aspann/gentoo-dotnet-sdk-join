#!/bin/bash

## FOR TESTINGS ONLY!
# this script is meant to create the .../test_data dirs..
# DO NOT CHANGE ANY OF THE CHECKS! (be warned)

## checking caller. (ln is fine, rename isn't)
tbdir=$(realpath $(dirname ${0})/..)/test_data
[ $(realpath $0) != ${tbdir}/create.sh ] && exit 1

### main script (respect the above!)
echo "running test dir creation script..."

## INFO
echo test-dir: ${tbdir}

## SDK's to create
sdks="2.0,3.1,5.0,6.0,7.0,8.0"

# cleanup old data (if any)
[ -d ${tbdir}/opt ] && rm -rf ${tbdir}/opt

## iterate through SDK's
for sdk in ${sdks//,/ }; do
    echo "creating test-structure for SDK: ${sdk}.."

    mkdir -p ${tbdir}/opt/dotnet-sdk-bin-${sdk}/sdk/${sdk}.100
    touch ${tbdir}/opt/dotnet-sdk-bin-${sdk}/sdk/${sdk}.100/.keep

    mkdir -p ${tbdir}/opt/dotnet-sdk-bin-${sdk}/shared/Microsoft.AspNetCore.App/${sdk}.100
    touch ${tbdir}/opt/dotnet-sdk-bin-${sdk}/shared/Microsoft.AspNetCore.App/${sdk}.100/.keep

    mkdir -p ${tbdir}/opt/dotnet-sdk-bin-${sdk}/shared/Microsoft.NETCore.App/${sdk}.100
    touch ${tbdir}/opt/dotnet-sdk-bin-${sdk}/shared/Microsoft.NETCore.App/${sdk}.100/.keep
done
