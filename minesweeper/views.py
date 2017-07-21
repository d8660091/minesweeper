from django.views import generic


class GameView(generic.TemplateView):
    template_name = 'minesweeper/game.dtl'
