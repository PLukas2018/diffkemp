#!/bin/bash
/switch-llvm.sh $LLVM_VERSION
python3 -m pip install -r ${DIFFKEMP_DIR}/requirements.txt --ignore-installed
mkdir -p $SIMPLL_BUILD_DIR
cd $SIMPLL_BUILD_DIR
cmake $DIFFKEMP_DIR -GNinja -DVENDOR_GTEST=On -DBUILD_VIEWER=OFF
ninja -j4
cd -
python3 -m pip install -e $DIFFKEMP_DIR
