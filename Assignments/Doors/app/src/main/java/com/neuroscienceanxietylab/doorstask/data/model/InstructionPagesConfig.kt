package com.neuroscienceanxietylab.doorstask.data.model

import com.neuroscienceanxietylab.doorstask.R

object InstructionPagesConfig {
    /**
     * Centralized instruction content for easy copy/design updates.
     *
     * Source: instructions_english_door_2025_update.pptx (28 slides). Deck slide 26 was an empty
     * separator and is dropped, giving 27 app pages below, in deck order. Most pages are
     * full-bleed exports of their deck slide (via `slideImageRes`) because the deck composites
     * positioned text/callouts onto the artwork in ways the title/body model can't express
     * (e.g. coin labels pinned to specific door bars). The three pages that are cleanly a single
     * heading over one centered picture (deck slides 3-5) are kept as editable text instead.
     *
     * To update a flattened page: re-export that slide from the source deck as a PNG and replace
     * the matching `inst_en_NN.png` in res/drawable-nodpi/ (same filename, same slide number).
     */
    private val screenBackground = "#FDF6C8" // cream matte shared by the deck's artwork/text pages
    private val titleColor = "#3B2E13"
    private val bodyColor = "#2A2410"
    private val backButtonColor = "#8B6F3D"
    private val nextButtonColor = "#3D8B5A"

    val pages: List<InstructionPage> = listOf(
        // Deck slide 1
        InstructionPage(
            title = "Slide 01 (flattened)",
            body = "Baked into inst_en_01.png — edit by re-exporting slide 1 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_01
        ),
        // Deck slide 2
        InstructionPage(
            title = "Slide 02 (flattened)",
            body = "Baked into inst_en_02.png — edit by re-exporting slide 2 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_02
        ),
        // Deck slide 3 — coded: heading + centered fairy image
        InstructionPage(
            title = "The Fairies",
            body = "There are kind fairies in the castle, hiding behind some of the doors. They like to give coins to visitors who open their doors.",
            titleFontSizeSp = 26f,
            bodyFontSizeSp = 24f,
            textAlign = InstructionTextAlign.CENTER,
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            foregroundImageRes = R.drawable.inst_en_fairy,
            foregroundImageAlignment = InstructionImageAlignment.CENTER,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor
        ),
        // Deck slide 4 — coded: heading + centered monster image
        // Note: the deck bolds "some" and "take away"; InstructionPage.body is plain text, so
        // that emphasis is not reproduced here.
        InstructionPage(
            title = "The Monsters",
            body = "But, there are also grumpy monsters in the castle, hiding behind some of the doors. They like to steal coins from visitors who open their doors.",
            titleFontSizeSp = 26f,
            bodyFontSizeSp = 24f,
            textAlign = InstructionTextAlign.CENTER,
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            foregroundImageRes = R.drawable.inst_en_monster,
            foregroundImageAlignment = InstructionImageAlignment.CENTER,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor
        ),
        // Deck slide 5 — coded: heading + centered doors image
        InstructionPage(
            title = "Your Goal",
            body = "Your goal is to collect as many coins as possible, by going through the different rooms in the castle. The coins you collect will be transformed into money you'll get at the end of the experiment.",
            titleFontSizeSp = 26f,
            bodyFontSizeSp = 21f,
            textAlign = InstructionTextAlign.CENTER,
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            foregroundImageRes = R.drawable.inst_en_doors,
            foregroundImageAlignment = InstructionImageAlignment.CENTER,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor
        ),
        // Deck slide 6
        InstructionPage(
            title = "Slide 06 (flattened)",
            body = "Baked into inst_en_06.png — edit by re-exporting slide 6 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_06
        ),
        // Deck slide 7
        InstructionPage(
            title = "Slide 07 (flattened)",
            body = "Baked into inst_en_07.png — edit by re-exporting slide 7 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_07
        ),
        // Deck slide 8
        InstructionPage(
            title = "Slide 08 (flattened)",
            body = "Baked into inst_en_08.png — edit by re-exporting slide 8 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_08
        ),
        // Deck slide 9
        InstructionPage(
            title = "Slide 09 (flattened)",
            body = "Baked into inst_en_09.png — edit by re-exporting slide 9 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_09
        ),
        // Deck slide 10
        InstructionPage(
            title = "Slide 10 (flattened)",
            body = "Baked into inst_en_10.png — edit by re-exporting slide 10 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_10
        ),
        // Deck slide 11
        InstructionPage(
            title = "Slide 11 (flattened)",
            body = "Baked into inst_en_11.png — edit by re-exporting slide 11 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_11
        ),
        // Deck slide 12
        InstructionPage(
            title = "Slide 12 (flattened)",
            body = "Baked into inst_en_12.png — edit by re-exporting slide 12 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_12
        ),
        // Deck slide 13
        InstructionPage(
            title = "Slide 13 (flattened)",
            body = "Baked into inst_en_13.png — edit by re-exporting slide 13 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_13
        ),
        // Deck slide 14
        InstructionPage(
            title = "Slide 14 (flattened)",
            body = "Baked into inst_en_14.png — edit by re-exporting slide 14 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_14
        ),
        // Deck slide 15
        InstructionPage(
            title = "Slide 15 (flattened)",
            body = "Baked into inst_en_15.png — edit by re-exporting slide 15 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_15
        ),
        // Deck slide 16
        InstructionPage(
            title = "Slide 16 (flattened)",
            body = "Baked into inst_en_16.png — edit by re-exporting slide 16 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_16
        ),
        // Deck slide 17
        InstructionPage(
            title = "Slide 17 (flattened)",
            body = "Baked into inst_en_17.png — edit by re-exporting slide 17 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_17
        ),
        // Deck slide 18
        InstructionPage(
            title = "Slide 18 (flattened)",
            body = "Baked into inst_en_18.png — edit by re-exporting slide 18 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_18
        ),
        // Deck slide 19
        InstructionPage(
            title = "Slide 19 (flattened)",
            body = "Baked into inst_en_19.png — edit by re-exporting slide 19 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_19
        ),
        // Deck slide 20
        InstructionPage(
            title = "Slide 20 (flattened)",
            body = "Baked into inst_en_20.png — edit by re-exporting slide 20 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_20
        ),
        // Deck slide 21
        InstructionPage(
            title = "Slide 21 (flattened)",
            body = "Baked into inst_en_21.png — edit by re-exporting slide 21 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_21
        ),
        // Deck slide 22
        InstructionPage(
            title = "Slide 22 (flattened)",
            body = "Baked into inst_en_22.png — edit by re-exporting slide 22 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_22
        ),
        // Deck slide 23
        InstructionPage(
            title = "Slide 23 (flattened)",
            body = "Baked into inst_en_23.png — edit by re-exporting slide 23 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_23
        ),
        // Deck slide 24
        InstructionPage(
            title = "Slide 24 (flattened)",
            body = "Baked into inst_en_24.png — edit by re-exporting slide 24 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_24
        ),
        // Deck slide 25
        InstructionPage(
            title = "Slide 25 (flattened)",
            body = "Baked into inst_en_25.png — edit by re-exporting slide 25 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_25
        ),
        // Deck slide 26 was an empty separator — intentionally dropped.
        // Deck slide 27
        InstructionPage(
            title = "Slide 27 (flattened)",
            body = "Baked into inst_en_27.png — edit by re-exporting slide 27 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_27
        ),
        // Deck slide 28
        InstructionPage(
            title = "Slide 28 (flattened)",
            body = "Baked into inst_en_28.png — edit by re-exporting slide 28 from the source deck.",
            screenBackgroundColorHex = screenBackground,
            titleColorHex = titleColor,
            bodyColorHex = bodyColor,
            backButtonColorHex = backButtonColor,
            nextButtonColorHex = nextButtonColor,
            slideImageRes = R.drawable.inst_en_28
        )
    )
}
