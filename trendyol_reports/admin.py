from django.contrib import admin
from .models import WeeklyReport


@admin.register(WeeklyReport)
class WeeklyReportAdmin(admin.ModelAdmin):

    list_display = (
        "year",
        "week",
        "gross_revenue",
        "gross_sales_quantity",
        "average_commission_rate",
        "product_ad_roas",
        "meta_ad_roas",
        "total_views",
    )

    list_filter = (
        "year",
        "week",
    )

    search_fields = (
        "year",
        "week",
    )

    ordering = (
        "-year",
        "-week",
    )

    fieldsets = (

        (
            "Hafta Bilgisi",
            {
                "fields": (
                    "year",
                    "week",
                )
            },
        ),

        (
            "Satış / Operasyon",
            {
                "fields": (
                    "gross_revenue",
                    "gross_sales_quantity",
                    "average_commission_rate",
                    "unavailable_product_count",
                    "delivery_time",
                )
            },
        ),

        (
            "Ürün / Trafik",
            {
                "fields": (
                    "active_product_stock",
                    "active_model_count",
                    "total_views",
                    "seller_views",
                    "add_to_cart_count",
                    "gross_order_count",
                    "follower_count",
                )
            },
        ),

        (
            "Ürün Reklamları",
            {
                "fields": (
                    "product_ad_revenue",
                    "product_ad_spend",
                    "product_ad_impressions",
                    "product_ad_clicks",
                )
            },
        ),

        (
            "Meta Reklamları",
            {
                "fields": (
                    "meta_ad_revenue",
                    "meta_ad_spend",
                    "meta_ad_impressions",
                    "meta_ad_clicks",
                )
            },
        ),

        (
            "İptal",
            {
                "fields": (
                    "cancellation_count",
                    "cancellation_lost_revenue",
                )
            },
        ),

        (
            "İade",
            {
                "fields": (
                    "return_count",
                    "return_lost_revenue",
                )
            },
        ),

        (
            "Kampanya / Komisyon",
            {
                "fields": (
                    "commission_stock_count",
                    "three_star_stock_count",
                    "two_star_stock_count",
                    "one_star_stock_count",
                    "campaign_stock_count",
                    "commission_model_count",
                    "three_star_model_count",
                    "two_star_model_count",
                    "one_star_model_count",
                    "campaign_model_count",
                )
            },
        ),

        (
            "Kampanya Ciro Getirileri",
            {
                "fields": (
                    "commission_revenue",
                    "three_star_revenue",
                    "campaign_revenue",
                )
            },
        ),

        (
            "Üründen Kazan Kupon",
            {
                "fields": (
                    "coupon_stock_count",
                    "coupon_model_count",
                    "coupon_revenue",
                )
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )