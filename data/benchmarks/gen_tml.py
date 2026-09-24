#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml


class MyDumper(yaml.Dumper):
    pass


def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


MyDumper.add_representer(dict, dict_representer)

# BVFP_sat目录
input_dir = "/data/benchmarks/bvfp_sat"

# 输出文件
output_file = "/data/benchmarks/bvfp_sat/BVFP_sat.yml"


results = []


# 递归查找 smt2 文件
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".smt2"):

            full_path = os.path.join(root, file)

            # 保留相对于BVFP_sat的路径
            benchmark = os.path.relpath(full_path, input_dir)

            results.append({
                "benchmark": benchmark,
                "expected_sat": "sat",
                "is_trivial": False
            })


# 排序
results.sort(key=lambda x: x["benchmark"])


data = {
    "results": results,
    "schema_version": 0
}


# 写yaml
with open(output_file, "w", encoding="utf-8") as f:
    yaml.dump(
        data,
        f,
        Dumper=MyDumper,
        default_flow_style=False,
        allow_unicode=True
    )


print("Generated {} with {} benchmarks".format(
    output_file,
    len(results)
))