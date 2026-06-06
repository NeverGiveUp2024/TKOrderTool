from pathlib import Path
import pandas as pd
import os
import tempfile
import shutil
import time


def safe_to_excel(df, final_path: Path):

    final_path = Path(final_path)
    final_path.parent.mkdir(parents=True, exist_ok=True)

    # ============================
    # 1. 创建临时文件（同目录优先）
    # ============================
    fd, tmp_file = tempfile.mkstemp(suffix=".xlsx", dir=str(final_path.parent))
    os.close(fd)

    tmp_path = Path(tmp_file)

    try:
        # ============================
        # 2. 写入 Excel
        # ============================
        with pd.ExcelWriter(tmp_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        # ============================
        # 3. 如果目标存在 → 先删除
        # ============================
        if final_path.exists():

            try:
                final_path.unlink()
            except PermissionError:
                # 文件被占用 → 改名保存
                backup = final_path.with_name(
                    final_path.stem + f"_locked_{int(time.time())}.xlsx"
                )
                shutil.copy2(tmp_path, backup)
                tmp_path.unlink()
                return backup

        # ============================
        # 4. 用 copy 替代 replace（关键修复）
        # ============================
        shutil.copy2(tmp_path, final_path)
        tmp_path.unlink()

        return final_path

    except Exception as e:
        if tmp_path.exists():
            tmp_path.unlink()
        raise e