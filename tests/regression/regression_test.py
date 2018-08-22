"""
Regression testing using pytest.
Individual tests are specified using YAML in the tests/regression/test_specs/
directory. Each test describes a kernel module, two kernel versions between
which the module is compared, and a list of compared module parameters. For
each parameter, pairs of corresponding functions (using the parameter) along
with the expected analysis results must be provided.
This script parses the test specification and prepares testing scenarions for
pytest.
"""

from diffkemp.llvm_ir.build_llvm import LlvmKernelBuilder
from diffkemp.semdiff.function_diff import functions_diff, Result
from diffkemp.semdiff.function_coupling import FunctionCouplings
from diffkemp.simpll.simpll import simplify_modules_diff
import glob
import os
import pytest
import shutil
import yaml

specs_path = "tests/regression/test_specs"
tasks_path = "tests/regression/kernel_modules"


def collect_task_specs():
    """Collecting and parsing YAML files with test specifications."""
    result = list()
    cwd = os.getcwd()
    os.chdir(specs_path)
    for spec_file_path in glob.glob("*.yaml"):
        with open(spec_file_path, "r") as spec_file:
            spec_yaml = yaml.load(spec_file)
            if "disabled" in spec_yaml and spec_yaml["disabled"] is True:
                continue
            # One specification for each analysed parameter is created
            for param in spec_yaml["params"]:
                spec = param
                spec["module"] = spec_yaml["module"]
                spec["path"] = spec_yaml["path"]
                spec["filename"] = spec_yaml["filename"]
                spec["old_kernel"] = spec_yaml["old_kernel"]
                spec["new_kernel"] = spec_yaml["new_kernel"]
                if "debug" in spec_yaml:
                    spec["debug"] = True
                else:
                    spec["debug"] = False
                spec_id = spec["module"] + "-" + spec["param"]
                result.append((spec_id, spec))
    os.chdir(cwd)
    return result


specs = collect_task_specs()


class TaskSpec:
    """
    Task specification representing one testing scenario (a kernel module with
    a parameter)
    """
    def __init__(self, spec):
        # Values from the YAML file
        module = spec["module"]
        self.module = module
        self.param = spec["param"]
        self.module_dir = spec["path"]
        self.module_src = spec["filename"]
        self.old_kernel = spec["old_kernel"]
        self.new_kernel = spec["new_kernel"]
        self.debug = spec["debug"]

        # The dictionary mapping pairs of corresponding analysed functions into
        # expected results.
        # Special values 'only_old' and 'only_new' denote functions that occur
        # in a single version of the module only.
        self.functions = dict()
        self.only_old = set()
        self.only_new = set()
        for fun, desc in spec["functions"].iteritems():
            # If only a single function is specified, both compared functions
            # are supposed to have the same name
            if isinstance(fun, str):
                fun = (fun, fun)
            try:
                self.functions[fun] = Result[desc.upper()]
            except KeyError:
                if desc == "only_old":
                    self.only_old.add(fun[0])
                elif desc == "only_new":
                    self.only_new.add(fun[0])

        # Names of files
        self.task_dir = os.path.join(tasks_path, module)
        self.old = os.path.join(self.task_dir, module + "_old.ll")
        self.new = os.path.join(self.task_dir, module + "_new.ll")
        self.old_simpl = os.path.join(self.task_dir, module + "_old-" +
                                      spec["param"] + ".ll")
        self.new_simpl = os.path.join(self.task_dir, module + "_new-" +
                                      spec["param"] + ".ll")
        self.old_src = os.path.join(self.task_dir, module + "_old.c")
        self.new_src = os.path.join(self.task_dir, module + "_new.c")


def _build_module(kernel_version, module_dir, module, debug):
    """
    Build LLVM IR of the analysed module.
    """
    builder = LlvmKernelBuilder(kernel_version, module_dir, debug)
    llvm_mod = builder.build_module(module, True)
    return llvm_mod


def prepare_module(spec, kernel_version, llvm, llvm_simpl, src):
    if not os.path.isfile(llvm):
        mod = _build_module(kernel_version, spec.module_dir, spec.module,
                            spec.debug)
        shutil.copyfile(mod.llvm, llvm)
        mod_src = os.path.join(os.path.dirname(mod.llvm), spec.module_src)
        shutil.copyfile(mod_src, src)


def prepare_task(spec):
    """
    Prepare testing task (scenario). Build old and new modules if needed and
    copy created files.
    """
    # Create task dir
    if not os.path.isdir(spec.task_dir):
        os.mkdir(spec.task_dir)

    # Prepare old module
    prepare_module(spec, spec.old_kernel, spec.old, spec.old_simpl,
                   spec.old_src)
    # Prepare new module
    prepare_module(spec, spec.new_kernel, spec.new, spec.new_simpl,
                   spec.new_src)


@pytest.fixture(params=[x[1] for x in specs],
                ids=[x[0] for x in specs])
def task_spec(request):
    """pytest fixture to prepare tasks"""
    spec = TaskSpec(request.param)
    prepare_task(spec)
    return spec


class TestClass(object):
    """
    Main testing class. One object of the class is created for each testing
    task. Contains 2 tests for function couplings collection and for the
    actual function analysis (semantic comparison).
    """
    def test_couplings(self, task_spec):
        """
        Test collection of function couplings. Checks whether the collected
        couplings of main functions (functions using the paramter of the
        analysis) match functions specified in the test spec.
        """
        couplings = FunctionCouplings(task_spec.old, task_spec.new)
        couplings.infer_for_param(task_spec.param)

        coupled = set([(c.first, c.second) for c in couplings.main])
        assert coupled == set(task_spec.functions.keys())
        assert couplings.uncoupled_first == task_spec.only_old
        assert couplings.uncoupled_second == task_spec.only_new

    def test_simpll(self, task_spec):
        """
        Test simplifying modules with the SimpLL tool. Simplification must
        not fail and produce a valid LLVM IR file.
        """
        # First, copy LLVM IR files (simplification for all functions will be
        # done on task_spec.old_simpl and task_spec.new_simpl).
        shutil.copyfile(task_spec.old, task_spec.old_simpl)
        shutil.copyfile(task_spec.new, task_spec.new_simpl)
        # Calculate couplings and run simplification
        couplings = FunctionCouplings(task_spec.old, task_spec.new)
        couplings.infer_for_param(task_spec.param)
        for fun_pair, expected in task_spec.functions.iteritems():
            if expected != Result.TIMEOUT:
                simplify_modules_diff(task_spec.old_simpl, task_spec.new_simpl,
                                      fun_pair[0], fun_pair[1],
                                      task_spec.param)

    def test_function_comparison(self, task_spec):
        """
        Test the actual comparison of semantic difference of modules w.r.t. a
        parameter. Runs the analysis for each function couple and compares the
        result with the expected one.
        If timeout is expected, the analysis is not run to increase testing
        speed.
        """
        couplings = FunctionCouplings(task_spec.old_simpl,
                                      task_spec.new_simpl)
        couplings.infer_for_param(task_spec.param)
        for fun_pair, expected in task_spec.functions.iteritems():
            if expected != Result.TIMEOUT:
                couplings.infer_called_by(fun_pair[0], fun_pair[1])
                result = functions_diff(task_spec.old_simpl,
                                        task_spec.new_simpl,
                                        fun_pair[0], fun_pair[1],
                                        couplings.called,
                                        timeout=120)
                assert result == expected
