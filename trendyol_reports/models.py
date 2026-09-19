from django.db import models
from decimal import Decimal


class WeeklyReport(models.Model):
    """
    Trendyol haftalık operasyon raporu.
    Ham veriler database'de tutulur.
    Türetilmiş KPI'lar property olarak hesaplanır.
    """

    year = models.PositiveIntegerField(
        verbose_name="Yıl"
    )

    week = models.PositiveIntegerField(
        verbose_name="Hafta"
    )

    # ==========================================================
    # SATIŞ / OPERASYON
    # ==========================================================

    gross_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Haftalık Brüt Ciro"
    )

    gross_sales_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Brüt Satış Adedi"
    )

    average_commission_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=0,
        verbose_name="Ort. Komisyon Oranı"
    )

    unavailable_product_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Tedarik Edilemeyen Ürün Adedi"
    )

    delivery_time = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="Kargoya Teslim Süresi"
    )

    # ==========================================================
    # ÜRÜN / GÖRÜNTÜLENME
    # ==========================================================

    active_product_stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Aktif Ürün Stok Adedi"
    )

    active_model_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Aktif Renk Bazlı Model Adedi"
    )

    total_views = models.PositiveIntegerField(
        default=0,
        verbose_name="Toplam Görüntülenme Sayısı"
    )

    seller_views = models.PositiveIntegerField(
        default=0,
        verbose_name="Satıcı Görüntüleme Sayısı"
    )

    add_to_cart_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Sepete Eklenme Sayısı"
    )

    gross_order_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Brüt Sipariş Adedi"
    )

    follower_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Mağaza Takipçi Sayısı"
    )

    # ==========================================================
    # ÜRÜN REKLAMLARI
    # ==========================================================

    product_ad_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Ürün Reklam Cirosu"
    )

    product_ad_spend = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Ürün Reklam Harcaması"
    )

    product_ad_impressions = models.PositiveIntegerField(
        default=0,
        verbose_name="Ürün Reklam Görüntülenme"
    )

    product_ad_clicks = models.PositiveIntegerField(
        default=0,
        verbose_name="Ürün Reklam Tıklanma"
    )

    # ==========================================================
    # META REKLAMLARI
    # ==========================================================

    meta_ad_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Meta Reklam Cirosu"
    )

    meta_ad_spend = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Meta Reklam Harcaması"
    )

    meta_ad_impressions = models.PositiveIntegerField(
        default=0,
        verbose_name="Meta Reklam Görüntülenme"
    )

    meta_ad_clicks = models.PositiveIntegerField(
        default=0,
        verbose_name="Meta Reklam Tıklanma"
    )

    # ==========================================================
    # İPTAL
    # ==========================================================

    cancellation_count = models.PositiveIntegerField(
        default=0,
        verbose_name="İptal Adedi"
    )

    cancellation_lost_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="İptal Kaybedilen Ciro"
    )

    # ==========================================================
    # İADE
    # ==========================================================

    return_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="İade Adedi"
    )

    return_lost_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="İade Kaybedilen Ciro"
    )

    # ==========================================================
    # KAMPANYAYA GİREN STOK
    # ==========================================================

    commission_stock_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Komisyon Giren Stok Adedi"
    )

    three_star_stock_count = models.PositiveIntegerField(
        default=0,
        verbose_name="3 Yıldız Giren Stok Adedi"
    )

    two_star_stock_count = models.PositiveIntegerField(
        default=0,
        verbose_name="2 Yıldız Giren Stok Adedi"
    )

    one_star_stock_count = models.PositiveIntegerField(
        default=0,
        verbose_name="1 Yıldız Giren Stok Adedi"
    )

    campaign_stock_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Kampanya Giren Stok Adedi"
    )

    # ==========================================================
    # KAMPANYAYA GİREN MODEL
    # ==========================================================

    commission_model_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Komisyon Giren Model Sayısı"
    )

    three_star_model_count = models.PositiveIntegerField(
        default=0,
        verbose_name="3 Yıldız Giren Model Sayısı"
    )

    two_star_model_count = models.PositiveIntegerField(
        default=0,
        verbose_name="2 Yıldız Giren Model Sayısı"
    )

    one_star_model_count = models.PositiveIntegerField(
        default=0,
        verbose_name="1 Yıldız Giren Model Sayısı"
    )

    campaign_model_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Kampanya Giren Model Sayısı"
    )

    # ==========================================================
    # KAMPANYA CİRO GETİRİSİ
    # ==========================================================

    commission_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Komisyon Ciro Getirisi"
    )

    three_star_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Yıldız Ciro Getirisi"
    )

    campaign_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Kampanya Ciro Getirisi"
    )

    # ==========================================================
    # ÜRÜNDEN KAZAN KUPONU
    # ==========================================================

    coupon_stock_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Üründen Kazan Kupon Stok Adedi"
    )

    coupon_model_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Üründen Kazan Kupon Model Sayısı"
    )

    coupon_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Kupon Getirisi"
    )

    # ==========================================================
    # KAYIT TARİHLERİ
    # ==========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-year", "-week"]

        constraints = [
            models.UniqueConstraint(
                fields=["year", "week"],
                name="unique_year_week"
            )
        ]

        verbose_name = "Haftalık Rapor"
        verbose_name_plural = "Haftalık Raporlar"

    def __str__(self):
        return f"{self.year} - {self.week}. Hafta"

    # ==========================================================
    # HESAPLANAN KPI'LAR
    # ==========================================================

    @property
    def unavailable_rate(self):
        """Tedarik edememe oranı."""

        if self.gross_sales_quantity == 0:
            return Decimal("0")

        return (
            Decimal(self.unavailable_product_count)
            / Decimal(self.gross_sales_quantity)
        ) * 100

    @property
    def sales_conversion_rate(self):
        """Görüntülenmeden siparişe dönüşüm oranı."""

        if self.total_views == 0:
            return Decimal("0")

        return (
            Decimal(self.gross_order_count)
            / Decimal(self.total_views)
        ) * 100

    @property
    def product_ad_roas(self):
        """Ürün reklam ROAS."""

        if self.product_ad_spend == 0:
            return Decimal("0")

        return (
            self.product_ad_revenue
            / self.product_ad_spend
        )

    @property
    def meta_ad_roas(self):
        """Meta reklam ROAS."""

        if self.meta_ad_spend == 0:
            return Decimal("0")

        return (
            self.meta_ad_revenue
            / self.meta_ad_spend
        )

    @property
    def seller_view_share(self):
        """Satıcı görüntüleme payı."""

        if self.total_views == 0:
            return Decimal("0")

        return (
            Decimal(self.seller_views)
            / Decimal(self.total_views)
        ) * 100

    @property
    def average_order_value(self):
        """Ortalama sipariş tutarı."""

        if self.gross_order_count == 0:
            return Decimal("0")

        return (
            self.gross_revenue
            / Decimal(self.gross_order_count)
        )

    @property
    def campaign_revenue_total(self):
        """Komisyon + yıldız + kampanya + kupon toplam getirisi."""

        return (
            self.commission_revenue
            + self.three_star_revenue
            + self.campaign_revenue
            + self.coupon_revenue
        )