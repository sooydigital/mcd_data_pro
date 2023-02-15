from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from tzlocal import get_localzone
from datetime import datetime
from dateutil import relativedelta as rdelta


# Create your models here.
class Departamento(models.Model):
    name = models.CharField(
        max_length=1024,
        verbose_name="nombre del departamento"
    )
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Departamento, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class Municipio(models.Model):
    departamento = models.ForeignKey(
        Departamento,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=1024,
        verbose_name="nombre del municipio"
    )
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Municipio, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class Barrio(models.Model):
    municipio = models.ForeignKey(
        Municipio,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=1024,
        verbose_name="nombre del barrio"
    )
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Barrio, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class PuestoVotacion(models.Model):
    departamento = models.ForeignKey(
        Departamento,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    municipio = models.ForeignKey(
        Municipio,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    barrio = models.ForeignKey(
        Barrio,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=1024,
        verbose_name="Nombre Puesto de Votación",
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=1024,
        verbose_name="Dirección",
        blank=True,
        null=True,
    )
    longitude = models.CharField(
        max_length=1024,
        verbose_name="longitude"
    )
    latitude = models.CharField(
        max_length=1024,
        verbose_name="latitude"
    )

    def __str__(self):
        return '{}, {}, {}'.format(self.name, self.barrio, self.municipio)

class CustomUser(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    document_id = models.CharField(
        max_length=20,
        verbose_name="document id"
    )
    code = models.CharField(
        max_length=10,
        verbose_name="Code"
    )
    super_visor = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    municipio = models.ForeignKey(
        Municipio,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def full_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class Votante(models.Model):
    document_id = models.CharField(
        max_length=20,
        verbose_name="Cedula",
        unique=True
    )

    STATUS_CHOICES = [
        ("PENDING", "PENDING"),
        ("PROCESSED", "PROCESSED"),
        ("ERROR", "ERROR"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )

    custom_user = models.ForeignKey(
        CustomUser,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.document_id)

    def full_name(self):
        profile = self.votanteprofile_set.first()
        if profile:
            return '{} {}'.format(profile.first_name, profile.last_name)
        return ''


class VotanteProfile(models.Model):
    votante = models.ForeignKey(
        Votante,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name="Nombre Votante"
    )

    last_name = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name="Apellido Votante"
    )

    email = models.CharField(
        max_length=1024,
        verbose_name="Email",
        blank=True,
        null=True,
    )

    mobile_phone = models.CharField(
        max_length=1024,
        verbose_name="Celular",
        blank=True,
        null=True,
    )

    birthday = models.DateField()

    GENDER_CHOICES = [
        ("HOMBRE", "HOMBRE"),
        ("MUJER", "MUJER"),
    ]

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )

    address = models.CharField(
        max_length=1024,
        verbose_name="Direccion",
        blank=True,
        null=True,
    )

    municipio = models.ForeignKey(
        Municipio,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    barrio = models.ForeignKey(
        Barrio,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def age(self):
        local_tz = get_localzone()
        now = datetime.now(local_tz).date()
        birthday = self.birthday
        rd = rdelta.relativedelta(now, birthday)
        return rd.years

    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class VotantePuestoVotacion(models.Model):
    votante = models.ForeignKey(
        Votante,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    mesa = models.CharField(
        max_length=1024,
        verbose_name="Mesa",
        blank=True,
        null=True,
    )

    puesto_votacion = models.ForeignKey(
        PuestoVotacion,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )


class VotanteMessage(models.Model):
    votante = models.ForeignKey(
        Votante,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    message = models.CharField(
        max_length=1024,
        verbose_name="message",
        blank=True,
        null=True,
    )