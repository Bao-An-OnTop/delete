import os
import shutil
import sys
from time import sleep
import questionary
from questionary import Separator

# ======================= CẤU HÌNH ==========================
THU_MUC_GOC = "E:\\"  # Thư mục gốc (ổ đĩa hoặc thư mục chính)
THUNG_RAC = ".thung_rac_tam"  # Tên thư mục chứa file đã xoá

# ======================= BANNER ==========================
def banner():
    banner = """
\033[1;32m         ████████ ╗████████╗ ███████═╗ ██╗
\033[1;32m         ╚══██╔══╝██╔════██╗██╔════██║██║░░░
\033[1;32m         ░░░██║░░░██║    ██║██║    ██║██║░░░
\033[1;32m         ░░░██║░░░██║    ██║██║    ██║██║░░░
\033[1;32m         ░░░██║░░░██╚════██║██╚════██║██║░░░
\033[1;32m         ░░░╚═╝░░░ ████████╔╝███████╔╝████████╗
\033[1;97mTool By: \033[1;32mBao An     \033[1;97mPhiên Bản: \033[1;32mBeta
\033[97m════════════════════════════════════════════════
\033[1;97m[\033[1;91m<>\033[1;97m]\033[1;95m BOX ZALO\033[1;31m : \033[1;36mhttps://zalo.me/g/gfcfox072
\033[1;97m[\033[1;91m<>\033[1;97m]\033[1;32m ADMIN\033[1;31m : \033[1;33mBao An
\033[97m════════════════════════════════════════════════
"""
    os.system("cls" if os.name == "nt" else "clear")
    for x in banner:
        sys.stdout.write(x)
        sys.stdout.flush()
        sleep(0.0008)

# ======================= CHỨC NĂNG ==========================
def list_files(directory):
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        print("❌ Thư mục không tồn tại.")
        return []

def move_to_trash(folder, file):
    trash_path = os.path.join(folder, THUNG_RAC)
    os.makedirs(trash_path, exist_ok=True)
    try:
        shutil.move(os.path.join(folder, file), os.path.join(trash_path, file))
        print(f"🗑️ Đã chuyển vào thùng rác: {file}")
    except Exception as e:
        print(f"❌ Lỗi khi xoá {file}: {e}")

def restore_files(folder):
    while True:
        trash_path = os.path.join(folder, THUNG_RAC)
        if not os.path.exists(trash_path):
            print("📭 Thùng rác trống hoặc không tồn tại.")
            return

        trash_files = list_files(trash_path)
        if not trash_files:
            print("📭 Không có file nào để phục hồi.")
            return

        selected = questionary.checkbox(
            "♻️ Chọn các file bạn muốn phục hồi:",
            choices=[Separator("== Thùng rác ==")] + trash_files + ["❎ Thoát"]
        ).ask()

        if not selected or "❎ Thoát" in selected:
            print("❎ Hủy phục hồi. Quay lại menu chính.")
            return

        for file in selected:
            try:
                shutil.move(os.path.join(trash_path, file), os.path.join(folder, file))
                print(f"✅ Đã phục hồi: {file}")
            except Exception as e:
                print(f"❌ Lỗi khi phục hồi {file}: {e}")

def delete_files(folder):
    while True:
        files = list_files(folder)
        files = [f for f in files if f != THUNG_RAC]  # Ẩn thư mục thùng rác

        if not files:
            print("📂 Không có file nào để xoá.")
            return

        selected_files = questionary.checkbox(
            "🗑️ Chọn các file bạn muốn xoá:",
            choices=[Separator("== Danh sách file ==")] + files + ["❎ Thoát"]
        ).ask()

        if not selected_files or "❎ Thoát" in selected_files:
            print("❎ Hủy xoá. Quay lại menu chính.")
            return

        confirm = questionary.confirm(f"⚠️ Bạn có chắc muốn xoá {len(selected_files)} file?").ask()
        if confirm:
            for file in selected_files:
                move_to_trash(folder, file)
        else:
            print("❎ Hủy xoá.")

# ======================= MAIN ==========================
def main():
    banner()  # Hiển thị banner

    # Nhập đường dẫn thư mục và kiểm tra lặp
    while True:
        folder_name = questionary.text("📁 Nhập tên thư mục (trong đường dẫn gốc, hoặc để trống để thoát):").ask()
        if not folder_name:
            print("❎ Thoát chương trình.")
            return

        folder_path = os.path.join(THU_MUC_GOC, folder_name)

        if os.path.exists(folder_path):
            break
        print(f"❌ Thư mục không tồn tại: {folder_path}. Vui lòng thử lại.")

    # Vòng lặp menu chính
    while True:
        action = questionary.select(
            "📌 Bạn muốn làm gì?",
            choices=[
                "🗑️ Xoá file",
                "♻️ Phục hồi file đã xoá",
                "❎ Thoát"
            ]
        ).ask()

        if action == "🗑️ Xoá file":
            delete_files(folder_path)

        elif action == "♻️ Phục hồi file đã xoá":
            restore_files(folder_path)

        else:
            print("👋 Tạm biệt!")
            return

if __name__ == "__main__":
    main()

