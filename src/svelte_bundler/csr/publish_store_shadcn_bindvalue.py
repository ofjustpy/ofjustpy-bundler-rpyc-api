from string import Template
from ..config import (hostname,
                     port,
                     username,
                     csr_bundle_style_css_dir as remote_svelte_bundle_dir 
                     )

from ..helper_utils import write_to_bundler_dir


def publish_store_shadcn_bindvalue():
    store_shadcn_bindvalue_str = """
import { writable } from 'svelte/store';
 import { getLocalTimeZone, today } from "@internationalized/date";
type ComponentValueState = {
  [key: string]: any;
};

const initialValues: ComponentValueState = {
 '/volume_slider': [50],
 '/appointment_calendar': today(getLocalTimeZone())
};

export const componentValues = writable<ComponentValueState>(initialValues);
    """

    
    write_to_bundler_dir(store_shadcn_bindvalue_str, "src/store_shadcn_bindvalue.ts",
                         target_bundler_dir = remote_svelte_bundle_dir
                         )
