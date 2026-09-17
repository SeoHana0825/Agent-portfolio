#!/bin/bash

# ── 1. cs-ai-learning gateway_state.json 강제 초기화 ──────────────────
CS_STATE="/opt/data/profiles/cs-ai-learning/gateway_state.json"

if [ -f "$CS_STATE" ]; then
    cat > "$CS_STATE" << 'JSON'
{
  "desired_state": "stopped",
  "gateway_state": "stopped",
  "platforms": {},
  "kind": "hermes-gateway",
  "pid": null,
  "exit_reason": null,
  "restart_requested": false,
  "active_agents": 0
}
JSON
    echo "[entrypoint] cs-ai-learning gateway_state.json 초기화 완료"
fi

# ── 2. 대시보드 백그라운드 실행 ────────────────────────────────────────
echo "[entrypoint] 대시보드 백그라운드 시작..."
export HOME=/opt/data
cd /opt/data
. /opt/hermes/.venv/bin/activate
nohup hermes dashboard --host 0.0.0.0 --port 9119 --no-open \
    > /opt/data/logs/dashboard.log 2>&1 &
echo "[entrypoint] 대시보드 PID: $!"

# ── 3. cs-ai-learning 게이트웨이 백그라운드 실행 ───────────────────────
echo "[entrypoint] cs-ai-learning gateway 백그라운드 시작..."
nohup hermes -p cs-ai-learning gateway run \
    > /opt/data/profiles/cs-ai-learning/logs/gateway.log 2>&1 &
echo "[entrypoint] cs-ai-learning gateway PID: $!"

# ── 4. default 게이트웨이 포그라운드 실행 (PID 1 유지) ────────────────
echo "[entrypoint] default gateway 포그라운드 시작..."
exec hermes gateway run
