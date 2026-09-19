import json
from decimal import Decimal

from django.shortcuts import render, redirect

from .models import WeeklyReport
from .forms import WeeklyReportForm
from .analysis_engine import analyze_reports


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def format_number(value):
    if value is None:
        return 0

    if isinstance(value, Decimal):
        return float(value)

    return value


def percentage_change(current, previous):
    if previous in [None, 0]:
        return None

    return ((current - previous) / previous) * 100


def normalize_percentage(value):
    """
    Komisyon gibi alanlar 0.188 veya 18.8 şeklinde
    girilmiş olabilir.
    """

    if value is None:
        return 0

    value = float(value)

    if abs(value) <= 1:
        return value * 100

    return value


def build_sparkline(
    values,
    width=170,
    height=50,
    padding=6
):
    """
    Dashboard için SVG sparkline koordinatları üretir.
    """

    if not values:
        return {
            "points": "",
            "last_point": "",
            "last_x": "",
            "last_y": "",
        }

    numeric_values = [
        float(v or 0)
        for v in values
    ]

    if len(numeric_values) == 1:

        x = width / 2
        y = height / 2

        point = f"{x:.1f},{y:.1f}"

        return {
            "points": point,
            "last_point": point,
            "last_x": f"{x:.1f}",
            "last_y": f"{y:.1f}",
        }

    minimum = min(numeric_values)
    maximum = max(numeric_values)

    value_range = maximum - minimum

    points = []

    for index, value in enumerate(
        numeric_values
    ):

        x = padding + (
            index
            * (width - 2 * padding)
            / (len(numeric_values) - 1)
        )

        if value_range == 0:

            y = height / 2

        else:

            normalized = (
                value - minimum
            ) / value_range

            y = (
                height
                - padding
                - (
                    normalized
                    * (height - 2 * padding)
                )
            )

        points.append(
            f"{x:.1f},{y:.1f}"
        )

    last_x, last_y = (
        points[-1].split(",")
    )

    return {
        "points": " ".join(points),
        "last_point": points[-1],
        "last_x": last_x,
        "last_y": last_y,
    }


# ============================================================
# DASHBOARD
# ============================================================

def dashboard(request):

    # --------------------------------------------------------
    # TÜM HAFTALAR
    # --------------------------------------------------------

    all_reports = list(
        WeeklyReport.objects
        .all()
        .order_by("-year", "-week")
    )

    # --------------------------------------------------------
    # NORMAL DASHBOARD
    #
    # Son 4 hafta
    #
    # Örnek:
    # 34 - 35 - 36 - 37
    # --------------------------------------------------------

    reports = all_reports[:4]

    reports_chart = list(
        reversed(reports)
    )

    latest = (
        reports[0]
        if reports
        else None
    )

    # --------------------------------------------------------
    # İADE DASHBOARD
    #
    # Son 4 haftanın ÖNCESİNDEKİ 4 HAFTA
    #
    # 37 aktif:
    # 30 - 31 - 32 - 33
    #
    # 38 aktif:
    # 31 - 32 - 33 - 34
    #
    # 39 aktif:
    # 32 - 33 - 34 - 35
    # --------------------------------------------------------

    return_reports = all_reports[4:8]

    return_reports_chart = list(
        reversed(return_reports)
    )

    # --------------------------------------------------------
    # RAPOR SECTIONS
    # --------------------------------------------------------

    sections = [

        {
            "title": "SATIŞ",
            "icon": "💰",
            "metrics": [

                (
                    "Haftalık Brüt Ciro",
                    "gross_revenue",
                    "currency"
                ),

                (
                    "Brüt Satış Adedi",
                    "gross_sales_quantity",
                    "number"
                ),

                (
                    "Ort. Komisyon Oranı",
                    "average_commission_rate",
                    "percent"
                ),

                (
                    "Tedarik Edilemeyen Ürün Adedi",
                    "unavailable_product_count",
                    "number"
                ),

                (
                    "Tedarik Edememe Oranı",
                    "unavailable_rate",
                    "percent_property"
                ),

                (
                    "Kargoya Teslim Süresi",
                    "delivery_time",
                    "decimal"
                ),

                (
                    "Satışa Dönüş Oranı",
                    "sales_conversion_rate",
                    "percent_property"
                ),
            ],
        },

        {
            "title": "ÜRÜN & GÖRÜNTÜLEME",
            "icon": "📦",
            "metrics": [

                (
                    "Aktif Ürün Stok Adedi",
                    "active_product_stock",
                    "number"
                ),

                (
                    "Aktif Renk Bazlı Model Adedi",
                    "active_model_count",
                    "number"
                ),

                (
                    "Toplam Görüntülenme Sayısı",
                    "total_views",
                    "number"
                ),

                (
                    "Satıcı Görüntülenme Sayısı",
                    "seller_views",
                    "number"
                ),

                (
                    "Sepete Eklenme Sayısı",
                    "add_to_cart_count",
                    "number"
                ),

                (
                    "Brüt Sipariş Adedi",
                    "gross_order_count",
                    "number"
                ),

                (
                    "Mağaza Takipçi Sayısı",
                    "follower_count",
                    "number"
                ),
            ],
        },

        {
            "title": "ÜRÜN REKLAMLARI",
            "icon": "📢",
            "metrics": [

                (
                    "Reklam Cirosu",
                    "product_ad_revenue",
                    "currency"
                ),

                (
                    "Reklam Harcaması",
                    "product_ad_spend",
                    "currency"
                ),

                (
                    "Harcama Getirisi / ROAS",
                    "product_ad_roas",
                    "roas"
                ),

                (
                    "Görüntülenme Sayısı",
                    "product_ad_impressions",
                    "number"
                ),

                (
                    "Tıklanma Sayısı",
                    "product_ad_clicks",
                    "number"
                ),
            ],
        },

        {
            "title": "META REKLAMLARI",
            "icon": "📣",
            "metrics": [

                (
                    "Meta Reklam Cirosu",
                    "meta_ad_revenue",
                    "currency"
                ),

                (
                    "Meta Reklam Harcaması",
                    "meta_ad_spend",
                    "currency"
                ),

                (
                    "Meta ROAS",
                    "meta_ad_roas",
                    "roas"
                ),

                (
                    "Görüntülenme Sayısı",
                    "meta_ad_impressions",
                    "number"
                ),

                (
                    "Tıklanma Sayısı",
                    "meta_ad_clicks",
                    "number"
                ),
            ],
        },

        # ====================================================
        # İADE
        #
        # Buradaki alanlar normal dashboard'dan farklı olarak
        # return_reports_chart üzerinden beslenecek.
        # ====================================================

        {
            "title": "İADE",
            "icon": "↩️",
            "metrics": [

                (
                    "İade Adedi",
                    "return_count",
                    "number"
                ),

                (
                    "Kaybedilen Ciro",
                    "return_lost_revenue",
                    "currency"
                ),
            ],
        },

        {
            "title": "İPTAL",
            "icon": "❌",
            "metrics": [

                (
                    "İptal Adedi",
                    "cancellation_count",
                    "number"
                ),

                (
                    "Kaybedilen Ciro",
                    "cancellation_lost_revenue",
                    "currency"
                ),
            ],
        },

        {
            "title": "KAMPANYAYA GİREN STOK",
            "icon": "🏷️",
            "metrics": [

                (
                    "Üründen Kazan Kuponu",
                    "coupon_stock_count",
                    "number"
                ),

                (
                    "Komisyon",
                    "commission_stock_count",
                    "number"
                ),

                (
                    "3 Yıldız",
                    "three_star_stock_count",
                    "number"
                ),

                (
                    "2 Yıldız",
                    "two_star_stock_count",
                    "number"
                ),

                (
                    "1 Yıldız",
                    "one_star_stock_count",
                    "number"
                ),

                (
                    "Kampanya",
                    "campaign_stock_count",
                    "number"
                ),
            ],
        },

        {
            "title": "KAMPANYAYA GİREN MODEL SAYISI",
            "icon": "🧩",
            "metrics": [

                (
                    "Üründen Kazan Kuponu",
                    "coupon_model_count",
                    "number"
                ),

                (
                    "Komisyon",
                    "commission_model_count",
                    "number"
                ),

                (
                    "3 Yıldız",
                    "three_star_model_count",
                    "number"
                ),

                (
                    "2 Yıldız",
                    "two_star_model_count",
                    "number"
                ),

                (
                    "1 Yıldız",
                    "one_star_model_count",
                    "number"
                ),

                (
                    "Kampanya",
                    "campaign_model_count",
                    "number"
                ),
            ],
        },

        {
            "title": "KAMPANYA GETİRİSİ CİRO",
            "icon": "📈",
            "metrics": [

                (
                    "Komisyon",
                    "commission_revenue",
                    "currency"
                ),

                (
                    "Yıldız",
                    "three_star_revenue",
                    "currency"
                ),

                (
                    "Kampanya",
                    "campaign_revenue",
                    "currency"
                ),

                (
                    "Üründen Kazan Kuponu",
                    "coupon_revenue",
                    "currency"
                ),
            ],
        },
    ]

    # ========================================================
    # DASHBOARD METRİKLERİNİ HAZIRLA
    # ========================================================

    dashboard_sections = []

    for section_index, section in enumerate(
        sections
    ):

        prepared_metrics = []

        # ----------------------------------------------------
        # İADE İÇİN FARKLI RAPOR SETİ
        # ----------------------------------------------------

        if section["title"] == "İADE":

            source_reports = (
                return_reports_chart
            )

        else:

            source_reports = (
                reports_chart
            )

        # ----------------------------------------------------
        # METRİKLER
        # ----------------------------------------------------

        for metric_index, (
            label,
            field,
            value_type
        ) in enumerate(
            section["metrics"]
        ):

            values = []
            display_values = []

            for report in source_reports:

                value = getattr(
                    report,
                    field,
                    0
                )

                if value is None:
                    value = 0

                value = format_number(
                    value
                )

                if value_type in [
                    "percent",
                    "percent_property"
                ]:

                    value = normalize_percentage(
                        value
                    )

                value = float(value)

                values.append(value)

                # --------------------------------------------
                # GÖRÜNÜM
                # --------------------------------------------

                if value_type == "currency":

                    display = (
                        f"₺{value:,.0f}"
                    )

                elif value_type in [
                    "percent",
                    "percent_property"
                ]:

                    display = (
                        f"{value:.2f}%"
                    )

                elif value_type == "roas":

                    display = (
                        f"{value:.2f}"
                    )

                elif value_type == "decimal":

                    display = (
                        f"{value:.2f}"
                    )

                else:

                    display = (
                        f"{value:,.0f}"
                    )

                display_values.append(
                    display
                )

            # ------------------------------------------------
            # DEĞİŞİM
            #
            # İADE için:
            # 30 → 31 → 32 → 33
            #
            # Normal KPI için:
            # 34 → 35 → 36 → 37
            # ------------------------------------------------

            change = None

            if len(values) >= 2:

                change = percentage_change(
                    values[-1],
                    values[-2]
                )

            # ------------------------------------------------
            # TREND SINIFI
            # ------------------------------------------------

            if change is None:

                trend_class = "neutral"

            elif change > 0:

                trend_class = "positive"

            elif change < 0:

                trend_class = "negative"

            else:

                trend_class = "neutral"

            # ------------------------------------------------
            # SPARKLINE
            # ------------------------------------------------

            sparkline = build_sparkline(
                values
            )

            prepared_metrics.append({

                "label": label,

                "values": values,

                "display_values":
                    display_values,

                "change": change,

                "chart_id":
                    f"chart_{section_index}_{metric_index}",

                "sparkline":
                    sparkline["points"],

                "last_point":
                    sparkline["last_point"],

                "last_x":
                    sparkline["last_x"],

                "last_y":
                    sparkline["last_y"],

                "trend_class":
                    trend_class,

                "type":
                    value_type,
            })

        dashboard_sections.append({

            "title":
                section["title"],

            "icon":
                section["icon"],

            "metrics":
                prepared_metrics,
        })

    # ========================================================
    # GRAFİK ETİKETLERİ
    # ========================================================

    chart_labels = [

        f"{report.week}. Hafta"

        for report in reports_chart
    ]

    # ========================================================
    # KARAR MOTORU
    #
    # Tüm geçmiş veriyi gönderiyoruz.
    # Böylece ileride 4 haftalık trend analizine de
    # genişletmek kolay olacak.
    # ========================================================

    analysis_result = analyze_reports(
        list(
            reversed(all_reports)
        )
    )

    # ========================================================
    # CONTEXT
    # ========================================================

    context = {

        "reports":
            reports,

        "latest":
            latest,

        "return_reports":
            return_reports,

        "dashboard_sections":
            dashboard_sections,

        "chart_labels":
            json.dumps(
                chart_labels,
                ensure_ascii=False
            ),

        "analysis":
            analysis_result,
    }

    return render(

        request,

        "trendyol_reports/dashboard.html",

        context,
    )


# ============================================================
# YENİ HAFTA EKLE
# ============================================================

def create_report(request):

    if request.method == "POST":

        form = WeeklyReportForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                "dashboard"
            )

    else:

        form = WeeklyReportForm()

    return render(

        request,

        "trendyol_reports/report_form.html",

        {
            "form": form
        }
    )