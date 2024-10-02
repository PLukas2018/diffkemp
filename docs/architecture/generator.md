# 1. Snapshot generation

The snapshot generation phase consists of the following steps:

1. **Identifying relevant source files**:
   - Determine which parts of the project's code need to be compared. This
     typically means finding source files that contain definitions of the
     compared symbols specified by the user.
2. **Compiling source files to LLVM IR**:
   - The identified source files are compiled into LLVM modules containing
     human-readable LLVM IR using the `clang` compiler with the command
     `clang -S -emit-llvm ...`.
   - To make the oncoming comparison easier, [several optimisation passes](https://github.com/diffkemp/diffkemp/blob/master/diffkemp/llvm_ir/optimiser.py)
     (`dce` - dead code elimination, `simplifycfg` - simplifying control flow
     graph, ...) are run on the compiled LLVM modules. The passes are run using
     the `opt` utility.
3. **Creating and saving a snapshot**:
   - A snapshot, representing one version of the program prepared for
     comparison, is created from the compiled files and saved in the specified
     directory.

```mermaid
---
# This code renders an image, that does not show on the GitHub app, use
# a browser to see the image.
title: Classes involved in snapshot generation
---
classDiagram
  direction LR
  Snapshot --> SourceTree
  SourceTree --> LlvmSourceFinder
  SourceTree <|-- KernelSourceTree
  LlvmSourceFinder <|-- SingleLlvmFinder
  LlvmSourceFinder <|-- WrapperBuildFinder
  LlvmSourceFinder <|-- KernelLlvmSourceFinder
  SingleLlvmFinder <|-- SingleCBuilder
  SourceTree
  <<abstract>> LlvmSourceFinder
```

Classes involved in snapshot generation:
- [`LlvmSourceFinder`](https://github.com/diffkemp/diffkemp/blob/master/diffkemp/llvm_ir/llvm_source_finder.py):
  - An abstract class with a concrete implementation based on the command used
    for snapshot generation.
  - It is responsible for finding LLVM modules containing specific symbol. For
    some commands, it also handles finding necessary project source files and
    their compilation to LLVM IR.
- [`SourceTree`](https://github.com/diffkemp/diffkemp/blob/master/diffkemp/llvm_ir/source_tree.py):
  - Represents the source tree of analysed project.
  - This class wraps the `LlvmSourceFinder` class and provides its functionality.
  - The derived class, [`KernelSourceTree`](https://github.com/diffkemp/diffkemp/blob/master/diffkemp/llvm_ir/kernel_source_tree.py),
    extends its functionality by enabling to retrieve modules containing
    definitions of sysctl options and kernel modules.
- [`Snapshot`](https://github.com/diffkemp/diffkemp/blob/master/diffkemp/snapshot.py)
  - Represents the snapshot, which contains:
    - Relevant source files, including those containing definitions of the
      compared symbols.
    - The source files compiled into LLVM IR, which are used for the actual
      comparison.
    - Metadata, saved in the snapshot directory as a `snapshot.yaml` file with
      the following structure:
      ```yaml
      # For more details, refer to the implementation
      - created_time: Date and time of snapshot creation (YYYY-MM-DD hh:mm:ss.sTZ)
        diffkemp_version: x.y.z
        list: # List of compared symbols (functions or sysctl options) and their metadata
        # In cases of function comparison, contains directly the list from the `functions` field`.
        - functions:
          - glob_var: null # Name of the global variable whose usage is analysed within the function (only for sysctl).
            name: Name of function
            llvm: Relative path to module containing the function
            tag: null # Only for sysctl, describes if the function is proc handler or uses the sysctl data variable
          # Only for sysctl
          sysctl: Sysctl option name
        list_kind: Type of comparison (function/sysctl)
        llvm_source_finder:
          kind: Used LlvmSourceFinder class
        llvm_version: XX
        source_dir: Absolute path to the project's source directory
      ```

## a) Snapshot generation of `make`-based projects (`build`)

The `build` command is used to create snapshots from `make`-based projects.
The process includes the following steps:

1. The `make` command is executed on the project with [`cc_wrapper`](#cc-wrapper)
   used as the compiler instead of a standard compiler like `gcc`.
2. By running `make`, the project's source files are compiled to LLVM modules by
   the `cc_wrapper` script.
3. After `make` completes the compilation, the resulting LLVM modules are
   optimised using `opt` tool.
4. The `WrapperBuildFinder` class is used to identify the LLVM modules
   containing definitions of symbols specified by the user.
5. A snapshot is generated from the identified LLVM modules.

```mermaid
---
# This code renders an image, that does not show on the GitHub app, use
# a browser to see the image.
title: Simplified sequence diagram for creating a snapshot from make-based project
config:
  sequence:
    mirrorActors: false
---
sequenceDiagram
  actor User
  User->>+build: diffkemp build PROJ_DIR [SYMBOL_LIST]
  build->>+make: make CC=cc_wrapper PROJ_DIR
  loop
    make->>+cc_wrapper: $(CC) $(CFLAGS) *.c -c -o *.o ...
    cc_wrapper->>+clang: clang -emit-llvm -S $(CFLAGS) *.c -o *.ll ...
    clang-->>-cc_wrapper: *.ll
    cc_wrapper-->>-make: *.ll
  end
  make-->>-build: *.ll
  participant O as opt
  loop for each LLVM module
    build->>+O: opt ... *.ll
    O-->>-build: optimised *.ll
  end
  build->>build: snapshot = generate_from_function_list(SYMBOL_LIST)
  build-->>-User: SNAPSHOT_DIR
```

### `cc_wrapper`

The [`cc_wrapper`](https://github.com/diffkemp/diffkemp/blob/master/diffkemp/building/cc_wrapper.py)
is a Python script that wraps the `gcc` compiler. If [RPython](https://rpython.readthedocs.io/en/latest/)
is installed on the user's system, the `cc_wrapper` is compiled into a binary
form during DiffKemp's build process using RPython. This binary form speeds up
the snapshot generation process.

The `cc_wrapper` operates as follows:
- The `cc_wrapper` is invoked by `make` receiving the source file and options
  which would be used for compilation.
- The wrapper executes the original command using `gcc`, and additionally it
  compiles the C source file into LLVM module using `clang` and the received
  options.
- The user can optionally specify options to be added or removed when compiling
  the file to an LLVM module. These options are passed from the main DiffKemp
  script to the wrapper via system environment variables (the variables are
  prefixed with `DIFFKEMP_WRAPPER_`).
- The paths to the generated LLVM modules, along with flags indicating how they
  were created, are recorded in a file named `diffkemp-wdb`. The `f` flag
  indicates that the module was created by linking already compiled LLVM
  modules. The file format looks like this:
  ```
  o:/abs/path/to/module.ll
  f:/abs/path/to/linked_module.ll
  ...
  ```
  The `diffkemp-wdb` file is later used by the `WrapperBuildFinder` to locate
  modules containing the specified functions, which are then included in the
  final snapshot.

## aa) Snapshot generation of single C file (`build`)

The `build` command can also be used to create snapshots from a single C file.
It uses the [`SingleCBuilder`](https://github.com/diffkemp/diffkemp/blob/master/diffkemp/llvm_ir/single_c_builder.py)
class as the `LlvmSourceFinder`. The class also manages the compilation of the
C file into an LLVM module.

## b) Snapshot generation from the Linux kernel (`build-kernel`)

The `build-kernel` command is used to create snapshots from the Linux kernel's
source code. It compiles only the necessary files based on the symbols specified
by the user for comparison. The snapshot can be created using a list of
functions or sysctl parameters. The command uses
[`KernelLlvmSourceBuilder`](https://github.com/diffkemp/diffkemp/blob/master/diffkemp/llvm_ir/kernel_llvm_source_builder.py)
class as the `LlvmSourceFinder`. The process includes the following steps:

1. **Building a symbol cross-reference database** for the kernel using the
   [`cscope`](https://cscope.sourceforge.net/) tool. This database is then used
   to locate symbol definitions and usages within the kernel's source code.
2. **Identifying necessary files for the comparison** based on the provided
   symbol list.
   - If a **list of functions** is provided, the C source file containing the
     function definition is located using `cscope` for each function.
   - In case **list of sysctl parameters** is provided, the process is slightly
     different:
     1. The source file containing a sysctl table describing the parameter is
        identified and compiled into LLVM module.
     2. The proc handler function name (responsible for reading/writing the
        parameter value) and data variable (a global variable updated by the
        parameter) are extracted from the sysctl table.
     3. Source files containing the proc handler function and functions that
        interact with the data variable are identified using `cscope`.
3. The identified source **files are compiled into LLVM modules** using the
   following steps for each file:
   - The `make` tool is used to determine the compilation options required for
     the source file.
   - The source file is compiled into an LLVM module using `clang` with the
     discovered options. The module is then optimized using `opt` tool.
4. **A snapshot is created** from the compiled LLVM modules.

```mermaid
---
# This code renders an image, that does not show on the GitHub app, use
# a browser to see the image.
title: Simplified sequence diagram of kernel compilation to LLVM modules
config:
  sequence:
    mirrorActors: false
---
sequenceDiagram
  KernelLlvmSourceBuilder->>cscope: build cscope database
  loop for each symbol
    KernelLlvmSourceBuilder->>+cscope: get source file for symbol
    cscope-->>-KernelLlvmSourceBuilder: *.c
    KernelLlvmSourceBuilder->>+make: get command for compiling *.c file to object file
    make-->>-KernelLlvmSourceBuilder: gcc *.c -c -o *.o <options>
    KernelLlvmSourceBuilder->>+clang: clang -emit-llvm -S *.c -o *.ll <options>
    clang->>-KernelLlvmSourceBuilder: *.ll
    participant O as opt
    KernelLlvmSourceBuilder->>+O: opt ... *.ll
    O-->>-KernelLlvmSourceBuilder: optimised *.ll
  end
```

## c) Snapshot generation from a single LLVM IR file (`llvm-to-snapshot`)

The `llvm-to-snapshot` command is used to create snapshots from a single
existing LLVM module. It uses the
[`SingleLlvmFinder`](https://github.com/diffkemp/diffkemp/blob/master/diffkemp/llvm_ir/single_llvm_finder.py)
class as the `LlvmSourceFinder`.
