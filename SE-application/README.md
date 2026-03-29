# Pre install docker environment

We have deployed the experimental environment on docker. Please pre install docker on your host

# Download

Download docker image:

```sh
$ docker pull dockerqsf/fpse:tosem
```

If the image is pulled successfully, please check there is an image named dockerqsf/fpse exists.

```sh
$ docker images
REPOSITORY                    TAG          IMAGE ID       CREATED             SIZE
fpse                          tosem        97e77907a245   10 seconds ago      19.4GB
```


Start to run the container in interactive mode.

```sh
$ docker run -it dockerqsf/fpse:tosem
```

# Obtain experimental results

Our experiments were performed on an Intel(R) Xeon(R) Gold 6458Q 128-core CPU @ 3.10GHz, 512GB of memory and the operating system is Ubuntu 18.04 LTS. 

To obtain the results, a machine with similar CPUs is required. Moreover, our experiments were run in 60 parallel.

## Analyze a program

Navigate to `/home/aaa/analysis`. There are ten experiments in total, which are carried out in `exp-0`, `exp-1`, `exp-2`, `exp-3`, `exp-4`, `exp-5`, `exp-6`, `exp-7`, `exp-8` and `exp-9` respectively.
The process of analyzing the program is shown in `exp-0`.

```sh
$ cd /home/aaa/analysis/exp-0
```

You need to set the parameters to run the script `run_solver.sh`: `./run_solver.sh [work_path] [file_name] [solver_type] [search_type]`, where

- work_path: The path of program file location.
- file_name: The program file name.
- solver_type: The solving modes, e.g. (`jfs`, `jsampler`, `qsf`,`qsampler`). The bold fields are setting parameters.
- search_type: The search modes, e.g. `bfs` and `dfs`.

If you want to obtain experimental results for a single test program, e.g., `instances/gsl_acosh.c`. For example, obtain the experimental results of `qsampler+bfs`.

```sh
$ ./run_solver.sh instances gsl_acosh qsampler bfs
```

After running, log and test cases are generated in the corresponding directory, you can read the log as follow:

```sh
$ cat instances/gsl_acosh\&qsampler\&bfs.runlog 
```

```sh
KLEE: Using Z3 solver backend
KLEE: Replacing function "__isnanf" with "klee_internal_isnanf"
KLEE: Replacing function "__isnan" with "klee_internal_isnan"
KLEE: Replacing function "__isnanl" with "klee_internal_isnanl"
KLEE: Replacing function "__isinff" with "klee_internal_isinff"
KLEE: Replacing function "__isinf" with "klee_internal_isinf"
KLEE: Replacing function "__isinfl" with "klee_internal_isinfl"
KLEE: WARNING ONCE: function "gsl_ieee_set_mode" has inline asm
KLEE: WARNING: QSampler: Z3 solving SAT and evaluate SUCCESS !
KLEE: WARNING: QSampler: Z3 solving SAT and evaluate SUCCESS !
KLEE: WARNING: QSampler: Z3 solving SAT and evaluate SUCCESS !
KLEE: WARNING ONCE: calling external: log1p((FAdd w64 N0:(FSub w64 (ReadLSB w64 0 a)
                        4607182418800017408)
           (FSqrt w64 (FAdd w64 (FMul w64 4611686018427387904 N0) (FMul w64 N0 N0))))) at invhyp.c:39 7
KLEE: WARNING: QSampler: Z3 solving SAT and evaluate SUCCESS !

KLEE: done: total instructions = 84
KLEE: done: completed paths = 5
KLEE: done: partially completed paths = 0
KLEE: done: generated tests = 5
Total exec time: 5.081114e+03 ms
```

We can get the coverage information by running the script:

```sh
$ ./repaly.sh
```

```sh
......# some info
     ====  Replay Ktest ====
===>/home/aaa/analysis/exp-0/instances/instances&gsl_acosh&qsampler&bfs_output/test000001.ktest
CHECK:  KTests have been generated !
===>python_res: invhyp.c
===>gcno: /home/aaa/gsl/sys/.libs/invhyp.gcno
gcno file is exit
KTest : /home/aaa/analysis/exp-0/instances/instances&gsl_acosh&qsampler&bfs_output/test000001.ktest
KLEE-REPLAY: klee_assume(0)!
KLEE-REPLAY: NOTE: Test file: /home/aaa/analysis/exp-0/instances/instances&gsl_acosh&qsampler&bfs_output/test000001.ktest
KLEE-REPLAY: NOTE: Arguments: "./gsl_acosh" 
KLEE-REPLAY: NOTE: Storing KLEE replay files in /tmp/klee-replay-RPgytA
KLEE-REPLAY: NOTE: EXIT STATUS: NORMAL (0 seconds)
KLEE-REPLAY: NOTE: removing /tmp/klee-replay-RPgytA
===>ktest_time_log: /home/aaa/analysis/exp-0/instances/instances&gsl_acosh&qsampler&bfs_output/test000001.time
invhyp.c: No such file or directory
===>cover line res:50.0 , 7
invhyp.c: No such file or directory
===>cover branch res:3
...... # some info

```

Coverage information can be found in `res_all_60-0.txt`. The three columns are the name of benchmark, the code coverage, covered statements, covered branches, and the total execution time, respectively.

```sh
$ cat res_all_60-0.txt
```

```
instances&gsl_acosh&qsf&bfs_output/ , 100.0 , 11, 7, 6
```

## Run in 50 parallel

The machine used in our experiments has 128 cores and 512GB memory. Before running the script, please select the appropriate machine and complete parameter configuration.

The execution time and solving time settings in the `run_solver.sh` script are 3600s and 60s respectively. This is a long execution time, and you can enter the script and modify it to your own needs.

```sh
$ vim run_solver.sh
```

```sh
......
MAX_EXE_TIME=3600
SOLVER_TIME=60
......
```

You can also modify the parallel quantity in the script:

```sh
$ vim multi_process.sh
```

```sh
......
pool = multiprocessing.Pool(processes=50) # parallel of 60
......
```

Then you can use `run.sh` to execute all benchmarks in parallel.

```sh
$ ./run.sh
```

# Generating Figures for the Paper

## Bar Charts (Figure 10)
Go to the `res_bar/` directory, then run:
```
python3 plot_bar.py
```
The files `total_bfs_branch-60.pdf` and `total_dfs_branch-60.pdf` generated under `res_bar/bar-results/` correspond to Figure 10 in the paper.

## Scatter Plots (Figure 14)
Go to the `res_scatter/` directory, then run:
```
python3 plot_scatter.py
```
The files generated under `res_scatter/scatter-results/`:

- bfs_JFS_vs_JFSampler.pdf
- bfs_QSF_vs_QSampler.pdf
- bfs_JFSampler_vs_QSampler.pdf
- dfs_JFS_vs_JFSampler.pdf
- dfs_QSF_vs_QSampler.pdf
- dfs_JFSampler_vs_QSampler.pdf

together form Figure 14 in the paper.