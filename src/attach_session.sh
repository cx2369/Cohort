#!/bin/bash

# 获取所有tmux会话的列表
sessions=$(tmux list-sessions -F "#S")

# 对会话列表进行数值排序
sorted_sessions=($(echo "${sessions[@]}" | tr ' ' '\n' | sort -n))

# 获取要附加的会话起始和结束数字
start_session=${1:-0}  # 默认起始为0
end_session=${2:-${#sorted_sessions[@]}-1}  # 默认结束为会话总数减1

# 确保起始和结束数字在合理范围内
if (( start_session < 0 )); then
    start_session=0
fi
if (( end_session >= ${#sorted_sessions[@]} )); then
    end_session=${#sorted_sessions[@]}-1
fi

# 遍历指定范围内的会话，并在当前终端的不同标签页中打开tmux会话
for (( i=start_session; i<=end_session; i++ )); do
    session=${sorted_sessions[i]}
    gnome-terminal --tab -- tmux attach -t "$session"
    sleep 0.2
done
