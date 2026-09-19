import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Render ortamındaki başlangıç kullanıcılarını oluşturur veya günceller."

    def handle(self, *args, **options):
        User = get_user_model()

        users = [
            {
                "username": os.environ.get("kaan.seyis"),
                "email": os.environ.get("kseyis45@gmail.com", ""),
                "password": os.environ.get("123456"),
                "is_superuser": True,
                "is_staff": True,
            },
            {
                "username": os.environ.get("yasin.kaya"),
                "email": os.environ.get("abc@gmail.com", ""),
                "password": os.environ.get("123456"),
                "is_superuser": False,
                "is_staff": False,
            },
        ]

        for user_data in users:
            username = user_data["username"]
            password = user_data["password"]

            if not username or not password:
                self.stdout.write(
                    self.style.WARNING(
                        "Kullanıcı bilgileri eksik olduğu için kullanıcı atlandı."
                    )
                )
                continue

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": user_data["email"],
                    "is_staff": user_data["is_staff"],
                    "is_superuser": user_data["is_superuser"],
                    "is_active": True,
                },
            )

            # Kullanıcı zaten varsa bilgilerini güncelle.
            user.email = user_data["email"]
            user.is_active = True
            user.is_staff = user_data["is_staff"]
            user.is_superuser = user_data["is_superuser"]

            # Şifreyi environment'tan gelen değerle belirle.
            user.set_password(password)

            user.save()

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Kullanıcı oluşturuldu: {username}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Kullanıcı güncellendi: {username}"
                    )
                )