import ofjustpy as oj
import shadcnui_components
from py_tailwind_utils import *
from html_writer.macro_module import macros, writer_ctx


button1 = shadcnui_components.components.Button(key="button1",
                 text="Button",
                 variant="outline",
                 href="#",
                 twsty_tags=[bg/blue/100])


select = shadcnui_components.components.Select(key="select")
item1 = select.Item(value="sveltekit", label="Sveltekit", text="Sveltekit")
item2  = select.Item(value="next", label="Next.js", text="Next.js")
item3 = select.Item(value="nuxt", label="Nuxt.js", text="Nuxt.js")

select.components.append(item1)

badge_vf = oj.PC.Span(text="Badge", extra_classes= "badge preset-filled")

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
                              csr_bundle_dir="skeleton_shadcn_uibundle",
                              skeleton_data_theme="seafoam"                                              )
oj.add_jproute("/", endpoint)
