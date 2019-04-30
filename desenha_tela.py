from flask import render_template


class DesenhaTela:
    def render(self, page, *args):
        page = page + '.html'
        if(len(args) > 0):
            pass
        return render_template(page)
