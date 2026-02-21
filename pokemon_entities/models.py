from django.db import models

class Pokemon(models.Model):
   title = models.CharField(verbose_name='Название по русски',
                            max_length=200)
   title_en = models.CharField(verbose_name='Название по английски',
                               max_length=200,
                               blank=True)
   title_jp = models.CharField(verbose_name='НАзвание по японски',
                               max_length=200,
                               blank=True)
   photo = models.ImageField(verbose_name='Аватар',
                             upload_to='ava/',
                             null=True)
   description = models.TextField(verbose_name='Описание',
                                  blank=True)
   previous_evolution = models.ForeignKey('self',
                                           verbose_name='Из кого эволюционирует',
                                           null=True,
                                           blank=True,
                                           related_name='next_evolutions',
                                           on_delete=models.SET_NULL)
   def __str__(self):
       return self.title


class PokemonEntity(models.Model):
   pokemon = models.ForeignKey(Pokemon,
                               on_delete=models.CASCADE,
                               verbose_name='Покемон',
                               related_name = 'pokemon_entity')
   lat = models.FloatField(verbose_name='Широта')
   lon = models.FloatField(verbose_name='Долгота')
   appeared_at = models.DateTimeField(verbose_name='Активация')
   disappeared_at = models.DateTimeField(verbose_name='Дезактивация')
   level = models.IntegerField(verbose_name='Уровень',
                               null=True,
                               blank=True)
   health = models.IntegerField(verbose_name='Здоровье',
                                null=True,
                                blank=True)
   strength = models.IntegerField(verbose_name='Атака',
                                  null=True,
                                  blank=True)
   defence = models.IntegerField(verbose_name='Защита',
                                  null=True,
                                  blank=True)
   stamina = models.IntegerField(verbose_name='Выносливость',
                                  null=True,
                                  blank=True)
    
   def __str__(self):
       return self.pokemon.title





    
    
   
    
  