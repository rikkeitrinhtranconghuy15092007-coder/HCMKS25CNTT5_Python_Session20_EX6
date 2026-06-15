import logging

# Cấu hình Logging
logging.basicConfig(
    filename='arena_tickets.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Mock Data
ticket_db = [
    {"ticket_id": "T01", "buyer_name": "Nguyen Van A", "price": 500.0, "status": "Booked", "seat": ("A", 1)},
    {"ticket_id": "T02", "buyer_name": "Tran Thi B", "price": 300.0, "status": "Cancelled", "seat": ("B", 5)},
    {"ticket_id": "T03", "buyer_name": "Le Van C", "price": 500.0, "status": "Booked", "seat": ("A", 2)}
]


def find_ticket_by_id(tickets: list, ticket_id: str) -> int:
    """Trả về index của vé theo ticket_id. Trả về -1 nếu không tìm thấy."""
    tid = ticket_id.strip().upper()
    for i, ticket in enumerate(tickets):
        if ticket.get("ticket_id") == tid:
            return i
    return -1


def display_tickets(tickets: list) -> None:
    """Hiển thị danh sách vé."""
    logging.info("User viewed ticket list.")
    print("\n--- DANH SÁCH VÉ ---")
    if not tickets:
        print("Hiện chưa có vé nào trong hệ thống.")
        return

    print(f"{'Mã Vé':<6} | {'Tên Khách Hàng':<15} | {'Giá Vé':<8} | {'Chỗ Ngồi':<8} | Trạng Thái")
    print("-" * 70)
    has_error = False
    for ticket in tickets:
        try:
            seat = ticket.get("seat")
            seat_str = f"{seat[0]}-{seat[1]}" if seat and isinstance(seat, tuple) else "N/A"
            status = ticket.get("status", "Unknown")
            if status == "Cancelled":
                status += " [ĐÃ HỦY]"
            print(f"{ticket.get('ticket_id','N/A'):<6} | {ticket.get('buyer_name','N/A'):<15} | "
                  f"{ticket.get('price',0):<8.1f} | {seat_str:<8} | {status}")
        except (KeyError, TypeError, IndexError):
            has_error = True
            print("Lỗi: Một vé đang bị thiếu dữ liệu, vui lòng kiểm tra lại.")
            logging.error("Missing key while displaying ticket: 'seat'")
    if has_error:
        print("-" * 70)


def book_ticket(tickets: list) -> None:
    """Đặt vé mới."""
    print("\n--- ĐẶT VÉ MỚI ---")
    try:
        ticket_id = input("Nhập mã vé: ").strip().upper()
        if find_ticket_by_id(tickets, ticket_id) != -1:
            print(f"Lỗi: Mã vé {ticket_id} đã tồn tại.")
            logging.warning(f"Duplicate ticket ID entered: {ticket_id}")
            return

        buyer_name = input("Nhập tên khách hàng: ").strip()
        while True:
            try:
                price = float(input("Nhập giá vé: ").strip())
                if price <= 0:
                    print("Giá vé phải lớn hơn 0. Vui lòng nhập lại.")
                    continue
                break
            except ValueError:
                print("Giá vé phải là số. Vui lòng nhập lại.")
                logging.warning("Invalid price input while booking ticket")

        area = input("Nhập khu vực ghế: ").strip().upper()
        while True:
            try:
                seat_num = int(input("Nhập số ghế: ").strip())
                if seat_num <= 0:
                    print("Số ghế phải lớn hơn 0. Vui lòng nhập lại.")
                    continue
                break
            except ValueError:
                print("Số ghế phải là số nguyên. Vui lòng nhập lại.")

        new_ticket = {
            "ticket_id": ticket_id,
            "buyer_name": buyer_name,
            "price": price,
            "status": "Booked",
            "seat": (area, seat_num)
        }
        tickets.append(new_ticket)
        print(f"Thành công: Đã đặt vé {ticket_id} cho khách hàng {buyer_name}.")
        logging.info(f"Booked new ticket {ticket_id} for {buyer_name}")

    except Exception as e:
        logging.error(f"Error booking ticket: {e}")


def change_seat(tickets: list) -> None:
    """Đổi chỗ ngồi."""
    print("\n--- ĐỔI CHỖ NGỒI ---")
    try:
        ticket_id = input("Nhập mã vé cần đổi chỗ: ").strip().upper()
        idx = find_ticket_by_id(tickets, ticket_id)
        if idx == -1:
            print(f"Không tìm thấy vé mang mã {ticket_id}.")
            logging.warning(f"Change seat failed - Ticket {ticket_id} not found")
            return

        area = input("Nhập khu vực ghế mới: ").strip().upper()
        while True:
            try:
                seat_num = int(input("Nhập số ghế mới: ").strip())
                if seat_num <= 0:
                    print("Số ghế phải lớn hơn 0. Vui lòng nhập lại.")
                    continue
                break
            except ValueError:
                print("Số ghế phải là số nguyên. Vui lòng nhập lại.")

        tickets[idx]["seat"] = (area, seat_num)
        print(f"Thành công: Đã đổi chỗ vé {ticket_id} sang {area}-{seat_num}.")
        logging.info(f"Seat changed for ticket {ticket_id} to {area}-{seat_num}")

    except Exception as e:
        logging.error(f"Error changing seat: {e}")


def cancel_ticket(tickets: list) -> None:
    """Hủy vé."""
    print("\n--- HỦY VÉ ---")
    try:
        ticket_id = input("Nhập mã vé cần hủy: ").strip().upper()
        idx = find_ticket_by_id(tickets, ticket_id)
        if idx == -1:
            print(f"Không tìm thấy vé mang mã {ticket_id}.")
            logging.warning(f"Cancel ticket failed - Ticket {ticket_id} not found")
            return

        ticket = tickets[idx]
        if ticket.get("status") == "Cancelled":
            print(f"Vé {ticket_id} đã ở trạng thái Cancelled trước đó.")
            return

        ticket["status"] = "Cancelled"
        print(f"Thành công: Vé {ticket_id} đã được hủy.")
        logging.warning(f"Ticket {ticket_id} has been cancelled.")

    except Exception as e:
        logging.error(f"Error cancelling ticket: {e}")


def calculate_total_revenue(tickets: list) -> float:
    """Tính tổng doanh thu chỉ từ vé Booked (đã debug)."""
    total = 0.0
    try:
        for ticket in tickets:
            if ticket.get("status") == "Booked":
                total += ticket.get("price", 0.0)
    except (KeyError, TypeError):
        logging.error("Missing key while calculating revenue: 'price'")
        return 0.0
    return total


def generate_revenue_report(tickets: list) -> None:
    """Báo cáo doanh thu."""
    logging.info("Revenue report generated.")
    print("\n--- BÁO CÁO DOANH THU ---")
    if not tickets:
        print("Tổng số vé đã đặt: 0")
        print("Tổng số vé đã hủy: 0")
        print("Tổng doanh thu hợp lệ: 0.0")
        return

    booked = sum(1 for t in tickets if t.get("status") == "Booked")
    cancelled = len(tickets) - booked
    revenue = calculate_total_revenue(tickets)

    print(f"Tổng số vé đã đặt: {booked}")
    print(f"Tổng số vé đã hủy: {cancelled}")
    print(f"Tổng doanh thu hợp lệ: {revenue:,.1f}")


def show_menu() -> None:
    print("\n=== HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===")
    print("1. Xem danh sách vé đã bán")
    print("2. Đặt vé mới")
    print("3. Đổi chỗ ngồi (Cập nhật vé)")
    print("4. Hủy vé")
    print("5. Báo cáo doanh thu")
    print("6. Thoát chương trình")
    print("=" * 45)


def main() -> None:
    tickets = ticket_db.copy()  # Làm việc trên bản sao
    while True:
        show_menu()
        try:
            choice = input("Chọn chức năng (1-6): ").strip()
            if choice == "1":
                display_tickets(tickets)
            elif choice == "2":
                book_ticket(tickets)
            elif choice == "3":
                change_seat(tickets)
            elif choice == "4":
                cancel_ticket(tickets)
            elif choice == "5":
                generate_revenue_report(tickets)
            elif choice == "6":
                logging.info("Ticket management system closed.")
                print("Cảm ơn bạn đã sử dụng hệ thống quản lý vé Rikkei Esports.")
                break
            else:
                print("Lựa chọn không hợp lệ!")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()