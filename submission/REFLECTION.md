# REFLECTION — Top 5 Lakehouse Anti-Patterns

Anti-pattern team mình dễ gặp nhất là **Small-Files Problem**. Với dữ liệu AI telemetry hoặc streaming, mỗi request/batch nhỏ có thể tạo một file Parquet mới. Nếu chỉ nhìn tổng dung lượng thì hệ thống vẫn có vẻ ổn, nhưng số lượng file tăng nhanh làm metadata phình ra, query phải mở quá nhiều object và chi phí I/O tăng không cần thiết.

Điểm mình rút ra từ lab là không nên coi `OPTIMIZE` như một thao tác dọn dẹp khi hệ thống đã chậm. Cần thiết kế ngay từ đầu: gom micro-batch hợp lý, đặt target file size, chạy compaction định kỳ và clustering/Z-ORDER theo các cột lọc thường xuyên. Đồng thời phải theo dõi file count, kích thước file trung bình và pruning ratio như metric vận hành.

Ngoài ra, maintenance phải đi theo vòng đời đầy đủ: compaction chỉ tạo file mới; các file cũ/orphan vẫn cần VACUUM, snapshot expiry và orphan sweep. Nếu thiếu bước này, hiệu năng có thể tốt hơn nhưng chi phí lưu trữ vẫn tiếp tục tăng.
