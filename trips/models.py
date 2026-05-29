from django.db import models


# Create your models here.
class Travel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def check_status(self):
        places = self.places.all()
        if places.exists() and all(p.is_visited for p in places):
            self.is_completed = True
        else:
            self.is_completed = False
        self.save(update_fields=["is_completed"])


class Place(models.Model):
    travel = models.ForeignKey(Travel, related_name="places", on_delete=models.CASCADE)
    external_id = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    is_visited = models.BooleanField(default=False)

    class Meta:
        unique_together = ("travel", "external_id")

    def __str__(self):
        return f"Place {self.external_id} for Travel {self.travel.name}"
