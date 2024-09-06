from djongo import models

class Patient(models.Model):
    prenom = models.CharField(max_length=100)
    mot_de_passe = models.CharField(max_length=100)

    def __str__(self):
        return self.prenom

