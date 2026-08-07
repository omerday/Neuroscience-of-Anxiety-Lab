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

enum class InstructionOverlayType {
    TEXT,
    IMAGE
}

/**
 * One positioned element (text or image) on an overlay-based InstructionPage. Position and size
 * are fractions (0f-1f) of the page's full width/height, matching how the source deck's slide
 * XML expresses shape geometry, so a page can be laid out by copying its shapes' fractional
 * bounding boxes directly.
 */
data class InstructionOverlay(
    val type: InstructionOverlayType,
    val xFraction: Float,
    val yFraction: Float,
    val widthFraction: Float,
    val heightFraction: Float,
    val text: String? = null,
    val imageRes: Int? = null,
    val fontSizeSp: Float = 24f,
    val bold: Boolean = false,
    val colorHex: String = "#1A1A1A",
    val textAlign: InstructionTextAlign = InstructionTextAlign.CENTER
)

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
     * title/body/foreground layout. Kept for potential future use; no current page sets it, since
     * every page's text is now real, separate text rather than baked into a picture.
     */
    val slideImageRes: Int? = null,
    /**
     * When non-empty, this page renders as a set of independently positioned text and image
     * elements instead of the title/body/foreground layout, so pages that combine several images
     * with positioned captions (e.g. a coin-count label pinned beside a specific door bar) can be
     * expressed with real text and real images rather than a single flattened picture.
     */
    val overlays: List<InstructionOverlay> = emptyList()
)
