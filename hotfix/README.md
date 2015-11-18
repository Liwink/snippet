## 手动部署正式环境 OpenPlay 

1. 新建分支 hotfix，完成修改
    - commit 时的信息
2. 合并分支到 master
    - 这里只对线上环境修改，没有先合并到 develop
    - `--no-ff`
3. 打包分支 `gtar`
        
        alias groot='git rev-parse --show-toplevel'
        alias gcd='cd $(groot)'
        alias gtall='echo $(basename $(groot)).tar.gz'
        alias gtar='$(groot) && git archive --format=tar HEAD | gzip > $(gtall)'
        alias gscp='$(groot) && git archive --format=tar HEAD | gzip > $(gtall) && scp $(gtall)'

4. 上传服务器
    - scp openplay_backend.tar.gz openplay-prod-001:
5. 在项目目录解压
    - tar -vzx
6. 重启项目
    - supervisord -c /config/../.conf
    - restart openplay_player:



