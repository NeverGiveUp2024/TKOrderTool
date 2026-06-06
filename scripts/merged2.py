def run():
    import pandas as pd
    from pathlib import Path
    import os
    from utils.safe_excel import safe_to_excel

    BASE_DIR = Path(os.environ.get("BASE_DIR", Path.home()))

    cleaned_dir = Path(os.getenv("CLEANED_DIR", BASE_DIR / "cleaned_orders"))
    merged_dir = Path(os.getenv("MERGED_DIR", BASE_DIR / "merged_orders"))

    merged_dir.mkdir(parents=True, exist_ok=True)

    for file in cleaned_dir.glob("cleaned_*.xlsx"):
        print(f"处理：{file.name}")

        df = pd.read_excel(file, dtype=str)

        required = [
            "达人用户名",
            "创建时间",
            "产品名称",
            "下单件数"
        ]

        if not all(col in df.columns for col in required):
            print("跳过：缺列")
            continue

        grouped = df.groupby(
            ["达人用户名", "创建时间", "产品名称"],
            as_index=False
        ).agg({
            "下单件数": "count",
            "SKU ID": "first",
            "标准佣金率": "first",
            "店铺": "first",
            "内容形式": "first",
            "订单状态": "first",
            "负责人": "first"
        })

        grouped = grouped.sort_values(
            ["达人用户名", "创建时间", "产品名称"]
        )

        store_name = file.stem.replace("cleaned_", "")
        output_file = merged_dir / f"merged_{store_name}.xlsx"

        safe_to_excel(grouped, output_file)

        print(f"完成 -> {output_file}")