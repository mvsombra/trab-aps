from flask import render_template


class DesenhaTela:
    def render(self, page, *args):
        if(page == 'index'):
            return render_template('index.html')
