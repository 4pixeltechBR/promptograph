import sys
import asyncio
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

# Mock mínimo do pipeline
class MockPipeline:
    class _MockMemory:
        _db = None
    memory = _MockMemory()
    cascade_adapter = None
    vlm_client = None
    web_searcher = None

from src.skills.promptograph.goal import PromptographDailyReportGoal

async def main():
    g = PromptographDailyReportGoal(MockPipeline)
    print(f"Goal name: {g.name}")
    print(f"Interval (s): {g.interval_seconds}")
    print(f"Channels: {g.channels}")
    print(f"Budget: {g.budget.max_daily_usd}")
    print()
    print("=== Relatório completo ===")
    report = await g._build_report(datetime.now())
    print(report)

if __name__ == "__main__":
    asyncio.run(main())
