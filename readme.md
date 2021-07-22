# WA errorlog parser
_This script annotates ERRORLOG.TXT crash dumps to make them more readable for troubleshooting. It reads virtual memory layout, maps stack and register values to loaded modules and rebases them._

## Example:

Input file:
```
WA caused an Access Violation (0xc0000005) 
in module WA.exe at 0023:00e5c58a.
Exception parameters: 00000000 076600e0
Version 3.8.1

Error occurred at 7/22/2021 11:46:12.
D:\Program Files (x86)\Steam\steamapps\common\Worms Armageddon\WA.exe [003775F1], run by user.
Operating system:  Windows 8.1 (6.3.9600).
8 processor(s), type 586.
43% memory in use.
0 MBytes physical memory.
0 MBytes physical memory free.
0 MBytes paging file.
0 MBytes paging file free.
0 MBytes user address space.
3808 MBytes user address space free.
Read from location 076600e0 caused an access violation.

Context:
EDI:    0x07610b84  ESI: 0x076600e0  EAX:   0x07660194
EBX:    0x07610b84  ECX: 0x0000002d  EDX:   0x00000000
EIP:    0x00e5c58a  EBP: 0x0138d67c  SegCs: 0x00000023
EFlags: 0x00010202  ESP: 0x0138d674  SegSs: 0x0000002b

Bytes at CS:EIP:
f3 a5 ff 24 95 a4 c6 e5 00 90 8b c7 ba 03 00 00 

Stack:
0x0138d674: 076600e0 0000004c 000000b4 00ca6482 ..f.L........d..
0x0138d684: 07610b84 076600e0 000000b4 000000b4 ..a...f.........
0x0138d694: 00000000 00000005 03870058 0760c318 ........X.....`.
0x0138d6a4: 00000000 000000b4 00ca7511 0138d6c8 .........u....8.
0x0138d6b4: 03870058 000000b4 00ed1bc0 0138d728 X...........(.8.
0x0138d6c4: 000000b4 00ecc4b4 07654630 000001d0 ........0Fe.....
0x0138d6d4: 0000005a 00000000 00000000 000000b4 Z...............
0x0138d6e4: 000000b4 0138d7cc 00e8a838 00000000 ......8.8.......
0x0138d6f4: 6d9d1963 0779752c 00000000 00000000 c..m,uy.........
0x0138d704: 000000b4 000000b4 000000b4 00000000 ................
0x0138d714: 00000000 00ed1bc0 00000000 0779752c ............,uy.
0x0138d724: 00ed1bc0 0138d760 6d9d42b9 00000000 ....`.8..B.m....
0x0138d734: 00000000 000000b4 000000b4 000000b4 ................
0x0138d744: 00000000 00000005 00000000 00000000 ................
0x0138d754: 0000005a 0779740c 00ed1bc0 0138d7dc Z....ty.......8.
0x0138d764: 6d9d199e 0779752c 00ed1bc0 00000000 ...m,uy.........
0x0138d774: 00000000 0000005a 0000005a 000000b4 ....Z...Z.......
```

Output:
```
WA caused an Access Violation (0xc0000005) 
in module WA.exe at 0023:00e5c58a.
Exception parameters: 00000000 076600e0
Version 3.8.1

Error occurred at 7/22/2021 11:46:12.
D:\Program Files (x86)\Steam\steamapps\common\Worms Armageddon\WA.exe [003775F1], run by user.
Operating system:  Windows 8.1 (6.3.9600).
8 processor(s), type 586.
43% memory in use.
0 MBytes physical memory.
0 MBytes physical memory free.
0 MBytes paging file.
0 MBytes paging file free.
0 MBytes user address space.
3808 MBytes user address space free.
Read from location 076600e0 caused an access violation.

Context:
EDI:    0x07610b84  ESI: 0x076600e0  EAX:   0x07660194
EBX:    0x07610b84  ECX: 0x0000002d  EDX:   0x00000000
EIP:    0x00e5c58a [WA.exe 0x005dc58a.text]  EBP: 0x0138d67c  SegCs: 0x00000023
EFlags: 0x00010202  ESP: 0x0138d674  SegSs: 0x0000002b

Bytes at CS:EIP:
f3 a5 ff 24 95 a4 c6 e5 00 90 8b c7 ba 03 00 00 


-----------  -------------------------------------------  --------------------------------------  -------------------------------------------  --------------------------------------  ----------------
0x0138d674:  0x076600e0                                   0x0000004c                              0x000000b4                                   0x00ca6482 [WA.exe 0x00426482.text]     ..f.L........d..
0x0138d684:  0x07610b84                                   0x076600e0                              0x000000b4                                   0x000000b4                              ..a...f.........
0x0138d694:  0x00000000                                   0x00000005                              0x03870058                                   0x0760c318                              ........X.....`.
0x0138d6a4:  0x00000000                                   0x000000b4                              0x00ca7511 [WA.exe 0x00427511.text]          0x0138d6c8                              .........u....8.
0x0138d6b4:  0x03870058                                   0x000000b4                              0x00ed1bc0 [WA.exe 0x00651bc0.rdata]         0x0138d728                              X...........(.8.
0x0138d6c4:  0x000000b4                                   0x00ecc4b4 [WA.exe 0x0064c4b4.rdata]    0x07654630                                   0x000001d0                              ........0Fe.....
0x0138d6d4:  0x0000005a                                   0x00000000                              0x00000000                                   0x000000b4                              Z...............
0x0138d6e4:  0x000000b4                                   0x0138d7cc                              0x00e8a838 [WA.exe 0x0060a838.text]          0x00000000                              ......8.8.......
0x0138d6f4:  0x6d9d1963 [wkSuperFrontend.dll 0x10001963]  0x0779752c                              0x00000000                                   0x00000000                              c..m,uy.........
0x0138d704:  0x000000b4                                   0x000000b4                              0x000000b4                                   0x00000000                              ................
0x0138d714:  0x00000000                                   0x00ed1bc0 [WA.exe 0x00651bc0.rdata]    0x00000000                                   0x0779752c                              ............,uy.
0x0138d724:  0x00ed1bc0 [WA.exe 0x00651bc0.rdata]         0x0138d760                              0x6d9d42b9 [wkSuperFrontend.dll 0x100042b9]  0x00000000                              ....`.8..B.m....
0x0138d734:  0x00000000                                   0x000000b4                              0x000000b4                                   0x000000b4                              ................
0x0138d744:  0x00000000                                   0x00000005                              0x00000000                                   0x00000000                              ................
0x0138d754:  0x0000005a                                   0x0779740c                              0x00ed1bc0 [WA.exe 0x00651bc0.rdata]         0x0138d7dc                              Z....ty.......8.
0x0138d764:  0x6d9d199e [wkSuperFrontend.dll 0x1000199e]  0x0779752c                              0x00ed1bc0 [WA.exe 0x00651bc0.rdata]         0x00000000                              ...m,uy.........
0x0138d774:  0x00000000                                   0x0000005a                              0x0000005a                                   0x000000b4                              ....Z...Z.......
```
