import webapp2
from webapp2_extras import jinja2

import model.user as usr_mgt
from model.appinfo import AppInfo


class Error_Manager(webapp2.RequestHandler):
    def get(self):
        try:
            msg = self.request.GET['msg']
        except KeyError:
            msg = None
        if not msg:
            msg = "CRITICAL - contact development team"
        try:
            redirect = self.request.GET['redirect']
        except KeyError:
            redirect = None
        if not redirect:
            redirect = "/books"

        template_values = {
            "usr_info": usr_mgt.create_empty_user(),
            "error_msg": msg,
            "info": AppInfo,
            "redirect": redirect
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("error_page.html", **template_values));


app = webapp2.WSGIApplication([
    ("/error", Error_Manager),
], debug=True)
