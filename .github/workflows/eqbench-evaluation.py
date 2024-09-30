#!/usr/bin/env python3
# requirements: gitpython
# eqbench <owner/repo> <branch>
# 1. Evaluates upstream master of DiffKemp on EqBench dataset.
# 2. Evaluates DiffKemp (branch in given repo) on EqBench dataset.
# 3. Compares found differences and provides them as markdown to stdout
import csv
import re
import sys
import git
import os
from subprocess import check_call, check_output, DEVNULL, Popen, PIPE
from tempfile import TemporaryDirectory, mkdtemp

UPSTREAM_REPO="diffkemp/diffkemp"

def clone_repo(repo, output_dir, branch=None):
  options=["--depth 1 "]
  if branch:
    options.append(f"-b {branch}")
  git.Repo.clone_from(f"https://github.com/{repo}", to_path=output_dir, multi_options=options
  )
cwd = mkdtemp()
cwd = str(cwd)
print(cwd)
if True:
# with TemporaryDirectory() as cwd:
  os.chdir(cwd)
  # Downloading repos
  upstream_dir = os.path.join(cwd, "diffkemp-upstream")
  # TODO simplify - current repo is already downloaded by the action
  clone_repo(UPSTREAM_REPO, upstream_dir)
  current_repo = sys.argv[1]
  current_branch = sys.argv[2]
  current_dir = os.path.join(cwd, "diffkemp-current")
  clone_repo(current_repo, current_dir, branch=current_branch)
  # Build binaries for both DiffKemp versions
  check_call(["nix", "build", f"{upstream_dir}", "-o", "upstream"])
  check_call(["nix", "build", f"{current_dir}", "-o", "current"])

  # Clone EqBench repo
  eqbench_dir = os.path.join(cwd, "EqBench")
  clone_repo("shrBadihi/EqBench", eqbench_dir)

  eqbench_tool_dir = os.path.join(cwd, "eqbench_tool")
  # Clone tool for running DiffKemp on EqBench dataset
  clone_repo("PLukas2018/EqBench-workflow", eqbench_tool_dir, branch="evaluation-enhancements")

  # Evaluate upstream
  eqbench_runner = os.path.join(eqbench_tool_dir, "run")
  command = ["nix", "develop",
            f"{upstream_dir}",
            "--command",
            eqbench_runner, eqbench_dir,
            "--diffkemp", "upstream/bin/diffkemp",
            "--output-dir", "upstream-results"]

  upstream_output = check_output(command, stderr=DEVNULL, encoding='utf-8')
  upstream_results = {
    "TN": int(re.search("true negatives: ([0-9]*)", upstream_output)[1]),
    "TP": int(re.search("true positives: ([0-9]*)", upstream_output)[1]),
    "FP": int(re.search("false positives: ([0-9]*)", upstream_output)[1]),
    "FN": int(re.search("false negatives: ([0-9]*)", upstream_output)[1])
  }
  command = ["nix", "develop",
            f"{current_dir}",
            "--command",
            eqbench_runner, eqbench_dir,
            "--diffkemp", "current/bin/diffkemp",
            "--add-cmp-opt=--use-smt",
            "--output-dir", "current-results"]

  current_output = check_output(command, stderr=DEVNULL, encoding='utf-8')
  current_results = {
    "TN": int(re.search("true negatives: ([0-9]*)", current_output)[1]),
    "TP": int(re.search("true positives: ([0-9]*)", current_output)[1]),
    "FP": int(re.search("false positives: ([0-9]*)", current_output)[1]),
    "FN": int(re.search("false negatives: ([0-9]*)", current_output)[1])
  }

  def create_diff(val,correct):
      if val==0:
         return ''
      if val < 0 and correct:
         return "$$\\color{red}${" + str(val) + "}$$"
      if val > 0 and correct:
         return "$$\\color{green}+${" + str(val) + "}$$"
      if val > 0 and not correct:
          return "$$\\color{red}+${" + str(val) + "}$$"
      if val < 0 and not correct:
          return "$$\\color{green}${" + str(val) + "}$$"
  diff = {
    "TN": create_diff(current_results["TN"] - upstream_results["TN"], True),
    "TP": create_diff(current_results["TP"] - upstream_results["TP"], True),
    "FP": create_diff(current_results["FP"] - upstream_results["FP"], False),
    "FN": create_diff(current_results["FN"] - upstream_results["FN"], False),
  }
  # taking files with detailed info, removing header, sorting them and comparing them
  # taking lines which are unique for current-results
  command = [
      "comm",
      "<(tail -n+1 upstream-results/eqbench-results.csv | sort)",
      "<(tail -n+1 current-results/eqbench-results.csv | sort)",
      "-13"
  ]
  result = check_output(" ".join(command), shell=True, text=True, executable="/bin/bash").strip()
  tn = []
  tp = []
  fp = []
  fn = []
  if result != "":
    # 0 - type
    # 1 - benchmark
    # 2 - program
    # 3 - variant (eq/neq)
    # 4 - result (eq/neq)
    # 5 - correct (eq/neq)
    for change in csv.reader(result.split("\n"), delimiter = ";"):
      print(change)
      program = "-" + "/".join(change[1:4])
      if change[5] == "True" and change[3] == "Eq":
          tn.append(program)
      elif change[5] == "True" and change[3] == "Neq":
          tp.append(program)
      elif change[5] == "True" and change[3] == "Eq":
          fp.append(program)
      elif change[5] == "False" and change[3] == "Neq":
          fn.append(program)

  tn = "\n".join(tn)
  tp = "\n".join(tp)
  fp = "\n".join(fp)
  fn = "\n".join(fn)

  outMessage = f"""
# Experiment results

| experiment | TN            | FP            | TP            | FN            |
|------------|---------------|---------------|---------------|---------------|
|EqBench|{upstream_results["TN"]}{diff["TN"]}| {upstream_results["FP"]}{diff["FP"]}| {upstream_results["TP"]}{diff["TP"]} | {upstream_results["FN"]}{diff["FN"]} |


<details>

<summary>EqBench details</summary>

New true positives:

{tp}

New false positives:

{fp}

New false negatives:

{fn}

New true negatives:

{tn}

</details>
"""
  print(outMessage)
