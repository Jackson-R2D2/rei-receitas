from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timesince

# Create your models here.

class Topic(models.Model):
    name_topic = models.CharField(max_length=50)


    def __str__(self):
        return str(self.name_topic)


class Revenue(models.Model):
    name_revenue = models.CharField(max_length=100, verbose_name='Nome da receita')
    ingredients = models.TextField(verbose_name='Ingredientes')
    preparation_mode = models.TextField(verbose_name='Modo de preparo')
    host = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    revenue_image = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name='Passe uma imagem ou foto para esta receita', default='images/image_notfound.jpg')
    like = models.ManyToManyField(get_user_model(), related_name='like')

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


    def __str__(self):
        return str(self.name_revenue)


    def ingredients_format(self):
        # Formatar o campo 'ingredients' para separar cada ingrediente em uma string
        stringIngredient = ''
        listIngredients = []
        for positionString in range(0, len(self.ingredients)):
            if self.ingredients[positionString].isnumeric():
                if self.ingredients[positionString+1].isnumeric():
                    stringIngredient += self.ingredients[positionString]
                else:
                    stringIngredient += self.ingredients[positionString]
                    for otherLetters in range(positionString+1, len(self.ingredients)):
                        if self.ingredients[otherLetters].isnumeric():
                            if self.ingredients[positionString+1] == '/' or self.ingredients[otherLetters+1] == '/':
                                break
                            else:
                                listIngredients.append(stringIngredient)
                                stringIngredient = ''
                                break
                        stringIngredient += self.ingredients[otherLetters]
            elif positionString == len(self.ingredients)-1:
                listIngredients.append(stringIngredient)
        return listIngredients


    def yield_ingredients(self):
        for ingredient in self.ingredients_format():
            yield ingredient


    def total_likes(self):
        return self.like.count()


class Message(models.Model):
    host = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    revenue = models.ForeignKey(Revenue, on_delete=models.CASCADE, default='')
    textMessage  = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


    def __str__(self):
        return str(self.textMessage)