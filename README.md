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

    $ mv test.apk test.apk.zip
    $ unzip test.apk.zip
    $ cd test.apk
    $ cp assets\bin\Data\Managed\Metadata\global-metadata.dat lib\armeabi-v7a
    $ cp ../unity_metadata_loader/Release/unity_decoder.exe lib\armeabi-v7a
    $ cp ../unity_metadata_loader/unity_loader_v23.py lib\armeabi-v7a
    $ cd lib\armeabi-v7a
    $ ./unity_decoder.exe

Copy global-metadata.dat, unity_decoder.exe and unity_loader_vXX.py to the same folder(lib\armeabi-v7a), then execute unity_decoder.exe. The exe will make 2 files which name are "method_name.txt" and "string_literal.txt".
