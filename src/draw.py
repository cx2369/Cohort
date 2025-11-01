# import matplotlib.pyplot as plt
# from matplotlib.patches import Patch

# # 1. 创建图例元素（保持与原图一致）
# legend_elements = [
#     Patch(facecolor='green', edgecolor='black', label='AFL++'),
#     Patch(facecolor='red', edgecolor='black', label='Cmplog'),
#     Patch(facecolor='blue', edgecolor='black', label='Cohort'),
#     Patch(facecolor='orange', edgecolor='black', label='Cohort-c')
# ]

# # 2. 创建空白画布（白色背景）
# fig = plt.figure(figsize=(10, 1), facecolor='white')  # 宽度足够容纳4个图例
# ax = fig.add_subplot(facecolor='white')

# # 3. 添加横向图例（带白色背景框）
# legend = ax.legend(
#     handles=legend_elements,
#     loc='center',
#     ncol=4,  # 横向排列4个图例
#     frameon=True,  # 显示外框
#     framealpha=1,  # 不透明
#     edgecolor='black',  # 边框颜色
#     facecolor='white',  # 背景白色
#     prop={'size': 16}  # 字体大小
# )

# # 4. 隐藏坐标轴
# ax.axis('off')

# # 5. 调整边距并保存
# plt.tight_layout()
# plt.savefig(
#     '/home/cas/chenxu/cxfuzz3/draw/legend_white.png',
#     dpi=300,
#     bbox_inches='tight',
#     facecolor='white'  # 确保保存的背景也是白色
# )
# plt.close()

# import matplotlib.pyplot as plt
# import pandas as pd
# import glob
# import numpy as np

# # Function to read data from a file and return time and edges_found


# def read_data(file_path):
#     data = pd.read_csv(file_path, header=None, skiprows=1)
#     time_seconds = data[0]  # First column is time in seconds
#     edges_found = data[12]   # 13th column is edges_found
#     return time_seconds * 2 / 3600, (edges_found.astype(float))/1000  # Convert seconds to hours


# file_groups = {
#     'AFL++': [f'/home/cas/chenxu/cxfuzz3/expdata/aflpp/aflpp-imginfo-{i}/default/plot_data' for i in range(10)],
#     'Cmplog': [f'/home/cas/chenxu/cxfuzz3/expdata/cmplog/aflpp-cmplog-imginfo-{i}/default/plot_data' for i in range(10)],
#     'Cohort': [f'/home/cas/chenxu/cxfuzz3/expdata/cx/old1/cx-imginfo-{i}/default/plot_data' for i in range(10)],
#     'Cohort-c': [f'/home/cas/chenxu/cxfuzz3/expdata/cx-cmplog/cx-cmplog-imginfo-{i}/default/plot_data' for i in range(10)],
# }

# colors = ['green', 'red', 'blue', 'orange']

# plt.figure(figsize=(8, 6))

# # Read each group and calculate average
# for label, file_paths in file_groups.items():
#     all_edges_found = []
#     all_hours = []

#     # Read each file in the group
#     for file_path in file_paths:
#         try:
#             hours, edges_found = read_data(file_path)
#             all_edges_found.append(edges_found)
#             all_hours.append(hours)
#         except Exception as e:
#             print(f"Error reading {file_path}: {e}")
#             continue

#     # Interpolate to a common set of time points
#     common_hours = np.linspace(0, 24, num=1000)  # Define common time points
#     interpolated_edges = []

#     for edges_found, hours in zip(all_edges_found, all_hours):
#         interp_edges = np.interp(common_hours, hours, edges_found, left=np.nan, right=np.nan)
#         interpolated_edges.append(interp_edges)

#     # Convert to NumPy array and calculate the mean
#     interpolated_edges = np.array(interpolated_edges)
#     mean_edges_found = np.nanmean(interpolated_edges, axis=0)  # Calculate mean ignoring NaNs

#     # Plot the average result
#     plt.plot(common_hours, mean_edges_found, label=label, color=colors.pop(0),linewidth=2.5)  # Use a color for each group

# # Configure the plot
# plt.subplots_adjust(
#     left=0.15,    # 左边距从默认0.125减小
#     right=0.95,   # 右边距从默认0.9增大
#     bottom=0.15,  # 底边距从默认0.1增大
#     top=0.9      # 顶边距从默认0.9增大
# )
# plt.tick_params(axis='both', which='major', 
#                length=8, width=2,labelsize=22)  
# # plt.title('Coverage')
# plt.xlabel('Time (Hours)', fontsize=22)
# plt.ylabel('Edges Found(K)', fontsize=22)
# plt.xlim(0, 24)
# plt.ylim(0, max(edges_found) * 1.2)  # Adjust y-axis limit
# plt.xticks(range(0, 25, 4))  # Set x-ticks from 0 to 24
# plt.legend()
# # plt.grid()

# # Save the plot instead of showing it
# plt.savefig('/home/cas/chenxu/cxfuzz3/draw/plot_data.png')  # Save as PNG file
# plt.close()  # Close the plot
