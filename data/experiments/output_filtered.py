import yaml
import os
import shutil

# 读取B.yml文件
with open('/home/aaa/PlatQSF/data/benchmarks/program_qf_fp/program_filtered_final.yml',
          'r') as file:
    B_data = yaml.safe_load(file)

# 获取B.yml中的所有benchmark
B_benchmarks = {entry['benchmark'] for entry in B_data['results']}

# 遍历目录，过滤output.yml文件
directory = '/home/aaa/PlatQSF/data/experiments/runs/program_qf_fp_600'

for root, _, files in os.walk(directory):
    for file_name in files:
        if file_name == 'output.yml':
            file_path = os.path.join(root, file_name)
            backup_file_path = file_path + '.bak'

            # 备份output.yml文件
            shutil.copy(file_path, backup_file_path)

            with open(file_path, 'r') as file:
                A_data = yaml.safe_load(file)

            # 在A.yml中过滤掉不在B.yml中的benchmark
            filtered_results = [result for result in A_data['results'] if result['benchmark'] in B_benchmarks]

            # 更新A_data
            A_data['results'] = filtered_results
            A_data['schema_version'] = 0

            # 将更新后的A.yml写入文件
            with open(file_path, 'w') as file:
                yaml.dump(A_data, file, default_flow_style=False)

print("所有output.yml文件已更新并备份")
