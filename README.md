# wav_speed_change
该工程使用python脚本调用c代码实现wav音频的变速不变调。

1.gcc编译生成动态库speed_change.dll：gcc -o speed_change.dll -shared -fPIC runsonic.c sonic.c sonic.h。

2.使用python代码speedup.py调用speed_change.dll进行变速。
