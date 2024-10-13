#!/usr/bin/env bash
# ./analysis-rhel-sysctls <path-to-diffkemp-binary>
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

cat >sysctl_list <<__END
kernel.*
vm.*
__END


for version in "${RHEL_VERSIONS[@]}"; do
    echo "Download and preparation RHEL $version"
    time ( rhel-kernel-get --kabi -o kernel $version >${version}.log 2>&1 )
    echo "Size kernel sources `du -sh kernel/linux-${version}`"
    echo "Build kernel RHEL $version"
    time ( $bin build-kernel --sysctl kernel/linux-${version} snapshots/linux-${version} sysctl_list >${version}.log 2>&1 )
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
