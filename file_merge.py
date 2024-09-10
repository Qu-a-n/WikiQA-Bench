import pandas as pd
import os
from bench import write_list_to_tsv # input: [<[idx, answer]>]  -> .tsv

# 指定文件夹路径
folder_path = 'log/train'
# 指定输出文件路径1
start, end = 0 ,1000
output_file = f'log/merge/merged_{start}_{end}.tsv'

# 创建一个空的 DataFrame
merged_df = pd.DataFrame()
idx, ans = [], []

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.tsv'):  # 检查文件扩展名
        file_path = os.path.join(folder_path, filename)  # 构造完整文件路径
        with open(file_path, "r", encoding='utf8') as fp:
            for line in fp:
                line_split = line.rstrip("\n").split("\t")
                idx.append(line_split[0])
                ans.append(line_split[1])

res = [
    [idx[i], ans[i]] for i in range(len(idx))
]
        
write_list_to_tsv(output_file, res)
# 将合并后的 DataFrame 保存为 TSV 文件

# merged_df.to_csv(output_file, sep='\t', index=False)

# print(f"所有 TSV 文件已合并为 {output_file}")
