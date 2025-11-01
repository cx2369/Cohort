#!/bin/bash

# 获取所有tmux会话的列表
sessions=$(tmux list-sessions -F "#S")

# 遍历所有会话，并detach每个会话
for session in $sessions; do
    tmux detach -s $session
done
