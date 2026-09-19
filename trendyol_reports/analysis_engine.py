from decimal import Decimal


# ============================================================
# TEMEL HESAPLAMALAR
# ============================================================

def pct_change(current, previous):
    """
    İki değer arasındaki yüzde değişim.
    """

    if previous in [None, 0]:
        return None

    return ((Decimal(str(current)) - Decimal(str(previous)))
            / Decimal(str(previous))) * 100


def calculate_conversion(report):
    """
    Brüt Sipariş / Toplam Görüntülenme
    """

    if report.total_views == 0:
        return Decimal("0")

    return (
        Decimal(report.gross_order_count)
        / Decimal(report.total_views)
    ) * 100


def calculate_cart_rate(report):
    """
    Sepete Eklenme / Toplam Görüntülenme
    """

    if report.total_views == 0:
        return Decimal("0")

    return (
        Decimal(report.add_to_cart_count)
        / Decimal(report.total_views)
    ) * 100


def calculate_cart_to_order(report):
    """
    Brüt Sipariş / Sepete Eklenme
    """

    if report.add_to_cart_count == 0:
        return Decimal("0")

    return (
        Decimal(report.gross_order_count)
        / Decimal(report.add_to_cart_count)
    ) * 100


def calculate_campaign_revenue(report):
    return (
        Decimal(report.commission_revenue or 0)
        + Decimal(report.three_star_revenue or 0)
        + Decimal(report.campaign_revenue or 0)
        + Decimal(report.coupon_revenue or 0)
    )


# ============================================================
# GENEL KPI DEĞİŞİMİ
# ============================================================

def get_kpi_changes(current, previous):

    current_conversion = calculate_conversion(current)
    previous_conversion = calculate_conversion(previous)

    current_cart_rate = calculate_cart_rate(current)
    previous_cart_rate = calculate_cart_rate(previous)

    current_cart_order = calculate_cart_to_order(current)
    previous_cart_order = calculate_cart_to_order(previous)

    return {

        "revenue": pct_change(
            current.gross_revenue,
            previous.gross_revenue
        ),

        "sales": pct_change(
            current.gross_sales_quantity,
            previous.gross_sales_quantity
        ),

        "views": pct_change(
            current.total_views,
            previous.total_views
        ),

        "cart": pct_change(
            current.add_to_cart_count,
            previous.add_to_cart_count
        ),

        "orders": pct_change(
            current.gross_order_count,
            previous.gross_order_count
        ),

        "conversion": pct_change(
            current_conversion,
            previous_conversion
        ),

        "cart_rate": pct_change(
            current_cart_rate,
            previous_cart_rate
        ),

        "cart_to_order": pct_change(
            current_cart_order,
            previous_cart_order
        ),

        "stock": pct_change(
            current.active_product_stock,
            previous.active_product_stock
        ),

        "delivery": pct_change(
            current.delivery_time,
            previous.delivery_time
        ),

        "cancellation": pct_change(
            current.cancellation_count,
            previous.cancellation_count
        ),

        "product_ad_revenue": pct_change(
            current.product_ad_revenue,
            previous.product_ad_revenue
        ),

        "product_ad_spend": pct_change(
            current.product_ad_spend,
            previous.product_ad_spend
        ),

        "product_ad_roas": pct_change(
            current.product_ad_roas,
            previous.product_ad_roas
        ),

        "campaign_revenue": pct_change(
            calculate_campaign_revenue(current),
            calculate_campaign_revenue(previous)
        ),
    }


# ============================================================
# 1 — TRAFİK → SEPET → SİPARİŞ ANALİZİ
# ============================================================

def analyze_funnel(current, previous, changes):

    findings = []
    opportunities = []
    actions = []

    views = changes["views"]
    cart = changes["cart"]
    orders = changes["orders"]
    conversion = changes["conversion"]

    # --------------------------------------------------------
    # Trafik artıyor ama sipariş artmıyor
    # --------------------------------------------------------

    if (
        views is not None
        and orders is not None
        and views >= 5
        and orders < 2
    ):

        findings.append({
            "type": "warning",
            "category": "Funnel",
            "title": "Trafik satışa dönüşmüyor",
            "message": (
                f"Görüntülenme %{views:.1f} artarken "
                f"sipariş %{orders:.1f} değişti."
            ),
        })

        actions.append({
            "priority": "high",
            "category": "Funnel",
            "action": (
                "Yüksek görüntülenme alan ürünlerde fiyat, "
                "ürün sayfası, kampanya ve stok durumunu incele."
            ),
        })

    # --------------------------------------------------------
    # Trafik artıyor + sepet artıyor + sipariş artmıyor
    # --------------------------------------------------------

    if (
        views is not None
        and cart is not None
        and orders is not None
        and views >= 5
        and cart >= 5
        and orders < 2
    ):

        findings.append({
            "type": "critical",
            "category": "Funnel",
            "title": "Sepetten siparişe geçiş problemi",
            "message": (
                "Kullanıcı ilgisi ve sepete ekleme artmasına rağmen "
                "siparişler aynı ölçekte artmadı."
            ),
        })

        actions.append({
            "priority": "high",
            "category": "Funnel",
            "action": (
                "Sepete eklenen ürünlerde fiyat, kampanya, "
                "beden/stok ve satın alma aşamasındaki "
                "kayıpları kontrol et."
            ),
        })

    # --------------------------------------------------------
    # Trafik + sepet + sipariş birlikte artıyor
    # --------------------------------------------------------

    if (
        views is not None
        and cart is not None
        and orders is not None
        and views >= 5
        and cart >= 5
        and orders >= 5
    ):

        opportunities.append({
            "category": "Funnel",
            "title": "Satış hunisi güçleniyor",
            "message": (
                "Görüntülenme, sepete ekleme ve sipariş "
                "birlikte yükseliyor."
            ),
        })

    # --------------------------------------------------------
    # Dönüşüm düşüşü
    # --------------------------------------------------------

    if conversion is not None and conversion <= -5:

        findings.append({
            "type": "warning",
            "category": "Dönüşüm",
            "title": "Satış dönüşümü geriliyor",
            "message": (
                f"Dönüşüm oranı %{abs(conversion):.1f} geriledi."
            ),
        })

    return findings, opportunities, actions


# ============================================================
# 2 — REKLAM İLİŞKİ ANALİZİ
# ============================================================

def analyze_ads(current, previous, changes):

    findings = []
    opportunities = []
    actions = []

    spend = changes["product_ad_spend"]
    revenue = changes["product_ad_revenue"]
    roas = changes["product_ad_roas"]

    # --------------------------------------------------------
    # Harcama ↑ / Ciro ↓
    # --------------------------------------------------------

    if (
        spend is not None
        and revenue is not None
        and spend >= 10
        and revenue <= -5
    ):

        findings.append({
            "type": "critical",
            "category": "Product Ads",
            "title": "Reklam harcaması verimsizleşiyor",
            "message": (
                f"Reklam harcaması %{spend:.1f} artarken "
                f"reklam cirosu %{abs(revenue):.1f} azaldı."
            ),
        })

        actions.append({
            "priority": "high",
            "category": "Product Ads",
            "action": (
                "Düşük performanslı reklamları tespit ederek "
                "bütçe dağılımını yeniden değerlendir."
            ),
        })

    # --------------------------------------------------------
    # ROAS düşüyor
    # --------------------------------------------------------

    if roas is not None and roas <= -10:

        findings.append({
            "type": "warning",
            "category": "Product Ads",
            "title": "ROAS geriliyor",
            "message": (
                f"Product Ads ROAS %{abs(roas):.1f} geriledi."
            ),
        })

        # Mutlak ROAS hâlâ güçlü mü?
        if current.product_ad_roas >= 10:

            opportunities.append({
                "category": "Product Ads",
                "title": "ROAS düşmesine rağmen seviye güçlü",
                "message": (
                    f"ROAS düşmesine rağmen mevcut seviye "
                    f"{current.product_ad_roas:.2f}."
                ),
            })

            actions.append({
                "priority": "medium",
                "category": "Product Ads",
                "action": (
                    "Reklam bütçesini tamamen kısmak yerine "
                    "düşüşe neden olan ürünleri ayırıp "
                    "performanslı ürünleri koru."
                ),
            })

    return findings, opportunities, actions


# ============================================================
# 3 — STOK ↔ SATIŞ ANALİZİ
# ============================================================

def analyze_stock(current, previous, changes):

    findings = []
    opportunities = []
    actions = []

    stock = changes["stock"]
    sales = changes["sales"]

    # --------------------------------------------------------
    # Stok artıyor + satış düşüyor
    # --------------------------------------------------------

    if (
        stock is not None
        and sales is not None
        and stock >= 10
        and sales <= -5
    ):

        findings.append({
            "type": "warning",
            "category": "Stok",
            "title": "Stok büyürken satış geriliyor",
            "message": (
                f"Aktif stok %{stock:.1f} artarken "
                f"satış adedi %{abs(sales):.1f} geriledi."
            ),
        })

        opportunities.append({
            "category": "Stok",
            "title": "Stok eritme fırsatı",
            "message": (
                "Yüksek stoklu ürünlerde kampanya veya "
                "reklam fırsatı araştırılabilir."
            ),
        })

        actions.append({
            "priority": "medium",
            "category": "Stok",
            "action": (
                "Yüksek stok + düşük satış kombinasyonundaki "
                "ürünleri kampanya aday havuzuna al."
            ),
        })

    # --------------------------------------------------------
    # Satış artıyor + stok düşüyor
    # --------------------------------------------------------

    if (
        stock is not None
        and sales is not None
        and stock <= -10
        and sales >= 5
    ):

        findings.append({
            "type": "warning",
            "category": "Stok",
            "title": "Stok riski oluşabilir",
            "message": (
                "Satış artarken aktif stok geriliyor."
            ),
        })

        actions.append({
            "priority": "high",
            "category": "Stok",
            "action": (
                "Yüksek satış hızına sahip ürünlerin "
                "stok devamlılığını kontrol et."
            ),
        })

    return findings, opportunities, actions


# ============================================================
# 4 — OPERASYON ANALİZİ
# ============================================================

def analyze_operations(current, previous, changes):

    findings = []
    opportunities = []
    actions = []

    delivery = changes["delivery"]
    cancellation = changes["cancellation"]

    # --------------------------------------------------------
    # Teslimat süresi artışı
    # --------------------------------------------------------

    if delivery is not None and delivery >= 10:

        findings.append({
            "type": "warning",
            "category": "Operasyon",
            "title": "Teslim süresi yükseldi",
            "message": (
                f"Kargoya teslim süresi %{delivery:.1f} arttı."
            ),
        })

        actions.append({
            "priority": "medium",
            "category": "Operasyon",
            "action": (
                "Mağaza ve online depo kaynaklı sevkiyat "
                "gecikmelerini incele."
            ),
        })

    # --------------------------------------------------------
    # İptal artışı
    # --------------------------------------------------------

    if cancellation is not None and cancellation >= 15:

        findings.append({
            "type": "warning",
            "category": "İptal",
            "title": "İptal adedi yükseldi",
            "message": (
                f"İptal adedi %{cancellation:.1f} arttı."
            ),
        })

        actions.append({
            "priority": "high",
            "category": "İptal",
            "action": (
                "İptallerin stok, tedarik ve sevkiyat "
                "kaynaklarını ayrı ayrı incele."
            ),
        })

    # --------------------------------------------------------
    # Teslimat + iptal birlikte kötüleşiyorsa
    # --------------------------------------------------------

    if (
        delivery is not None
        and cancellation is not None
        and delivery >= 10
        and cancellation >= 15
    ):

        findings.append({
            "type": "critical",
            "category": "Operasyon",
            "title": "Operasyonel risk sinyali",
            "message": (
                "Teslim süresi ve iptal adedi aynı dönemde yükseldi."
            ),
        })

        actions.append({
            "priority": "high",
            "category": "Operasyon",
            "action": (
                "Teslimat gecikmeleri ile iptallerin "
                "aynı siparişlerde yoğunlaşıp yoğunlaşmadığını kontrol et."
            ),
        })

    return findings, opportunities, actions


# ============================================================
# 5 — KAMPANYA ANALİZİ
# ============================================================

def analyze_campaigns(current, previous, changes):

    findings = []
    opportunities = []
    actions = []

    campaign_change = changes["campaign_revenue"]

    if campaign_change is not None:

        if campaign_change <= -15:

            findings.append({
                "type": "warning",
                "category": "Kampanya",
                "title": "Kampanya cirosu geriliyor",
                "message": (
                    f"Kampanya cirosu %{abs(campaign_change):.1f} azaldı."
                ),
            })

            actions.append({
                "priority": "medium",
                "category": "Kampanya",
                "action": (
                    "Kampanyaya giren model ve stok adetlerini "
                    "önceki haftayla karşılaştır."
                ),
            })

        elif campaign_change >= 10:

            opportunities.append({
                "category": "Kampanya",
                "title": "Kampanya performansı yükseliyor",
                "message": (
                    f"Kampanya cirosu %{campaign_change:.1f} arttı."
                ),
            })

    return findings, opportunities, actions


# ============================================================
# 6 — ANA KARAR MOTORU
# ============================================================

def analyze_reports(reports):

    if len(reports) < 2:

        return {
            "status": "insufficient_data",
            "score": 0,
            "findings": [],
            "opportunities": [],
            "actions": [],
            "message": (
                "Karşılaştırma için en az iki haftalık "
                "veri gerekiyor."
            ),
        }

    reports = sorted(
        reports,
        key=lambda x: (x.year, x.week)
    )

    previous = reports[-2]
    current = reports[-1]

    changes = get_kpi_changes(
        current,
        previous
    )

    findings = []
    opportunities = []
    actions = []

    analyzers = [
        analyze_funnel,
        analyze_ads,
        analyze_stock,
        analyze_operations,
        analyze_campaigns,
    ]

    for analyzer in analyzers:

        result = analyzer(
            current,
            previous,
            changes
        )

        findings.extend(result[0])
        opportunities.extend(result[1])
        actions.extend(result[2])

    # ========================================================
    # TEKRAR EDEN ÖNERİLERİ TEMİZLE
    # ========================================================

    unique_actions = []

    seen_actions = set()

    for action in actions:

        key = action["action"]

        if key not in seen_actions:

            seen_actions.add(key)
            unique_actions.append(action)

    actions = unique_actions

    # ========================================================
    # SKOR
    # ========================================================

    score = 100

    for finding in findings:

        if finding["type"] == "critical":
            score -= 15

        elif finding["type"] == "warning":
            score -= 7

    score += min(
        len(opportunities) * 3,
        10
    )

    score = max(
        0,
        min(100, score)
    )

    # ========================================================
    # DURUM
    # ========================================================

    if score >= 80:

        status = "strong"

    elif score >= 60:

        status = "stable"

    elif score >= 40:

        status = "attention"

    else:

        status = "critical"

    return {

        "status": status,

        "score": score,

        "current_week": current.week,

        "current_year": current.year,

        "previous_week": previous.week,

        "previous_year": previous.year,

        "changes": changes,

        "findings": findings,

        "opportunities": opportunities,

        "actions": actions,

    }