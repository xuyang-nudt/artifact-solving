import yaml
import os
import shutil

# =========================
# 文件路径
# =========================
A_FILE = "/home/aaa/artifact-solving/data/experiments/runs/smtlib_qf_fp/optsat_soea/0/output_with_sat.yml"
B_FILE = "/home/aaa/artifact-solving/data/experiments/runs/smtlib_qf_fp/optsat_nsga2/0/output_with_sat.yml"
OUTPUT_DIR = "/home/aaa/artifact-solving/data/newfile/"

# benchmark 的根目录
BENCHMARK_ROOT = "/home/aaa/artifact-solving/data/benchmarks/smtlib_qf_fp"


def load_results(filename):
    with open(filename, "r") as f:
        data = yaml.safe_load(f)

    return {
        item["benchmark"]: item.get("sat")
        for item in data.get("results", [])
    }


# =========================
# 读取 A、B
# =========================
a_results = load_results(A_FILE)
b_results = load_results(B_FILE)


# =========================
# 筛选并复制
# =========================
copied = 0
removed = 0
missing = 0

TARGET_DIR = "imperial_svcomp_float-benchs_svcomp_mea8000.x86_64"

for benchmark, a_sat in a_results.items():

    # benchmark 路径中某一级目录是否为 TARGET_DIR
    parts = benchmark.split("/")

    if TARGET_DIR not in parts:
        continue

    # 只处理 .smt2
    if not benchmark.endswith(".smt2"):
        continue

    b_sat = b_results.get(benchmark)

    # 删除：
    # A = sat，但是 B != sat
    if a_sat == "sat" and b_sat != "sat":
        removed += 1
        continue

    # 原始 benchmark 文件
    src = os.path.join(BENCHMARK_ROOT, benchmark)

    # 新目录中的目标文件
    dst = os.path.join(OUTPUT_DIR, benchmark)

    if not os.path.isfile(src):
        print(f"[MISSING] {src}")
        missing += 1
        continue

    # 创建目标目录
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    # 拷贝文件
    shutil.copy2(src, dst)

    copied += 1


print("=========================")
print(f"A benchmarks : {len(a_results)}")
print(f"Removed      : {removed}")
print(f"Missing      : {missing}")
print(f"Copied       : {copied}")
print(f"Output       : {OUTPUT_DIR}")
print("=========================")