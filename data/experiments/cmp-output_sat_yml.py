import yaml

def extract_benchmarks_with_different_sat(file_a, file_b):
    # 读取 A.yml 和 B.yml 文件
    with open(file_a, 'r') as f_a:
        data_a = yaml.safe_load(f_a)

    with open(file_b, 'r') as f_b:
        data_b = yaml.safe_load(f_b)

    benchmarks = []

    # 在 A.yml 中找出 sat: unknown，同时在 B.yml 中找出 sat: sat 的 benchmark
    for result_a in data_a['results']:
        for result_b in data_b['results']:
            if (result_a['benchmark'] == result_b['benchmark'] and
                result_a['sat'] == 'unknown' and
                result_b['sat'] == 'sat'):
                benchmarks.append(result_b)

    return benchmarks

def save_to_yaml(benchmarks, filename):
    data = {'misc': {'backend': 'Docker'},
            'results': benchmarks}

    # 写入到 C.yml 文件
    with open(filename, 'w') as f:
        yaml.dump(data, f)

# 调用函数提取 benchmark
benchmarks = extract_benchmarks_with_different_sat('/home/aaa/PlatQSF/data/experiments/runs/smtlib_qf_fp_600/optsat/0/output_with_sat.yml', '/home/aaa/PlatQSF/data/experiments/runs/smtlib_qf_fp_600/gosat/0/output_with_sat.yml')

# 保存提取出来的 benchmark 到 C.yml 文件
save_to_yaml(benchmarks, 'qf_fp-optsat-gosat_600.yml')
