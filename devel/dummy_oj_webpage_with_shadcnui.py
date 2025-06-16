import ofjustpy as oj
from shadcnui_components.components import Button
from py_tailwind_utils import *
from html_writer.macro_module import macros, writer_ctx
badge_vf = oj.PC.Span(text="Badge", extra_classes= "badge preset-filled")
button1 = Button(key="button1",
                 text="Button",
                 variant="outline",
                 href="#",
                 twsty_tags=[bg/blue/100]
                 )

variant_type = "filled"
pshdn= "-primary"
btn_icon = oj.AD.Button(key="ibtn",
                        childs = [# oj.icons.FontAwesomeIcon(label="faSkull",
                                  #                          size="2x", 
                                  #                          fixedWidth=True,
                                  #                          )
                                  ],
                        type="button", 
                        extra_classes=f"btn-icon preset-icon"
                        )

app = oj.load_app()
endpoint = oj.create_endpoint("dummy_webpage",
                              childs = [button1, badge_vf, btn_icon],
                              csr_bundle_dir="oj_browser_bits",
                              skeleton_data_theme="seafoam"                                              )
oj.add_jproute("/", endpoint)
