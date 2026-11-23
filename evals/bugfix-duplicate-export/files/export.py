"""Export orders to CSV. A scheduler calls run_export(); on timeout it retries with the same job id."""
import csv
import sys

HEADER = ["order_id", "customer", "total"]


def export_orders(orders, path, job_id):
    """Write orders to `path` for one export job."""
    # Opened in append mode so a slow job can stream rows in several calls.
    new_file = False
    try:
        open(path).close()
    except FileNotFoundError:
        new_file = True
    with open(path, "a", newline="") as fh:
        writer = csv.writer(fh)
        if new_file:
            writer.writerow(HEADER)
        for order in orders:
            writer.writerow([order["id"], order["customer"], f'{order["total"]:.2f}'])
    return path


SAMPLE = [
    {"id": 1, "customer": "ana", "total": 12.5},
    {"id": 2, "customer": "budi", "total": 7.0},
    {"id": 3, "customer": "citra", "total": 30.25},
]

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output.csv"
    export_orders(SAMPLE, out, job_id="nightly")
    print(f"wrote {out}")
