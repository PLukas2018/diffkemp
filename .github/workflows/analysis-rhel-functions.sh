#!/usr/bin/env bash
# ./analysis-rhel-functions <path-to-diffkemp-binary>
bin=$1
mkdir kernel
mkdir snapshots
RHEL_VERSIONS=(
  "4.18.0-80.el8"
  "4.18.0-147.el8"
  "4.18.0-193.el8"
  "4.18.0-240.el8"
  "4.18.0-305.el8"
  "4.18.0-348.el8"
)
for version in "${RHEL_VERSIONS[@]}"; do
    echo "Download and preparation RHEL $version"
    time ( rhel-kernel-get --kabi -o kernel $version >${version}.log 2>&1 )
    echo "Size kernel sources `du -sh kernel/linux-${version}`"
    echo "Cscope runtime $version"
    time (cd kernel/linux-${version} && make cscope >${version}.log 2>&1)
    echo "Size of $version after cscope `du -sh kernel/linux-${version}`"
    echo "Build kernel RHEL $version"
    time ( $bin build-kernel kernel/linux-${version} snapshots/linux-${version} kernel/linux-${version}/kabi_whitelist_x86_64 >${version}.log 2>&1 )
    echo "Size kernel snapshot `du -sh snapshots/linux-${version}`"
    echo "Size kernel sources `du -sh kernel/linux-${version}`"
    echo "Free space `df -h`"
done

for i in "${!RHEL_VERSIONS[@]}"; do
    if [[ $(($i + 1)) == ${#RHEL_VERSIONS[@]} ]]; then break; fi
    old=${RHEL_VERSIONS[$i]}
    new=${RHEL_VERSIONS[$i + 1]}
	out="diff-linux-$old-$new"
    echo "Compare RHEL $old $new"
    time ( $bin compare snapshots/linux-${old} snapshots/linux-${new} -o $out >${old}-${new}.log 2>&1 )
    echo "Size ${old} kernel sources `du -sh kernel/linux-${old}`"
    echo "Size ${new} kernel snapshot `du -sh snapshots/linux-${new}`"
    echo "Size ${old} snapshots `du -sh snapshots/linux-${old}`"
    echo "Size ${new} snapshots `du -sh snapshots/linux-${new}`"
    echo "Size ${old}-${new} diff `du -sh $out"
    echo "Size ${old}-${new} diff yaml `du -sh ${out}/diffkemp-out.yaml"
done

echo "SUBSEQUENT COMPARISON"
for i in "${!RHEL_VERSIONS[@]}"; do
    if [[ $(($i + 1)) == ${#RHEL_VERSIONS[@]} ]]; then break; fi
    old=${RHEL_VERSIONS[$i]}
    new=${RHEL_VERSIONS[$i + 1]}
	out="diff-linux-$old-$new"
    echo "Compare RHEL $old $new"
    time ( $bin compare snapshots/linux-${old} snapshots/linux-${new} >${old}-${new}.log 2>&1 )
    echo "Size ${old} kernel sources `du -sh kernel/linux-${old}`"
    echo "Size ${new} kernel snapshot `du -sh snapshots/linux-${new}`"
    echo "Size ${old} snapshots `du -sh snapshots/linux-${old}`"
    echo "Size ${new} snapshots `du -sh snapshots/linux-${new}`"
    echo "Size ${old}-${new} diff `du -sh $out"
    echo "Size ${old}-${new} diff yaml `du -sh ${out}/diffkemp-out.yaml"
done

# logs
echo LOGS
for version in ${RHEL_VERSIONS[@]}; do
    echo ${version} LOG
    cat ${version}.log
done
for i in ${!RHEL_VERSIONS[@]}; do
    if [[ $(($i + 1)) == ${#RHEL_VERSIONS[@]} ]]; then break; fi
    old=${RHEL_VERSIONS[$i]}
    new=${RHEL_VERSIONS[$i + 1]}
	out="diff-linux-$old-$new"
    echo ${old}-${new} LOG
    cat ${old}-${new}.log
done
