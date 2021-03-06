#!/usr/bin/env python
# coding=utf-8

import paramiko

# 创建SSH对象
ssh = paramiko.SSHClient()

# 允许连接不在know_hosts文件中的主机 第一次登录的认证信息
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接服务器
ssh.connect(hostname='192.168.158.131', port=22, username='root', password='hadoop')

# 执行命令
stdin, stdout, stderr = ssh.exec_command('ls /')

# 获取命令结果
res, err = stdout.read(), stderr.read()

result = res if res else err

print(result.decode())
# 关闭连接
ssh.close()
