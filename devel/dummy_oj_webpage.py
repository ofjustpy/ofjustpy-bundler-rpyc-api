import ofjustpy as oj


from html_writer.macro_module import macros, writer_ctx
from py_tailwind_utils import *
app = oj.load_app()
adiv = oj.PD.Div(twsty_tags=[bg/green/100],
                 extra_classes="text-primary-300-700 "
          )

aspan = oj.PD.Span(text="Hello world",
                   extra_classes="text-primary-300-700 ")


twsty_tags =[space/y/4, gap/4, noop/placeholder, noop/animate_pulse, noop/placeholder_circle,]
print(tstr(*twsty_tags))

with writer_ctx:
    with Div(twsty_tags=[W/full, space/y/4]) as tlc:
        with Div(twsty_tags = [db.f, ai.center, jc.between]):
            with Div(twsty_tags=[noop/placeholder_circle, size/16, noop/animate_pulse
                                 ]
                     ):
                pass
            with Div(twsty_tags=[noop/placeholder_circle, size/16, noop/animate_pulse
                                 ]
                     ):
                pass
            with Div(twsty_tags=[noop/placeholder_circle, size/10, noop/animate_pulse
                                 ]
                     ):
                pass
            pass
        with Div(twsty_tags=[space/y/4]):
            with Div(twsty_tags=[noop/placeholder, noop/animate_pulse]):
                pass
        
            with StackG(num_cols=4, twsty_tags=[gap/4]):
                with Div(twsty_tags=[noop/placeholder, noop/animate_pulse]):
                    pass
                with Div(twsty_tags=[noop/placeholder, noop/animate_pulse]):
                    pass
                with Div(twsty_tags=[noop/placeholder, noop/animate_pulse]):
                    pass
                with Div(twsty_tags=[noop/placeholder, noop/animate_pulse]):
                    pass

            with Div(twsty_tags=[noop/placeholder, noop/animate_pulse]):
                pass
            with Div(twsty_tags=[noop/placeholder, noop/animate_pulse]):
                pass
            pass
        pass
    pass






        
endpoint = oj.create_endpoint("dummy_webpage",
                              childs = [tlc],
                              csr_bundle_dir="skeletonui_plus",
                              skeleton_data_theme="seafoam"                            
                              )


oj.add_jproute("/", endpoint)




        
# oj.PD.Div(twsty_tags=[W/full, space/y/4],
#           childs=[oj.PD.Div(twsty_tags=[db.f, ai.center, jc.between],
#                             childs = [
#                                 oj.PD.Div(twsty_tags=[placeholder_circle, size/16, animate_pulse]),
#                                 oj.PD.Div(twsty_tags=[placeholder_circle,
#                                                       size/14,
#                                                       animate_pulse
#                                                       ]),
#                                 oj.PD.Div(twsty_tags=[placeholder_circle,
#                                                       size/10, animate_pulse

#                                                       ]),
                                          

#                             ]

#                             )

# ]

#           )

# <div class="w-full space-y-4">
#   <div class="flex items-center justify-between">
#     <div class="flex items-center justify-center space-x-4">
#       <div class="placeholder-circle size-16 animate-pulse"></div>
#       <div class="placeholder-circle size-14 animate-pulse"></div>
#       <div class="placeholder-circle size-10 animate-pulse"></div>
#     </div>
#   </div>
# </div>
#   <div class="space-y-4">
#     <div class="placeholder animate-pulse"></div>
#     <div class="grid grid-cols-4 gap-4">
#       <div class="placeholder animate-pulse"></div>
#       <div class="placeholder animate-pulse"></div>
#       <div class="placeholder animate-pulse"></div>
#       <div class="placeholder animate-pulse"></div>
#     </div>
#     <div class="placeholder animate-pulse"></div>
#     <div class="placeholder animate-pulse"></div>
#   </div>
# </div>
