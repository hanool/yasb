# Language Widget Options
| Option           | Type     | Default                        | Description                                                                 |
|------------------|----------|--------------------------------|-----------------------------------------------------------------------------|
| `label`          | string   | `"{lang[language_code]}-{lang[country_code]}"`              | The format string for the label. |
| `label_alt`      | string   | `"{lang[full_name]}"`               | The alternative format string for the label. Useful for displaying the full language name. |
| `update_interval`| integer  | `5`                            | The interval in seconds to update the language information. Must be between 1 and 3600. |
| `class_name`      | string   | `""`                           | Additional CSS class name for the widget.                                    |
| `callbacks`      | dict     | `{ 'on_left': 'toggle_label', 'on_middle': 'do_nothing', 'on_right': 'do_nothing' }` | The dictionary of callback functions for different mouse actions. |
| `language_menu` | dict     | [See below](#language-menu-configuration) | Options for the language menu. |
| `label_maps` | dict | `{}` | Optional rules for creating custom `{mapped[...]}` label values from `lang` and `ime` data. |

## Callbacks
The `callbacks` option allows you to define custom actions for mouse events on the widget. The keys are:
- `on_left`: Action when the left mouse button is clicked.
- `on_middle`: Action when the middle mouse button is clicked.
- `on_right`: Action when the right mouse button is clicked.
- The values are the names of the callback functions that will be executed when the respective mouse button is clicked.
- `toggle_label`: A function to toggle the label between the main and alternative formats.
- `toggle_menu`: A function to toggle the visibility of the language selection menu.
- `do_nothing`: A placeholder function that does nothing when the mouse button is clicked.

## Language Menu Configuration
The `language_menu` option allows you to configure the popup menu for language selection. It accepts the following keys:

| Option              | Type     | Default      | Description                                                                 |
|---------------------|----------|--------------|-----------------------------------------------------------------------------|
| `blur`              | boolean  | `true`       | Enables a blur effect in the menu popup.                                    |
| `round_corners`     | boolean  | `true`       | If `true`, the menu has rounded corners.                                    |
| `round_corners_type`| string   | `"normal"`   | Determines the corner style; allowed values are `normal` and `small`.       |
| `border_color`      | string   | `"system"`   | Sets the border color for the menu. Can be `"system"`, `None` or HEX color. |
| `alignment`         | string   | `"right"`    | Horizontal alignment of the menu relative to the widget (`left`, `right`, `center`). |
| `direction`         | string   | `"down"`     | Direction in which the menu opens (`down` or `up`).                         |
| `offset_top`        | integer  | `6`          | Vertical offset for fine positioning of the menu.                           |
| `offset_left`       | integer  | `0`          | Horizontal offset for fine positioning of the menu.                         |
| `layout_icon`       | string   | `"\uf11c"`   | Icon displayed next to layout names in the menu.                            |
| `show_layout_icon`  | boolean  | `true`       | Whether to show the layout icon next to each language entry.                |

## Label Maps Configuration
The `label_maps` option allows you to create custom values for labels without hardcoding language-specific behavior in the widget. Each entry creates a value available as `{mapped[name]}` in `label` and `label_alt`.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `default` | string | `""` | Value used when no rule matches. Supports `{lang[...]}` and `{ime[...]}` placeholders. |
| `rules` | list | `[]` | Ordered list of rules. The first matching rule is used. |

The `ime` fields come from Windows Input Method Manager (IMM32) state. Values can vary by input method, and some fields may return `None` when the active input method does not provide a value.

Each rule accepts:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `match` | dict | `{}` | Fields to match under `lang` and `ime`. All fields must match. |
| `value` | string | Required | Value used when the rule matches. Supports `{lang[...]}` and `{ime[...]}` placeholders. |

Rules use exact equality. If two input states return the same `{ime[...]}` values, `label_maps` cannot distinguish them.

Example:

```yaml
label_maps:
  ime_indicator:
    default: "{lang[language_code]}"
    rules:
      - match:
          lang:
            language_code: "ja"
          ime:
            conversion_mode: 0
        value: "A"
      - match:
          lang:
            language_code: "ja"
          ime:
            cmode_native: true
            cmode_katakana: true
        value: "カ"
```

Then use `{mapped[ime_indicator]}` in `label` or `label_alt`.

## Example Configuration
```yaml
language:
  type: "yasb.language.LanguageWidget"
  options:
    label: "{lang[language_code]}-{lang[country_code]}"
    label_alt: "{lang[full_name]}"
    update_interval: 5
    callbacks:
      on_left: "toggle_menu"
      on_middle: "do_nothing"
      on_right: "toggle_label"
    language_menu:
      blur: true
      round_corners: true
      round_corners_type: "normal"
      border_color: "system"
      alignment: "right"
      direction: "down"
      offset_top: 6
      offset_left: 0
      show_layout_icon: true
      layout_icon: "\uf11c"
```

## Example IME Indicator Configuration
This example derives a compact indicator from Windows IMM32 input mode state. First use `label_alt` to inspect the values returned by your installed input method, then adjust `label_maps` rules to match those observed values.

```yaml
language:
  type: "yasb.language.LanguageWidget"
  options:
    label: "{mapped[ime_indicator]}"
    label_alt: "{lang[language_code]}-{lang[country_code]} open={ime[open]} conv={ime[conversion_mode]} sentence={ime[sentence_mode]} native={ime[cmode_native]} kata={ime[cmode_katakana]}"
    update_interval: 1
    label_maps:
      ime_indicator:
        default: "{lang[language_code]}"
        rules:
          # Replace these values with values observed from your input method.
          - match:
              lang:
                language_code: "ja"
              ime:
                conversion_mode: 0
            value: "A"
          - match:
              lang:
                language_code: "ja"
              ime:
                cmode_native: false
            value: "A"
          - match:
              lang:
                language_code: "ja"
              ime:
                cmode_native: true
                cmode_katakana: true
            value: "カ"
          - match:
              lang:
                language_code: "ja"
              ime:
                cmode_native: true
                cmode_katakana: false
            value: "あ"
```

Korean, Chinese, and other input methods can be configured the same way by matching the raw `{ime[...]}` values observed for that input method.

If your input method reports the same IMM32 values for two visible modes, those modes cannot be represented as different `{mapped[...]}` values with `label_maps` alone.

## Description of Options
- **label:** The format string for the label. You can use placeholders like `{lang[language_code]}`, `{lang[country_code]}`, `{lang[full_name]}`, `{lang[native_country_name]}`, `{lang[native_lang_name]}`, `{lang[layout_name]}`, `{lang[full_layout_name]}`, `{lang[layout_country_name]}`, `{lang[iso_language_code]}`, `{ime[open]}`, `{ime[conversion_mode]}`, and `{mapped[example]}`.
- **label_alt:** The alternative format string for the label. Useful for displaying the full language name.
- **update_interval:** The interval in seconds to update the language information. Must be between 1 and 3600.
- **class_name:** Additional CSS class name for the widget. This allows for custom styling.
- **callbacks:** A dictionary specifying the callbacks for mouse events. The keys are `on_left`, `on_middle`, and `on_right`, and the values are the names of the callback functions.
- **language_menu:** A dictionary containing options for the language selection menu. It includes options like `blur`, `round_corners`, `round_corners_type`, `border_color`, `alignment`, `direction`, `offset_top`, `offset_left`, `layout_icon`, and `show_layout_icon`.
- **label_maps:** A dictionary for creating custom `{mapped[...]}` values from `lang` and `ime` fields. This is useful for displaying IME indicators while keeping language-specific rules in user configuration.

## Available IME Placeholders
The `ime` namespace exposes raw Windows IMM32 input mode state. YASB does not interpret these values as Japanese, Korean, Chinese, or vendor-specific modes.

| Placeholder | Type | Description |
|-------------|------|-------------|
| `{ime[available]}` | boolean | Whether IMM32 returned at least one input mode value. |
| `{ime[open]}` | boolean or `None` | Raw IME open status. |
| `{ime[conversion_mode]}` | integer or `None` | Raw IME conversion mode. |
| `{ime[sentence_mode]}` | integer or `None` | Raw IME sentence mode. |
| `{ime[cmode_native]}` | boolean or `None` | Whether `IME_CMODE_NATIVE` is set. |
| `{ime[cmode_katakana]}` | boolean or `None` | Whether `IME_CMODE_KATAKANA` is set. |
| `{ime[cmode_fullshape]}` | boolean or `None` | Whether `IME_CMODE_FULLSHAPE` is set. |
| `{ime[cmode_roman]}` | boolean or `None` | Whether `IME_CMODE_ROMAN` is set. |
| `{ime[cmode_charcode]}` | boolean or `None` | Whether `IME_CMODE_CHARCODE` is set. |
| `{ime[cmode_hanjaconvert]}` | boolean or `None` | Whether `IME_CMODE_HANJACONVERT` is set. |
| `{ime[cmode_softkbd]}` | boolean or `None` | Whether `IME_CMODE_SOFTKBD` is set. |
| `{ime[cmode_noconversion]}` | boolean or `None` | Whether `IME_CMODE_NOCONVERSION` is set. |
| `{ime[cmode_eudc]}` | boolean or `None` | Whether `IME_CMODE_EUDC` is set. |
| `{ime[cmode_symbol]}` | boolean or `None` | Whether `IME_CMODE_SYMBOL` is set. |
| `{ime[cmode_fixed]}` | boolean or `None` | Whether `IME_CMODE_FIXED` is set. |

## Example Style
```css
.language-widget {}
.language-widget.your_class {} /* If you are using class_name option */
.language-widget .widget-container {}
.language-widget .widget-container.caps-lock-on {} /* If Caps Lock is on */
.language-widget .label {}
.language-widget .label.alt {}
.language-widget .icon {}
.language-widget .widget-container.caps-lock-on .label {} /* If Caps Lock is on */
.language-widget .widget-container.caps-lock-on .icon {} /* If Caps Lock is on */

/* Language Menu */
.language-menu {}
.language-menu .header {}
.language-menu .footer {}
.language-menu .language-item {}
.language-menu .language-item.active {}
.language-menu .language-item .code {}
.language-menu .language-item .icon {}
.language-menu .language-item .name {}
.language-menu .language-item .layout {}

```

## Example Style for Menu
```css
.language-menu {
    background-color: rgba(17, 17, 27, 0.4);
    min-width: 300px;
}
.language-menu .header {
    font-family: 'Segoe UI';
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 2px;
    padding: 12px;
    background-color: rgba(17, 17, 27, 0.6);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.language-menu .footer {
    font-family: 'Segoe UI';
    font-size: 12px;
    font-weight: 600;
    padding: 12px;
    margin-top: 2px;
    color: #9399b2;
    background-color: rgba(17, 17, 27, 0.6);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}
.language-menu .footer:hover {
    background-color: rgba(36, 36, 51, 0.6);
    color: #fff;
}
.language-menu .language-item {
    padding: 6px 12px;
    margin: 2px 4px;
}
.language-menu .language-item.active {
    background-color:rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}
.language-menu .language-item:hover {
    background-color: rgba(255, 255, 255, 0.05);
}
.language-menu .language-item.active:hover {
    background-color:rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}
.language-menu .language-item .code {
    font-weight: 900;
    font-size: 14px;
    min-width: 40px;
    text-transform: uppercase;
}
.language-menu .language-item .icon {
    font-size: 16px;
    margin-right: 8px;
    color: #fff;
}
.language-menu .language-item .name {
    font-weight: 600;
    font-family: 'Segoe UI';
    font-size: 14px;
}
.language-menu .language-item .layout {
    font-weight: 600;
    font-family: 'Segoe UI';
    font-size: 12px;
}
```

## Preview of the Widget
![Language YASB Widget](assets/6b646834-fc98abfe-b297-ce61-4bce3683223c.png)
