import argparse
import requests
import yaml
import sys
import os

API_ENDPOINT = "https://inbrief.info/api/feed"

def load_config():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, 'config.yaml')
    if not os.path.exists(config_path):
        config_path = os.path.join(base_dir, 'config.default.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}

def main():
    parser = argparse.ArgumentParser(description="Your-Chief-AI-Intelligence-Officer API Fetcher")
    parser.add_argument("--include-categories", type=str)
    parser.add_argument("--exclude-categories", type=str)
    parser.add_argument("--include-sources", type=str)
    parser.add_argument("--exclude-sources", type=str)
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--show-short-summary", type=lambda x: str(x).lower() in ['true', '1', 'yes'], default=None, help="是否显示短摘要 (true/false)")
    parser.add_argument("--show-long-summary", type=lambda x: str(x).lower() in ['true', '1', 'yes'], default=None, help="是否显示长摘要 (true/false)")
    parser.add_argument("--show-link", type=lambda x: str(x).lower() in ['true', '1', 'yes'], default=None, help="是否显示文章链接 (true/false，默认为 false)")
    parser.add_argument("--output-file", type=str, default="pulse_output.json", help="导出纯净JSON到文件，传入空字符串则不输出文件")
    args = parser.parse_args()
    
    config = load_config()
    params = {}
    
    def apply_param(k, arg_val, cfg_val=None):
        if arg_val:
            params[k] = arg_val
        elif cfg_val:
            params[k] = cfg_val
            
    apply_param("include_categories", args.include_categories, config.get("include_categories"))
    apply_param("exclude_categories", args.exclude_categories, config.get("exclude_categories"))
    apply_param("include_sources", args.include_sources, config.get("include_sources"))
    apply_param("exclude_sources", args.exclude_sources, config.get("exclude_sources"))
    apply_param("hours", args.hours)
    apply_param("limit", args.limit)

    show_short = config.get("show_short_summary", True)
    if args.show_short_summary is not None:
        show_short = args.show_short_summary

    show_long = config.get("show_long_summary", False)
    if args.show_long_summary is not None:
        show_long = args.show_long_summary

    show_link = config.get("show_link", False)
    if args.show_link is not None:
        show_link = args.show_link

    custom_host = config.get("api_host", API_ENDPOINT)

    try:
        response = requests.get(custom_host, params=params, timeout=15)
        if response.status_code == 429:
            try:
                error_data = response.json()
                detail = error_data.get('detail', "IP Rate Limit Exceeded (Interval or Daily Quota).")
            except Exception:
                detail = "IP Rate Limit Exceeded."
            print(f"Error fetching data: HTTP 429 Too Many Requests -> {detail}")
            sys.exit(1)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        
        if args.output_file and args.output_file.strip():
            import json
            with open(args.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"--- Your-Chief-AI-Intelligence-Officer: 已将 {len(articles)} 条内容保存至 {args.output_file} ---")
            return

        print(f"--- Your-Chief-AI-Intelligence-Officer: Fetched {len(articles)} items ---")
        def clean_line(text):
            return str(text).replace('\r', '').replace('\n', ' ').strip() if text else ''
            
        def clean_multi(text):
            return str(text).replace('\r', '').strip() if text else ''

        for idx, a in enumerate(articles, 1):
            cat = clean_line(a.get('category'))
            title = clean_line(a.get('title'))
            source = clean_line(a.get('source'))
            url = clean_line(a.get('url'))
            
            print(f"{idx}. [{cat.upper()}] {title} (from {source})")
            if show_short and a.get('summary'):
                print(f"   Short Summary: {clean_multi(a['summary'])}")
            if show_long and a.get('long_summary'):
                print(f"   Long Summary: {clean_multi(a['long_summary'])}")
            if show_link and url:
                print(f"   Link: {url}")
            print("-" * 40)
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
