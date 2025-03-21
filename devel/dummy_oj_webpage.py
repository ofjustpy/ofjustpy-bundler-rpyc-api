import ofjustpy as oj

from py_tailwind_utils import *
app = oj.load_app()
adiv = oj.PD.Div(twsty_tags=[bg/green/100],
                 extra_classes="text-primary-300-700 "
          )

aspan = oj.PD.Span(text="Hello world",
                   extra_classes="text-primary-300-700 ")
endpoint = oj.create_endpoint("dummy_webpage",
                              childs = [aspan],
                              csr_bundle_dir="skeletonui_plus",
                              )


oj.add_jproute("/", endpoint)
