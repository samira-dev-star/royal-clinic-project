from django.apps import AppConfig


class CommentsScoresFavouritesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.comments_scores_favourites'
    
    verbose_name = 'نظر و سوالات'
    verbose_name_plural = 'نظرات و سوالات'
