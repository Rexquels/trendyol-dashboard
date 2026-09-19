from django import forms
from .models import WeeklyReport


class WeeklyReportForm(forms.ModelForm):

    class Meta:
        model = WeeklyReport

        fields = [
            "year",
            "week",

            "gross_revenue",
            "gross_sales_quantity",
            "average_commission_rate",
            "unavailable_product_count",
            "delivery_time",

            "active_product_stock",
            "active_model_count",
            "total_views",
            "seller_views",
            "add_to_cart_count",
            "gross_order_count",
            "follower_count",

            "product_ad_revenue",
            "product_ad_spend",
            "product_ad_impressions",
            "product_ad_clicks",

            "meta_ad_revenue",
            "meta_ad_spend",
            "meta_ad_impressions",
            "meta_ad_clicks",

            "cancellation_count",
            "cancellation_lost_revenue",

            "return_count",
            "return_lost_revenue",

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

            "commission_revenue",
            "three_star_revenue",
            "campaign_revenue",

            "coupon_stock_count",
            "coupon_model_count",
            "coupon_revenue",
        ]

        widgets = {
            "year": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "week": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 53,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            if name not in ["year", "week"]:
                field.widget.attrs.update({
                    "class": "form-control"
                })

            field.widget.attrs["placeholder"] = (
                field.label
            )