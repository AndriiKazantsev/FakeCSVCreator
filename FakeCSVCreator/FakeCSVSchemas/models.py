import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.db import models
from faker import Faker

UserModel = get_user_model()


class FakeCSVSchemes(models.Model):
    DELIMITERS = [
        (",", "Comma (,)"),
        (";", "Semicolon (;)"),
        ("\t", "Tab (\t)"),
        (" ", "Space ( )"),
        ("|", "Vertical bar (|)"),
    ]

    QUOTES = [
        ('"', 'Double-quote (")'),
        ("'", "Single-quote (')"),
    ]

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="FakeCSVSchemas")
    name = models.CharField(blank=True, null=True, max_length=30)
    delimiters = models.CharField(max_length=1, choices=DELIMITERS, default=",")
    quotes = models.CharField(max_length=1, choices=QUOTES, default='"')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return f"/schemas/?{self.pk}"

    def generate_fake_data(self, rows=5, uid=None):
        import csv

        print('INSIDE OF THE GEN FUNC of MODEL')

        csv.register_dialect(
            "custom",
            delimiter=self.delimiters,
            quotechar=self.quotes,
            quoting=csv.QUOTE_ALL,
        )

        fake_creator = Faker()

        def fake_data(field_type: int, val_range=(0, 100)):
            faker_methods = {
                0: fake_creator.name(),
                1: fake_creator.job(),
                2: fake_creator.safe_email(),
                3: fake_creator.paragraph(nb_sentences=val_range[1], variable_nb_sentences=False),
                4: fake_creator.random_int(*val_range),
                5: fake_creator.address(),
                6: fake_creator.date(),
            }
            return faker_methods[field_type]

        columns = self.schema_column.all().values()
        fieldnames = [el["name"] for el in columns]

        try:
            os.mkdir(settings.MEDIA_ROOT)
        except OSError:
            print("error creating output folder")

        with default_storage.open(settings.MEDIA_ROOT + f"/{uid}_dataScheme.csv", "w") as f:

            writer = csv.DictWriter(f, fieldnames=fieldnames, dialect="custom")
            writer.writeheader()

            for i in range(rows):
                row = {}
                for col in columns:

                    value = fake_data(col["field_type"])
                    if col["data_range_from"] and col["data_range_to"] and col["field_type"] in (6, 7):
                        value = fake_data(col["field_type"], val_range=(col["data_range_from"], col["data_range_to"]))

                    row[col["name"]] = value
                writer.writerow(row)

        return f"{settings.MEDIA_URL}{uid}_dataScheme.csv"


class FakeCSVSchemesInline(models.Model):
    FIELD_DROPDOWN_CHOICES = [
        (0, "Full Name"),
        (1, "Job"),
        (2, "Email"),
        (3, "Text"),
        (4, "Integer"),
        (5, "Address"),
        (6, "Date"),
    ]

    schema = models.ForeignKey(FakeCSVSchemes, on_delete=models.CASCADE, related_name="scheme_column")
    name = models.CharField(verbose_name="column name", blank=True, null=True, max_length=30)
    field_type = models.IntegerField(choices=FIELD_DROPDOWN_CHOICES, verbose_name="type")
    order = models.IntegerField(blank=True, default=0)
    data_range_from = models.IntegerField(blank=True, null=True, verbose_name="from")
    data_range_to = models.IntegerField(blank=True, null=True, verbose_name="to")


class ExportedDatascheme(models.Model):
    EXPORT_STATUS_CHOICES = [
        (0, "processing"),
        (1, "ready"),
        (2, "error"),
    ]
    schema = models.ForeignKey(FakeCSVSchemes, on_delete=models.SET_NULL, related_name="schemadatasets", null=True,
                               blank=True, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0, choices=EXPORT_STATUS_CHOICES)
    download_link = models.URLField(null=True, blank=True)
    task_id = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-created"]
