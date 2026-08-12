"""Excel Auto-Exporter for DDE Live Sync.

This script runs in the user's interactive session (Session 1), connects to the active
Excel application, and automatically exports the live updating DDE sheets to CSV files
every 10 seconds.
"""

from __future__ import annotations

import os
from pathlib import Path
import time
import win32com.client

PROJECT_ROOT = Path(__file__).resolve().parent.parent


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
            return

        for i in range(1, workbooks_count + 1):
            wb = xl.Workbooks(i)
            name_lower = wb.Name.lower()

            # Identify options chain workbooks
            is_options = any(
                k in name_lower for k in ["נגזרים", "option", "dde", "שבועית", "אוגוסט", "תא 35", "תא-35"]
            )
            if not is_options:
                continue

            try:
                ws = wb.ActiveSheet
                # Determine expiration type
                if "שבועית" in name_lower or "weekly" in name_lower:
                    dest_name = "נגזרים נגזרים - תא 35 - שבועית 140826_12082026_114111.csv"
                else:
                    dest_name = "נגזרים נגזרים - תא 35 - אוגוסט 26_12082026_114146.csv"

                dest_path = PROJECT_ROOT / dest_name

                # Export active sheet to CSV
                # FileFormat = 6 corresponds to xlCSV (standard comma-separated CSV)
                # We save a copy to avoid Excel blocking the main workbook
                print(f"[עדכון] מייצא את {wb.Name} -> {dest_name}...")
                
                # Copy sheet to a temp workbook and save as CSV
                ws.Copy()
                temp_wb = xl.ActiveWorkbook
                # Disable alerts
                xl.Application.DisplayAlerts = False
                temp_wb.SaveAs(Filename=str(dest_path), FileFormat=6)  # 6 = xlCSV
                temp_wb.Close(SaveChanges=False)
                xl.Application.DisplayAlerts = True
                print(f"  ✓ קובץ יוצא בהצלחה ל-{dest_name}")
            except Exception as e:
                print(f"[שגיאה] כשל בייצוא {wb.Name}: {e}")
                # Reset alerts just in case
                try:
                    xl.Application.DisplayAlerts = True
                except:
                    pass
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
