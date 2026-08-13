# -*- coding: utf-8 -*-
"""
Agent Smith - Real-time Token & Cost Tracker Engine
Tracks Input/Output Tokens per Model & Calculates USD/KRW Costs
"""

import logging
from typing import Dict, Any
from model_config import DEFAULT_MODELS, ModelConfig

logging.basicConfig(level=logging.INFO, format="[COST-TRACKER][%(asctime)s] %(message)s")


class CostTracker:
    def __init__(self, krw_exchange_rate: float = 1380.0):
        self.krw_exchange_rate = krw_exchange_rate
        self.usage_data: Dict[str, Dict[str, Any]] = {}

        # Initialize tracking counters for default models
        for model_id, config in DEFAULT_MODELS.items():
            self.usage_data[model_id] = {
                "config": config,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "cost_usd": 0.0,
                "cost_krw": 0.0
            }

    def record_usage(self, model_id: str, prompt_tokens: int, completion_tokens: int):
        """Record token usage and accumulate costs for a model"""
        if model_id not in self.usage_data:
            logging.warning(f"Unknown model_id '{model_id}', defaulting to claude-3-5-sonnet")
            model_id = "claude-3-5-sonnet"

        data = self.usage_data[model_id]
        config: ModelConfig = data["config"]

        data["prompt_tokens"] += prompt_tokens
        data["completion_tokens"] += completion_tokens
        data["total_tokens"] += (prompt_tokens + completion_tokens)

        # Calculate incremental costs
        prompt_cost = (prompt_tokens / 1_000_000.0) * config.input_cost_per_m
        completion_cost = (completion_tokens / 1_000_000.0) * config.output_cost_per_m
        total_incremental_usd = prompt_cost + completion_cost

        data["cost_usd"] += total_incremental_usd
        data["cost_krw"] += (total_incremental_usd * self.krw_exchange_rate)

        logging.info(
            f"Model [{config.name}] Usage Recorded: "
            f"+{prompt_tokens} In / +{completion_tokens} Out | "
            f"Total Cost: ${data['cost_usd']:.4f} ({data['cost_krw']:,.0f} KRW)"
        )

    def get_summary(self) -> Dict[str, Any]:
        """Return usage and cost summary across all models"""
        total_tokens_all = 0
        total_usd_all = 0.0
        total_krw_all = 0.0

        for item in self.usage_data.values():
            total_tokens_all += item["total_tokens"]
            total_usd_all += item["cost_usd"]
            total_krw_all += item["cost_krw"]

        return {
            "models": self.usage_data,
            "total_tokens_all": total_tokens_all,
            "total_usd_all": total_usd_all,
            "total_krw_all": total_krw_all,
            "krw_rate": self.krw_exchange_rate
        }

    def print_formatted_report(self):
        """Print clean CLI analytics report"""
        summary = self.get_summary()
        print("\n================ MODEL TOKEN & COST ANALYTICS REPORT ================")
        print(f"USD/KRW Exchange Rate: {summary['krw_rate']:,.0f} KRW/USD\n")
        print(f"{'Model Name':<30} | {'Prompt Tokens':<13} | {'Completion':<10} | {'Cost (USD)':<10} | {'Cost (KRW)':<12}")
        print("-" * 88)

        for model_id, data in summary["models"].items():
            cfg: ModelConfig = data["config"]
            print(
                f"{cfg.name:<30} | "
                f"{data['prompt_tokens']:<13,} | "
                f"{data['completion_tokens']:<10,} | "
                f"${data['cost_usd']:<9.4f} | "
                f"{data['cost_krw']:<11,.0f} KRW"
            )

        print("-" * 88)
        print(
            f"{'TOTAL SUMMARY':<30} | "
            f"{summary['total_tokens_all']:<26,} | "
            f"${summary['total_usd_all']:<9.4f} | "
            f"{summary['total_krw_all']:<11,.0f} KRW"
        )
        print("=====================================================================\n")


if __name__ == '__main__':
    tracker = CostTracker()
    # Simulate multi-model token usage
    tracker.record_usage("claude-3-5-sonnet", prompt_tokens=150_000, completion_tokens=35_000)
    tracker.record_usage("gpt-4o", prompt_tokens=80_000, completion_tokens=20_000)
    tracker.record_usage("qwen-2.5-coder-32b", prompt_tokens=500_000, completion_tokens=120_000)
    tracker.record_usage("deepseek-r1", prompt_tokens=200_000, completion_tokens=90_000)
    tracker.record_usage("local-vllm-qwen", prompt_tokens=1_000_000, completion_tokens=400_000)

    tracker.print_formatted_report()
