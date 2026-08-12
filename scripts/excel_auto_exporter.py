"""Excel Auto-Exporter for DDE Live Sync.

This script runs in the user's interactive session (Session 1), connects to the active
Excel application, and automatically exports the live updating DDE sheets to CSV files
every 10 seconds.
"""

from __future__ import annotations

import sys
import os
from pathlib import Path
import re
import time
import win32com.client
import csv

# Force stdout and stderr to UTF-8 with backslashreplace error handling to prevent any print encoding crashes
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
sys.stderr.reconfigure(encoding='utf-8', errors='backslashreplace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def sanitize_filename(filename: str) -> str:
    """Remove invalid chars and file extensions to create a clean CSV name."""
    name = Path(filename).stem
    return name.strip()


def export_active_workbooks():
    try:
        # Connect to the running instance of Excel
        xl = win32com.client.GetActiveObject("Excel.Application")
    except Exception:
        print("[אזהרה] אקסל אינו פתוח כעת. מחכה לפתיחת אקסל...")
        return

    try:
        workbooks_count = xl.Workbooks.Count
        if workbooks_count == 0:
            print("[מידע] אין חוברות עבודה פתוחות באקסל.")
            return

        for i in range(1, workbooks_count + 1):
            wb = xl.Workbooks(i)
            name_lower = wb.Name.lower()

            # Identify options chain workbooks
            is_options = any(
                k in name_lower for k in ["נגזרים", "option", "dde", "שבועית", "אוגוסט", "תא 35", "תא-35", "יומית"]
            )
            if not is_options:
                continue

            try:
                ws = wb.ActiveSheet
                clean_name = sanitize_filename(wb.Name)
                
                # We append '_live' to avoid Windows permission/file-lock errors 
                # since Excel holds exclusive locks on the open files
                dest_name = f"{clean_name}_live.csv"
                dest_path = PROJECT_ROOT / dest_name

                print(f"[עדכון] מייצא את {wb.Name} -> {dest_name}...")
                
                # Read all values directly from Excel COM memory
                data = ws.UsedRange.Value
                if data:
                    # If it's a single cell value, wrap it
                    if not isinstance(data, (list, tuple)):
                        data = [[data]]
                    
                    with open(dest_path, "w", newline="", encoding="utf-8-sig") as f:
                        writer = csv.writer(f)
                        for row in data:
                            if isinstance(row, (list, tuple)):
                                clean_row = [str(cell) if cell is not None else "" for cell in row]
                            else:
                                clean_row = [str(row) if row is not None else ""]
                            writer.writerow(clean_row)
                    print(f"  [OK] קובץ יוצא בהצלחה ל-{dest_name}")
                else:
                    print(f"  [אזהרה] גיליון ריק ב-{wb.Name}")
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                print(f"[שגיאה] כשל בייצוא {wb.Name}: {e}")
                print(tb)
    except Exception as e:
        print(f"[שגיאה] כשל בסריקת אקסל: {e}")


def main():
    print("=" * 60)
    print(" מייצא אקסל אוטומטי לנתוני DDE בלייב - פועל ברקע")
    print("=" * 60)
    print(f"נתיב פרויקט: {PROJECT_ROOT}")
    print("המערכת תייצא אוטומטית כל 10 שניות כל גיליון אופציות פתוח...")
    print("ניתן לסגור חלון זה בכל עת כדי להפסיק את הסנכרון.")
    print("-" * 60)

    while True:
        export_active_workbooks()
        time.sleep(10)


if __name__ == "__main__":
    main()
