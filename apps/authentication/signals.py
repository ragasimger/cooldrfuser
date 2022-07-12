from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.db import models
from apps.authentication.models import User
from apps.authentication.staticstuffs import default_image


@receiver(post_delete, sender=User)
def delete_on_instance_delete(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.ImageField):
            field_name = getattr(instance, field.name)
            delete_image_if_unused(sender, instance, field, field_name)


@receiver(pre_save, sender=User)
def delete_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:

        if isinstance(field, models.ImageField):
            try:
                db_instance = sender.objects.get(pk=instance.pk)

            except sender.DoesNotExist:
                return

            db_instance_field_name = getattr(db_instance, field.name)
            instance_image_field_name = getattr(instance, field.name)

            if db_instance_field_name != instance_image_field_name:
                '''
                    Call image delete function if uploaded image doesn't match the name of corresponding instance.
                '''
                delete_image_if_unused(
                    sender, instance, field, db_instance_field_name)

            if instance_image_field_name.name == "":
                '''
                    Set the default image when the user deletes their profile image.
                '''
                setattr(instance, field.name, default_image)


def delete_image_if_unused(model, instance, field, instance_file_field):
    field_dict = {field.name: instance_file_field.name}
    instance_exist = model.objects.filter(
        **field_dict).exclude(pk=instance.pk).exists()
    '''
        Prevents signal to delete the default image file. Delete others if unused by any instance.
    '''
    if not instance_exist and instance_file_field.name != default_image:
        instance_file_field.delete(False)
