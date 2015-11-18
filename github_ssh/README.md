

### 创建新的密钥

Github 中一个公钥只能绑定一个账号

    ssh-keygen -t rsa -C "your_email@youremail.com"
    ssh-add ~/.ssh/id_rsa_activehacker



### `~/.ssh/config`

配置ssh，系统有默认的 rsa，这里要做的是对指定的 `host` 用指定的密钥。
会遇见的问题是，`github.com-liuyihe` 这种 host 在git中没有识别。

    host liuyihe.github.com
        HostName github.com
        User git
        IdentityFile ~/.ssh/id_rsa_sponia_backend
        IdentitiesOnly yes


### `repo/.git/config`

配置ssh，之前默认的是 https。
用 ssh host 代替写死的 host

    [remote "origin"]
	    url = ssh://git@liuyihe.github.com/sponialtd/openplay_backend.git


