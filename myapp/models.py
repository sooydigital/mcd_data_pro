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

    longitude = models.CharField(
        max_length=1024,
        verbose_name="longitude",
        blank=True,
        null=True,

    )
    latitude = models.CharField(
        max_length=1024,
        verbose_name="latitude",
        blank=True,
        null=True,
    )
    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Municipio, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class Comuna(models.Model):
    municipio = models.ForeignKey(
        Municipio,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    number = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=1024,
        verbose_name="nombre de la comuna"
    )
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Comuna, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class Barrio(models.Model):
    municipio = models.ForeignKey(
        Municipio,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    comuna = models.ForeignKey(
        Comuna,
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

    # barrio = models.ForeignKey(
    #     Barrio,
    #     blank=True,
    #     null=True,
    #     on_delete=models.CASCADE
    # )
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
    latitude = models.CharField(
        max_length=1024,
        verbose_name="latitude",
        blank=True,
        null=True,
    )
    longitude = models.CharField(
        max_length=1024,
        verbose_name="longitude",
        blank=True,
        null=True,

    )

    def __str__(self):
        return '{} -- {} -- {}'.format(self.name, self.address, self.municipio)


class IntecionDeVoto(models.Model):
    puesto_votacion = models.ForeignKey(
        PuestoVotacion,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    intencion_de_voto = models.PositiveIntegerField()

    def __str__(self):
        return '{} - {} #{}'.format(self.puesto_votacion.municipio.name, self.puesto_votacion.name, self.intencion_de_voto)


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
        if self.user.last_name:
            return '{} {}'.format(self.user.first_name, self.user.last_name)
        return '{}'.format(self.user.first_name)


class Votante(models.Model):
    document_id = models.CharField(
        max_length=20,
        verbose_name="Cedula",
        unique=True
    )
    TYPE_VOTANTE = [
        ("VOTANTE", "VOTANTE"),
        ("LIDER", "LIDER"),
        ("DINAMIZADOR", "DINAMIZADOR"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "PENDING"),
        ("PROCESSED", "PROCESSED"),
        ("ERROR", "ERROR"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )
    type = models.CharField(
        max_length=12,
        choices=TYPE_VOTANTE,
        default="VOTANTE"
    )
    num_referidos = models.IntegerField(
        default=0
    )

    custom_user = models.ForeignKey(
        CustomUser,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='supervisor'
    )

    # coordinador = models.ForeignKey(
    #     "self",
    #     related_name='Coordinador',
    #     blank=True,
    #     null=True,
    #     on_delete=models.CASCADE,
    # )

    lider = models.ForeignKey(
        "self",
        related_name='Leader',
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
            if profile.last_name:
                return '{} {}'.format(profile.first_name, profile.last_name)
            return '{}'.format(profile.first_name)
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

    birthday = models.DateField(
        blank=True,
        null=True,
    )

    GENDER_CHOICES = [
        ("MASCULINO", "MASCULINO"),
        ("FEMENINO", "FEMENINO"),
        ("OTRO", "OTRO"),
    ]

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )

    address = models.CharField(
        max_length=1024,
        verbose_name="Direccion",
        blank=True,
        null=True,
    )

    latitude = models.CharField(
        max_length=1024,
        verbose_name="latitude",
        blank=True,
        null=True,
    )

    longitude = models.CharField(
        max_length=1024,
        verbose_name="longitude",
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
        if self.birthday:
            local_tz = get_localzone()
            now = datetime.now(local_tz).date()
            birthday = self.birthday
            rd = rdelta.relativedelta(now, birthday)
            return rd.years
        return ""

    def full_name(self):
        if self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return '{}'.format(self.first_name)


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

class Etiqueta(models.Model):
    name = models.CharField(
        max_length=1024,
        verbose_name="nombre de la etiqueta"
    )
    def __str__(self):
        return '{}'.format(self.name)


class EtiquetaVotante(models.Model):
    votante = models.ForeignKey(
        Votante,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    etiqueta = models.ForeignKey(
        Etiqueta,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.etiqueta and self.votante:
            return '{} - {} #{}'.format(self.votante.document_id, self.etiqueta.name, self.is_active)
        return '{} - {} #{}'.format(self.votante, self.etiqueta, self.is_active )


class CustomLink(models.Model):
    votante = models.ForeignKey(
        Votante,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    sub_link = models.CharField(
        max_length=1024,
        verbose_name="enlace personalizado"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {} #{}'.format(self.votante.document_id, self.sub_link, self.is_active)

class Campaign(models.Model):
    name = models.CharField(
        max_length=1024,
        verbose_name="nombre de la campaña"
    )

    url = models.CharField(
        max_length=1024,
        verbose_name="sub url de la campaña"
    )

    is_active = models.BooleanField(default=True)

    color_principal = models.CharField(
        max_length=10,
        verbose_name="principal_color"
    )
    color_secondary = models.CharField(
        max_length=10,
        verbose_name="principal_color"
    )

    longitude_principal = models.CharField(
        max_length=1024,
        verbose_name="longitude",
        blank=True,
        null=True,

    )
    latitude_principal = models.CharField(
        max_length=1024,
        verbose_name="latitude",
        blank=True,
        null=True,
    )

    municipios = models.ManyToManyField(Municipio)

    def __str__(self):
        return '{} - {}'.format(self.name, self.is_active)
