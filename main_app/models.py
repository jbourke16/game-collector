from django.db import models

# Create your models here.

STUDIOS = (
    ('EA', 'Electronic Arts'),
    ('SQ', 'Square Enix'),
    ('ND', 'Naughty Dog'),
    ('NIN', 'Nintendo'),
    ('LS', 'Larian Studios'),
    ('PS', 'PlayStation'),
    ('BGS', 'Bethseda Game Studios'),
    ('CAP', 'Capcom'),
    ('CD', 'Crystal Dynamics'),
    ('EG', 'Epic Games'),
    ('GG', 'Guerrilla Games'),
    ('RIO', 'Riot Games'),
    ('RG', 'Rockstar Games'),
    ('SE', 'SEGA'),
    ('V', 'Valve')
)
class Game(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.title

class Developer(models.Model):
    date = models.DateField('Relase Date')
    studio = models.CharField(
        max_length=100,
        choices=STUDIOS,
        default=STUDIOS[0][0]
        )
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.get_studio_display()} on {self.date}'
    
    class Meta:
        ordering = ['-date']