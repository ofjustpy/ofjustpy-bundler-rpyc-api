import shadcnui_components
from py_tailwind_utils import *
from shadcnui_components.components import Card, Button,Label, Input, Select
abtn = shadcnui_components.components.Button(key="button1",
                 text="Button",
                 variant="outline",
                 href="#",
                 twsty_tags=[bg/blue/100])


select = shadcnui_components.components.Select(key="select")
item1 = select.Item(value="sveltekit", label="Sveltekit", text="Sveltekit")
item2  = select.Item(value="next", label="Next.js", text="Next.js")
item3 = select.Item(value="nuxt", label="Nuxt.js", text="Nuxt.js")

select.components.append(item1)
#select.set_slot_content(item1, item2, item3)

