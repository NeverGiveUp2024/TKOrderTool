def run():
    import pandas as pd
    from pathlib import Path
    import os
    from utils.safe_excel import safe_to_excel

    BASE_DIR = Path(os.environ.get("BASE_DIR", Path.home()))

    orders_dir = Path(os.getenv("ORDERS_DIR", BASE_DIR / "data" / "orders"))
    sku_mapping_file = Path(os.getenv("SKU_FILE", BASE_DIR / "data" / "sku_mapping.xlsx"))
    influencer_mapping_file = Path(os.getenv("INFLUENCER_FILE", BASE_DIR / "data" / "influencer_mapping.xlsx"))
    output_dir = Path(os.getenv("CLEANED_DIR", BASE_DIR / "cleaned_orders"))

    output_dir.mkdir(parents=True, exist_ok=True)

    sku_df = pd.read_excel(sku_mapping_file, dtype=str).fillna("")
    sku_map_dict = {
        f"{row['Store']}_{str(row['SKU_ID'])[-4:]}": row["Product_Name"]
        for _, row in sku_df.iterrows()
    }

    influencer_df = pd.read_excel(influencer_mapping_file, dtype=str).fillna("")
    influencer_df = influencer_df.rename(
        columns={influencer_df.columns[0]: "达人用户名",
                 influencer_df.columns[1]: "负责人"}
    )

    all_unmatched = []

    for order_file in orders_dir.glob("*.xlsx"):
        store_name = order_file.stem
        print(f"开始处理：{store_name}")

        df = pd.read_excel(order_file, dtype=str)
        df["店铺"] = store_name

        df = df[[
            "达人用户名",
            "创建时间",
            "下单件数",
            "SKU ID",
            "标准佣金率",
            "店铺",
            "内容形式",
            "订单状态"
        ]]

        df["SKU后四位"] = df["SKU ID"].astype(str).str[-4:]

        df["产品名称"] = df.apply(
            lambda x: sku_map_dict.get(f"{x['店铺']}_{x['SKU后四位']}", "未匹配SKU"),
            axis=1
        )

        df = df[df["订单状态"].isin(["待确认", "已结算"])]
        df = df[df["内容形式"].astype(str).str.strip().isin(["视频", "商品橱窗", "直播"])]

        df["标准佣金率"] = df["标准佣金率"].astype(str)
        df = df[df["标准佣金率"].str.contains("%", na=False)]

        df["创建时间"] = pd.to_datetime(df["创建时间"], errors="coerce")
        df = df.dropna(subset=["创建时间"])

        df["创建时间"] = df["创建时间"].dt.strftime("%Y/%m/%d")

        df = df.sort_values(["达人用户名", "创建时间", "产品名称"])

        df = df.merge(influencer_df, on="达人用户名", how="left")
        df["负责人"] = df["负责人"].fillna("未匹配负责人")

        output_path = output_dir / f"cleaned_{store_name}.xlsx"

        # ⭐关键：强制关闭 writer
        safe_to_excel(df, output_path)

        print(f"完成：{store_name}")