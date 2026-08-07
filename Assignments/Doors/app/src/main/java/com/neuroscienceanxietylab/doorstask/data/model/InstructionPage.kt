package com.neuroscienceanxietylab.doorstask.data.model

enum class InstructionFontFamily {
    DEFAULT,
    SERIF,
    MONOSPACE
}

enum class InstructionTextAlign {
    START,
    CENTER,
    END
}

enum class InstructionImageAlignment {
    TOP_START,
    TOP_CENTER,
    TOP_END,
    CENTER,
    BOTTOM_START,
    BOTTOM_CENTER,
    BOTTOM_END
}

data class InstructionPage(
    val title: String,
    val body: String,
    val titleFontSizeSp: Float = 30f,
    val bodyFontSizeSp: Float = 20f,
    val fontFamily: InstructionFontFamily = InstructionFontFamily.DEFAULT,
    val textAlign: InstructionTextAlign = InstructionTextAlign.CENTER,
    val screenBackgroundColorHex: String = "#101A2A",
    val titleColorHex: String = "#FFFFFF",
    val bodyColorHex: String = "#F2F4F8",
    val foregroundImageRes: Int? = null,
    val foregroundImageAlignment: InstructionImageAlignment = InstructionImageAlignment.CENTER,
    val backgroundImageRes: Int? = null,
    val backButtonColorHex: String = "#2E5B8C",
    val nextButtonColorHex: String = "#1C8E57",
    val buttonTextColorHex: String = "#FFFFFF",
    /**
     * When set, this page renders as a single full-bleed exported slide image instead of the
     * title/body/foreground layout. Used for instruction pages composed of positioned text and
     * images that don't map onto the fields above (e.g. coin-bar callouts baked into the art).
     * Title/body/foreground fields are ignored when this is non-null.
     */
    val slideImageRes: Int? = null
)
