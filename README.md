# unity_metadata_loader

This project will load strings and method/class names in global-metadata.dat to IDA.

detail: https://github.com/nevermoe/unity_metadata_loader

## how to build unity_decoder.exe

    $ git clone https://github.com/kenjiaiko/unity_metadata_loader/
    $ cd unity_metadata_loader/unity_decoder
    $ mv libil2cpp_v23 libil2cpp

Rename libil2cpp_vXX to libil2cpp. Open "unity_decoder.sln" using Visual Studio 2017.

## how to load strings and method/class from global-metadata.dat

sample apk: https://1drv.ms/u/s!ApYX-BnkUapSgn_fj9o7JsJGz7YU

    $ mkdir tmp
    $ cp test.apk/assets\bin\Data\Managed\Metadata\global-metadata.dat tmp\
    $ cp test.apk\lib\armeabi-v7a\libil2cpp.so tmp\
    $ cp unity_metadata_loader/Release/unity_decoder.exe tmp\
    $ cp unity_metadata_loader/unity_loader_v23.py tmp\
    $ cd tmp
    $ ./unity_decoder.exe

Copy global-metadata.dat, unity_decoder.exe, unity_loader_vXX.py and libil2cpp.so to the same folder(like lib\armeabi-v7a), then execute unity_decoder.exe. The exe file will make 2 files which name are "method_name.txt" and "string_literal.txt". 
