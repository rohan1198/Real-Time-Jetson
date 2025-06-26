#!/bin/bash

# 1. Baseline: cyclictest on a single core with no other load.
# 2. Full CPU Load: cyclictest while stressing ALL CPU cores.
# 3. Full System Load: cyclictest while stressing ALL CPU cores and the GPU.

# Usage:
# sudo ./run_rt_tests.sh


TEST_DURATION="2m"
LOG_DIR="rt_test_logs"

MEASUREMENT_CORE=3
ALL_CORES="0,1,2,3,4,5"
STRESS_WORKERS=6

CYCLICTEST_OPTS="--mlockall -p 95 -i 100 -h 1000 -q"
STRESS_NG_OPTS="--cpu $STRESS_WORKERS --cpu-method matrixprod"
GPU_BURN_DURATION_SECS=120

GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
RESET=$(tput sgr0)


if [ "$EUID" -ne 0 ]; then
  echo "${YELLOW}Please run this script with sudo.${RESET}"
  exit 1
fi

mkdir -p "$LOG_DIR"
echo "${BLUE}Log files will be saved in the '$LOG_DIR' directory.${RESET}"
echo "---------------------------------------------------------"

echo "${GREEN}Starting Test 1: Baseline latency on core $MEASUREMENT_CORE...${RESET}"
echo "Duration: $TEST_DURATION"

cyclictest -D "$TEST_DURATION" -a "$MEASUREMENT_CORE" $CYCLICTEST_OPTS > "$LOG_DIR/1_baseline_test.txt"

echo "${GREEN}Test 1 complete.${RESET}"
echo "---------------------------------------------------------"
sleep 2

echo "${GREEN}Starting Test 2: Latency under FULL CPU load...${RESET}"
echo "Stressing all cores: $ALL_CORES"

taskset -c "$ALL_CORES" stress-ng $STRESS_NG_OPTS -t "$TEST_DURATION" &
STRESS_PID=$!

cyclictest -D "$TEST_DURATION" -a "$MEASUREMENT_CORE" $CYCLICTEST_OPTS > "$LOG_DIR/2_full_cpu_load_test.txt"

wait $STRESS_PID
echo "${GREEN}Test 2 complete.${RESET}"
echo "---------------------------------------------------------"
sleep 2

echo "${GREEN}Starting Test 3: Latency under FULL SYSTEM (CPU + GPU) load...${RESET}"
echo "Stressing all cores ($ALL_CORES) and the GPU."

taskset -c "$ALL_CORES" stress-ng $STRESS_NG_OPTS -t "$TEST_DURATION" &
STRESS_PID=$!

cd ~/gpu-burn
./gpu_burn "$GPU_BURN_DURATION_SECS" &> /dev/null &
GPU_BURN_PID=$!

cyclictest -D "$TEST_DURATION" -a "$MEASUREMENT_CORE" $CYCLICTEST_OPTS > "$LOG_DIR/3_full_system_load_test.txt"

wait $STRESS_PID
wait $GPU_BURN_PID
echo "${GREEN}Test 3 complete.${RESET}"
echo "---------------------------------------------------------"

echo "${BLUE}All tests are finished. Results summary:${RESET}"
echo

echo -n "${YELLOW}Baseline Test:             ${RESET}"
grep "Max Latencies" "$LOG_DIR/1_baseline_test.txt"

echo -n "${YELLOW}Full CPU Load Test:        ${RESET}"
grep "Max Latencies" "$LOG_DIR/2_full_cpu_load_test.txt"

echo -n "${YELLOW}Full System (CPU+GPU) Test:${RESET}"
grep "Max Latencies" "$LOG_DIR/3_full_system_load_test.txt"

echo
echo "${BLUE}Detailed logs are available in the '$LOG_DIR' directory.${RESET}"
echo "---------------------------------------------------------"
