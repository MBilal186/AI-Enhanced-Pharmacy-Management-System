import os
import csv
from datetime import datetime
from collections import defaultdict

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALES_FILE = os.path.join(BASE_DIR, "dataset", "sales.csv")


class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:#0f0f1a; color:white;")
        self.sales = self.load_sales()
        self.init_ui()

    def load_sales(self):
        sales = []
        if not os.path.exists(SALES_FILE):
            return sales

        with open(SALES_FILE, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row["quantity"] = int(row["quantity"])
                    row["total"] = float(row["total"])
                    row["date"] = datetime.strptime(
                        row["date"].split()[0], "%Y-%m-%d"
                    )
                    sales.append(row)
                except:
                    pass
        return sales

    def init_ui(self):
        main = QVBoxLayout(self)
        main.setSpacing(24)

        main.addLayout(self.summary_cards())
        main.addLayout(self.graphs_section())

    def summary_cards(self):
        layout = QHBoxLayout()
        layout.setSpacing(14)

        total_sales = sum(s["total"] for s in self.sales)
        today = datetime.now().date()
        today_sales = sum(s["total"] for s in self.sales if s["date"].date() == today)
        transactions = len(self.sales)

        med_qty = defaultdict(int)
        for s in self.sales:
            med_qty[s["medicine_name"]] += s["quantity"]
        top_med = max(med_qty, key=med_qty.get) if med_qty else "N/A"

        cards = [
            ("💰 Total Sales", f"PKR {total_sales:,.0f}"),
            ("📅 Today Sales", f"PKR {today_sales:,.0f}"),
            ("🧾 Transactions", str(transactions)),
            ("🏆 Top Medicine", top_med)
        ]

        for title, value in cards:
            layout.addWidget(self.card(title, value))

        return layout

    def card(self, title, value):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background:#1a001a;
                border-radius:16px;
                padding:16px;
                border:2px solid #3498db;
            }
        """)
        v = QVBoxLayout(frame)

        t = QLabel(title)
        t.setStyleSheet("color:#00ffff;font-size:14px;")

        val = QLabel(value)
        val.setStyleSheet("font-size:18px;font-weight:bold;color:white;")

        v.addWidget(t)
        v.addWidget(val)
        return frame

    def graphs_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(28)

        layout.addWidget(self.sales_trend_graph())

        bottom = QHBoxLayout()
        bottom.setSpacing(24)
        bottom.addWidget(self.top_medicines_graph())
        bottom.addWidget(self.sales_distribution_graph())

        layout.addLayout(bottom)
        return layout

    def sales_trend_graph(self):
        daily = defaultdict(float)
        for s in self.sales:
            daily[s["date"].date()] += s["total"]

        dates = sorted(daily.keys())
        values = [daily[d] for d in dates]

        fig = Figure(figsize=(9, 4), facecolor="#0f0f1a")
        ax = fig.add_subplot(111)

        ax.plot(dates, values, marker="o", linewidth=2)

        ax.set_title("Sales Trend", color="white", fontsize=12)
        ax.set_xlabel("Date", color="white")
        ax.set_ylabel("Sales (PKR)", color="white")

        ax.tick_params(axis='x', rotation=35, colors="white")
        ax.tick_params(axis='y', colors="white")
        ax.grid(True, alpha=0.3)

        fig.tight_layout()
        return FigureCanvas(fig)

    def top_medicines_graph(self):
        med_qty = defaultdict(int)
        for s in self.sales:
            med_qty[s["medicine_name"]] += s["quantity"]

        meds = sorted(med_qty, key=med_qty.get, reverse=True)[:5]
        qty = [med_qty[m] for m in meds]

        fig = Figure(figsize=(5, 4), facecolor="#0f0f1a")
        ax = fig.add_subplot(111)

        ax.bar(meds, qty)

        ax.set_title("Top Selling Medicines", color="white", fontsize=12)
        ax.set_ylabel("Quantity Sold", color="white")

        ax.tick_params(axis='x', rotation=30, labelsize=9, colors="white")
        ax.tick_params(axis='y', colors="white")

        fig.tight_layout()
        return FigureCanvas(fig)

    def sales_distribution_graph(self):
        med_sales = defaultdict(float)
        for s in self.sales:
            med_sales[s["medicine_name"]] += s["total"]

        labels = list(med_sales.keys())[:5]
        sizes = [med_sales[l] for l in labels]

        fig = Figure(figsize=(5, 4), facecolor="#0f0f1a")
        ax = fig.add_subplot(111)

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=140,
            textprops={"color": "white", "fontsize": 9}
        )

        for t in autotexts:
            t.set_color("white")

        ax.set_title("Sales Distribution", color="white", fontsize=12)

        fig.tight_layout()
        return FigureCanvas(fig)