from flask import render_template


class DesenhaTela:
    def render(self, page, *args):
        page = page + '.html'
        if(len(args) > 0):
            return render_template(page, args=args)
        return render_template(page)
