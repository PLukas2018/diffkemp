![Build](https://github.com/viktormalik/diffkemp/actions/workflows/ci.yml/badge.svg?branch=master)

# DiffKemp

DiffKemp is a framework for automatic static analysis of semantic differences
between different versions of projects written in C, with main focus on the
Linux kernel.

The main use-case of DiffKemp is to compare selected functions and configuration
options in two versions of a project and to report any discovered semantic
differences.

See the [Publication](#publications-and-talks) section to learn more about
DiffKemp.

> [!WARNING]
> DiffKemp is incomplete in its nature, hence may provide false positive
results (i.e. claiming that functions are not equivalent even though they are).
This especially happens with complex refactorings.

## Installation

You can install DiffKemp:

- By building it manually [from source](docs/installation.md)
- From a prepared RPM package that can be installed from our
  [Copr repository](https://copr.fedorainfracloud.org/coprs/viktormalik/diffkemp/):

  ```sh
  # Enabling the DiffKemp repository
  dnf install -y dnf-plugins-core
  dnf copr enable -y viktormalik/diffkemp
  # Installing DiffKemp
  dnf install -y diffkemp
  ```

## Usage

![DiffKemp commands](docs/img/commands.svg)

DiffKemp runs in two phases:

1. **Snapshot generation** takes symbols (functions) that you want to compare
   and project versions. It compiles the versions into LLVM IR
   (which it uses for the comparison) and creates
   so-called *snapshots* which contain the relevant LLVM IR files and
   additional metadata.

   There are several options for snapshot generation:
     - ```sh
       diffkemp build PROJ_DIR SNAPSHOT_DIR [SYMBOL_LIST]
       ```
       is the default snapshot generation command for `make`-based projects.
     - ```sh
       diffkemp build-kernel KERNEL_DIR SNAPSHOT_DIR SYMBOL_LIST
       ```
       is a command specialized for building snapshots from the Linux kernel.
     - ```sh
       diffkemp llvm-to-snapshot PROJ_DIR LLVM_FILE SNAPSHOT_DIR SYMBOL_LIST
       ```
       can be used if the project is already compiled into a single LLVM IR file.

   In any case, the command should be run twice, once for each of the compared
   versions.

2. **Semantic comparison** takes two snapshots, compares them for semantic
   equality, and saves a report about symbols that were compared as semantically
   different. It is invoked via:

    ```sh
    diffkemp compare SNAPSHOT_DIR_1 SNAPSHOT_DIR_2 -o COMPARE_OUTPUT_DIR
    ```

- Additionally, you can run **result viewer** to get a visualisation of
  the found differences:

  ```sh
  diffkemp view COMPARE_OUTPUT_DIR
  ```

See the [Usage reference](docs/usage.md) to learn more about how to use
individual commands.

## Examples

If you want to learn how you can use DiffKemp, you can read the following
examples:

- [Simple program](docs/examples/simple_program.md): Example of using DiffKemp
  on a very simple program (contains a few lines of code) to understand how to
  use DiffKemp, what it does, and what it gives us as a result.
- [Library](docs/examples/musl_library.md): Example of using DiffKemp
  on a more complex program, specifically on the musl C library. We will learn
  how to compare complex `make`-based projects and how to use the result viewer.
- [Linux kernel](docs/examples/linux_kernel.md): Example of using DiffKemp
  on the Linux kernel.

## Why to use DiffKemp?

- **Efficiency in code review**: DiffKemp can reduce the amount of code that you will need to review manually by eliminating changes that do not impact the behaviour of the program.
- **Detection of unintended side effects**: Comparing programs on a semantic level can detect subtle changes that might alter the program's behavior.
- **Focus on critical functions**: You can specify a list of functions which you want to compare.
- **Support for large and complex C projects** like Linux kernel, C standard libraries, cryptographic libraries, ...

## How does it work?

The main focus of DiffKemp is high scalability, such that it can be applied to
large-scale projects containing a lot of code. To achieve that, the analysed
functions are first compiled into LLVM IR, then several code transformations are
applied, and finally the comparison itself is performed.

Wherever possible, DiffKemp tries to compare instruction-by-instruction (on LLVM
IR instructions) which is typically sufficient for most of the code. When not
sufficient, DiffKemp tries to apply one of the built-in or user-supplied
*semantics-preserving patterns*. If a semantic difference is still discovered,
the relevant diffs are reported to the user.

## Development

- [Development guide](docs/development.md)

## Important implementation details

The core of DiffKemp is the *SimpLL* component, written in C++ for performance
reasons. The user inputs and comparison results are handled by Python for
simplicity. SimpLL performs several important steps:

- Simplification of the compared programs by applying multiple code
  transformations such as dead code elimination, indirect calls abstraction,
  etc.
- Debug info parsing to collect information important for the comparison.
  DiffKemp needs the analysed project to be built with debugging information in
  order to work properly.
- The comparison itself is mostly done instruction-by-instruction. In addition,
  DiffKemp handles semantics-preserving changes that adhere to one of the
  built-in patterns. Additional patterns can be specified manually and passed to
  the `compare` command.

## Contributors

The list of code and non-code contributors to this project, in pseudo-random
order:
- Viktor Malík
- Tomáš Glozar
- Tomáš Vojnar
- Petr Šilling
- Pavol Žáčik
- František Nečas
- Tomáš Kučma
- Lukáš Petr
- Tatiana Malecová
- Jakub Rozek

## Publications and talks

There is a number of publications and talks related to DiffKemp:

- NETYS'22 talk  
  [![NETYS'22 talk](http://img.youtube.com/vi/FPOUfgorF8s/0.jpg)](https://www.youtube.com/watch?v=FPOUfgorF8s)  
  and [paper](https://link.springer.com/chapter/10.1007/978-3-031-17436-0_18):  
  Malík, V., Šilling, P., Vojnar, T. (2022). Applying Custom Patterns in
  Semantic Equality Analysis. In: Koulali, MA., Mezini, M. (eds) Networked
  Systems. NETYS 2022.
- ICST'21 [paper](https://ieeexplore.ieee.org/document/9438578)
  and [talk](https://zenodo.org/record/4658966):  
  V. Malík and T. Vojnar, "Automatically Checking Semantic Equivalence between
  Versions of Large-Scale C Projects," 2021 14th IEEE Conference on Software
  Testing, Verification and Validation (ICST), 2021, pp. 329-339.
- DevConf.CZ'19 talk  
  [![DevConf.CZ'19 talk](http://img.youtube.com/vi/PUZSaLf9exg/0.jpg)](https://www.youtube.com/watch?v=PUZSaLf9exg)
