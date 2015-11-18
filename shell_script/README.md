
## Git 拉取文件内所有项目

#### 修改 `.zshrz`：
`alias gsync='ls | xargs -P10 -I{} git -C {} pull'`

#### `alias`

#### `xargs`
> usage: xargs [-0opt] [-E eofstr] [-I replstr [-R replacements]] [-J replstr]
             [-L number] [-n number [-x]] [-P maxprocs] [-s size]
             [utility [argument ...]]
             
`-I`: 使用-i参数默认的前面输出用{}代替，-I参数可以指定其他代替字符，如例子中的[] 


#### `git -C`
