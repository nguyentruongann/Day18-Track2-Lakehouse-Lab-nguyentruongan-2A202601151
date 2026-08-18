# Lab 18 — Hướng dẫn chạy và nộp bài

## 1. Môi trường nên dùng

Repo này dùng đường dẫn `.venv/bin/...` trong `Makefile`, vì vậy chạy trực tiếp trên **macOS/Linux**. Nếu máy là Windows, nên chạy trong **WSL2 Ubuntu**, không chạy Makefile bằng PowerShell/CMD.

Yêu cầu: Python 3.10–3.14, `make`, `git` (và `unzip` nếu dùng file ZIP). GPU, Docker và API key không cần cho lightweight path.

> Sau khi dependencies đã được cài vào `.venv`, các notebook chạy offline. Bước `make setup` lần đầu vẫn cần truy cập package index nếu máy chưa có cache package.

## 2. Chạy từ đầu

```bash
cd Day18-Track2-Lakehouse-Lab-nguyentruongan-2A202601151
make setup
make smoke
make data
make data-ai
make test
make run-all
```

Kết quả cần đạt:

- `make test`: tất cả pytest pass. Lưu ý archive hiện tại có **24 test functions** dù README/rubric cũ ghi 22.
- `make run-all`: `8/8 passed` và NB1–NB8 đều in `NBx complete.`.

Nếu muốn đảm bảo trạng thái sạch trước khi chấm:

```bash
make clean
make setup
make smoke
make data
make data-ai
make test
make run-all
```

## 3. Lưu output vào 8 notebook `.ipynb`

`make run-all` kiểm tra code nhưng không ghi output vào file notebook. Để tạo notebook có output để nộp:

```bash
.venv/bin/jupytext --to notebook --update notebooks/*.py
for f in notebooks/0*.ipynb; do
  .venv/bin/jupyter nbconvert --to notebook --execute --inplace "$f" \
    --ExecutePreprocessor.timeout=1200
done
```

Sau đó mở `make lab` và kiểm tra nhanh output cuối mỗi notebook có `NB1 complete.` ... `NB8 complete.`.

## 4. Tạo artefact nộp bài

Sau khi `make run-all` đã chạy:

```bash
make prepare-submission
```

Lệnh này tạo:

- `submission/screenshots/lakehouse_tree.txt`
- `submission/screenshots/delta_log_sample.json`

`submission/REFLECTION.md` đã được chuẩn bị dưới giới hạn 200 từ.

## 5. Windows + WSL2

Trong Ubuntu/WSL:

```bash
sudo apt update
sudo apt install -y make unzip python3 python3-venv git
python3 --version
```

Nếu Python nằm ngoài 3.10–3.14, cài một bản phù hợp hoặc dùng `uv`. Nên copy repo vào thư mục Linux như `~/lab18/` thay vì chạy lâu dài dưới `/mnt/c/...` để I/O Parquet nhanh hơn.

## 6. Lỗi thường gặp

- `DeltaTable has no attribute files`: đang dùng `deltalake` 0.x → `make clean && make setup`.
- `array_cosine_similarity(FLOAT[], ...)`: notebook phải cast `emb::FLOAT[256]`.
- NB2 speedup < 3×: chấp nhận nếu files-pruned ratio ≥10×.
- Thiếu Bronze/corpus: chạy lại `make data` và `make data-ai` (NB4/NB7/NB8 cũng có self-healing).
- Setup lỗi DNS/PyPI: đây là lỗi tải dependency, không phải lỗi notebook; kiểm tra mạng/proxy rồi chạy lại `make setup`.
