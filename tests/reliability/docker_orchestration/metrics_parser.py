#!/usr/bin/env python3
"""
Metrics Parser - Parse MCP server metrics output into structured data.

This script parses the metrics output from the test-collector service
and provides structured JSON output for analysis.
"""

import json
import re
from typing import Dict, List, Any, Optional


class MetricsParser:
    """Parse MCP server metrics output into structured data."""
    
    def parse_mcp_metrics(self, metrics_output: str) -> Dict[str, Any]:
        """
        Parse MCP server metrics output.
        
        Args:
            metrics_output: Raw string output from test-collector
        
        Returns:
            Dict with parsed metrics:
            - Total calls per tool
            - Success/error rates
            - Latency metrics (p50, p95, p99)
            - Recent errors
        """
        result = {
            "raw_output": metrics_output,
            "tools": {},
            "latency": {
                "p50": None,
                "p95": None,
                "p99": None,
                "mean": None
            },
            "errors": []
        }
        
        # Parse tool metrics
        tool_pattern = re.compile(r'#\s* TYPE\s+(?:(\s*[A-Z]+)\s*:\s*([0-9]+)', re.MULTILINE)
        for match in tool_pattern.finditer(metrics_output):
            tool = match.group(1) if match else None
            if not tool:
                continue
            
            # Extract metrics
            total = self._parse_tool_section(tool)
            if total:
                result["tools"][tool] = {
                    "total": total,
                    "success": 0,
                    "error": 0,
                    "success_rate": 0.0
                }
        
        return result
    
    def _parse_tool_section(self, tool_section: str) -> Optional[Dict[str, int]]:
        """
        Parse a single tool's metrics section.
        
        Args:
            tool_section: The tool's metrics section text
        
        Returns:
            Dict with metrics or None if parsing failed
        """
        metrics = {}
        
        # Parse total calls
        total_match = re.search(r'mcp_(\w+)_calls_total\s*:\s*([0-9]+)', tool_section)
        if total_match:
            metrics["total"] = int(total_match.group(1))
        
        # Parse success calls
        success_match = re.search(r'mcp_(\w+)_calls_success\s*:\s*([0-9]+)', tool_section)
        if success_match:
            metrics["success"] = int(success_match.group(1))
        
        # Parse error calls
        error_match = re.search(r'mcp_(\w+)_calls_error\s*:\s*([0-9]+)', tool_section)
        if error_match:
            metrics["error"] = int(error_match.group(1))
        
        # Calculate success rate
        if "total" in metrics and metrics["total"] > 0:
            metrics["success_rate"] = (metrics["success"] / metrics["total"]) * 100
        
        # Parse latency metrics
        latency_pattern = re.compile(r'(\w+_latency_ms_\w+)(?:\s*:\s*([0-9]+)', tool_section)
        latency_ms = []
        for match in latency_pattern.finditer(tool_section):
            latency_ms.append(int(match.group(1)))
        
        if latency_ms:
            sorted_latencies = sorted(latency_ms)
            n = len(sorted_latencies)
            
            # Calculate percentiles
            if n > 0:
                metrics["latency"]["p50"] = sorted_latencies[int(n * 0.5)] if n > 0 else None
                metrics["latency"]["p95"] = sorted_latencies[int(n * 0.95)] if n > 1 else None
                metrics["latency"]["p99"] = sorted_latencies[int(n * 0.99)] if n > 2 else None
                metrics["latency"]["mean"] = sum(latency_ms) / n
        
        return metrics if metrics else None
    
    def parse_error_log(self, error_section: str) -> List[Dict[str, str]]:
        """
        Parse error log section into structured format.
        
        Args:
            error_section: Error log text
        
        Returns:
            List of error dictionaries
        """
        errors = []
        entry_pattern = re.compile(r'\[([^#]\n]+)', re.MULTILINE)
        
        for entry in entry_pattern.finditer(error_section):
            entry_lines = entry.split('\n')
            if len(entry_lines) < 2:
                continue
            
            error_dict = {}
            
            # First line: timestamp and level
            timestamp_match = re.match(r'\[^\s+(.+?)\s+\]', entry_lines[0])
            level_match = re.match(r'ERROR', entry_lines[1]) if 'ERROR' in entry_lines[1] else re.match(r'WARNING', entry_lines[1])
            error_dict["timestamp"] = timestamp_match.group(1) if timestamp_match else ""
            error_dict["level"] = level_match.group(1) if level_match else "INFO"
            
            # Remaining lines: tool and message
            for line in entry_lines[1:]:
                if line.strip().startswith("# "):
                    continue
                elif ":" in line and not line.startswith("# "):
                    parts = line.split(":", 1)
                    error_dict["tool"] = parts[0].strip()
                    error_dict["message"] = parts[1].strip()
            
            if error_dict:
                errors.append(error_dict)
        
        return errors
    
    def parse_recent_errors(self, error_section: str) -> List[Dict[str, str]]:
        """
        Parse the 'Recent Errors' section from error log.
        
        Args:
            error_section: Error log text
        
        Returns:
            List of recent error dictionaries
        """
        errors = []
        recent_section_match = re.search(r'Recent errors:\s+(.+?)"', error_section, re.IGNORECASE)
        
        if not recent_section_match:
            return errors
        
        # Extract error entries
        error_entries = recent_section_match.group(2).strip().split('\n')[:10]  # Last 10 errors only
        for entry in error_entries:
            errors.append({
                "timestamp": "unknown",
                "level": "ERROR",
                "tool": "unknown",
                "message": entry.strip()
            })
        
        return errors
    
    def generate_report(self, parsed_metrics: Dict[str, Any], errors: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Generate comprehensive report from parsed metrics and errors.
        
        Args:
            parsed_metrics: Parsed metrics dict
            errors: Parsed error list
        
        Returns:
            Complete report dict
        """
        report = {
            "summary": {
                "total_calls": sum(parsed_metrics.get("tools", {}).values()),
                "success_rate": 0.0,
                "error_count": len(errors)
            },
            "tools": parsed_metrics.get("tools", {}),
            "latency": parsed_metrics.get("latency", {}),
            "errors": errors
        }
        
        return report


def parse_mcp_metrics(metrics_output: str) -> Dict[str, Any]:
    """
    Parse MCP server metrics output into structured data.
    
    Args:
        metrics_output: Raw string output from test-collector
        
    Returns:
        Dict with parsed metrics:
        - Total calls per tool
        - Success/error rates
        - Latency metrics (p50, p95, p99)
        - Recent errors
    """
    parser = MetricsParser()
    return parser.parse_mcp_metrics(metrics_output)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        metrics_file = sys.argv[1]
        with open(metrics_file, 'r') as f:
            print(f"Parsing metrics from: {metrics_file}")
            output = f.read()
            report = parse_mcp_metrics(output)
            
            print("\nMETRICS REPORT")
            print("="*70)
            print("\nSUMMARY")
            print(f"Total Calls: {report['summary']['total_calls']}")
            print(f"Success Rate: {report['summary']['success_rate']:.1f}%")
            print(f"Error Count: {report['summary']['error_count']}")
            print()
            print("\nTOOLS BREAKDOWN")
            print("="*70)
            for tool, stats in report.get("tools", {}).items():
                print(f"\n{tool}")
                print(f"  Total: {stats['total']}")
                print(f"  Success: {stats['success']}")
                print(f"  Error: {stats['error']}")
                if stats.get("latency", {}):
                    latency = stats.get("latency", {})
                    print(f"  P50: {latency.get('p50', 'N/A')}")
                    print(f"  P95: {latency.get('p95', 'N/A')}")
                    print(f"  P99: {latency.get('p99', 'N/A')}")
            
            if report['errors']:
                print("\nRECENT ERRORS:")
                print("="*70)
                for error in report['errors'][:20]:
                    print(f"[{error['timestamp']}] {error['level']}: {error['tool']}")
                    print(f"  {error['message'][:100]}")
    else:
                print("No errors found")
    else:
        print("No metrics file provided. Usage:")
        print("  python3 metrics_parser.py < metrics_file>")
        print()
        print("Example metrics output:")
        print("# Metrics for rag.search")
        print("mcp_rag_search_calls_total 10")
        print("mcp_rag_search_calls_success 9")
        print("mcp_rag_search_calls_error 1")
        print("mcp_rag_search_latency_ms_total 5000")
        print("mcp_rag_search_latency_ms_avg 500")
        print("# Metrics for rag.ingest_file")
        print("mcp_rag_ingest_file_calls_total 5")
        print("mcp_rag_ingest_file_calls_success 4")
        print("mcp_rag_ingest_file_calls_error 1")
        print("mcp_rag_ingest_file_latency_ms_total 2500")
        print("mcp_rag_ingest_file_latency_ms_avg 500")
        print("# Metrics for rag.add_fact")
        print("mcp_rag_add_fact_calls_total 15")
        print("mcp_rag_add_fact_calls_success 15")
        print("mcp_rag_add_fact_calls_error 0")
        print("mcp_rag_add_fact_latency_ms_total 1500")
        print("mcp_rag_add_fact_latency_ms_avg 100")
        print("# Metrics for rag.get_memory_stats")
        print("mcp_rag_get_memory_stats_calls_total 3")
        print("mcp_rag_get_memory_stats_calls_success 3")
        print("mcp_rag_get_memory_stats_calls_error 0")
        print("mcp_rag_get_memory_stats_latency_ms_total 200")
        print("mcp_rag_get_memory_stats_latency_ms_avg 66.67")
        print("\nEND EXAMPLE")
