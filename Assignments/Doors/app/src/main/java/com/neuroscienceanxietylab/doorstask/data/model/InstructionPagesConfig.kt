package com.neuroscienceanxietylab.doorstask.data.model

import com.neuroscienceanxietylab.doorstask.R

object InstructionPagesConfig {
    /**
     * Centralized instruction content for easy copy/design updates.
     *
     * Source: instructions_english_door_2025_update.pptx (28 slides). Every page's text is real,
     * separate text (either the title/body fields, or an InstructionOverlay of type TEXT) and
     * every picture is a distinct image asset with no text baked into its pixels — no page uses
     * slideImageRes anymore.
     *
     * Pages composed of multiple positioned images and captions (e.g. a coin-count label pinned
     * beside a specific door bar) use `overlays`: a list of InstructionOverlay entries, each with
     * a fractional (0f-1f) position/size copied directly from the source slide's shape geometry.
     * Pages that are cleanly one heading over one centered picture use the plain title/body/
     * foregroundImageRes fields instead.
     *
     * Eight of the deck's 28 slides are intentionally not represented here:
     * - Slide 26 is an empty separator.
     * - Slides 11-15 and 18 describe desktop mouse-click/spacebar controls ("Left click to get
     *   closer", "hit the SPACEBAR to lock in", "magic mouse... secondary click") from an older,
     *   non-touch version of this task. They do not match this app's touch/slider interaction and
     *   were left out rather than shipped as incorrect instructions. Slide 20's mouse-drag icon
     *   was dropped for the same reason, but its text was kept (see "Review: Getting Closer" below)
     *   since the underlying statement ("the closer you get, the more likely it opens") still holds.
     * - Slide 25 ("Press 'r' to repeat") is obsolete: this app already has its own Repeat
     *   Instructions button on the opening screen.
     * If the app is ever extended to a desktop/mouse input mode, slides 11-15 and 18 are the ones
     * to revisit.
     */
    private const val BG = "#FDF6C8"       // cream matte shared by the deck's artwork/text pages
    private const val TITLE_COLOR = "#3B2E13"
    private const val BODY_COLOR = "#2A2410"
    private const val BACK_BTN = "#8B6F3D"
    private const val NEXT_BTN = "#3D8B5A"

    private fun textOverlay(
        x: Float, y: Float, w: Float, h: Float,
        text: String,
        sizeSp: Float = 24f,
        bold: Boolean = false,
        colorHex: String = BODY_COLOR,
        align: InstructionTextAlign = InstructionTextAlign.CENTER
    ) = InstructionOverlay(
        type = InstructionOverlayType.TEXT,
        xFraction = x, yFraction = y, widthFraction = w, heightFraction = h,
        text = text, fontSizeSp = sizeSp, bold = bold, colorHex = colorHex, textAlign = align
    )

    private fun imageOverlay(x: Float, y: Float, w: Float, h: Float, res: Int) = InstructionOverlay(
        type = InstructionOverlayType.IMAGE,
        xFraction = x, yFraction = y, widthFraction = w, heightFraction = h,
        imageRes = res
    )

    val pages: List<InstructionPage> = listOf(
        // Deck slide 1
        InstructionPage(
            title = "Castle Intro",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                imageOverlay(0f, 0f, 1f, 1f, R.drawable.inst_castle),
                textOverlay(
                    0.04f, 0.09f, 0.5f, 0.2f,
                    "You find yourself in a magic castle...",
                    sizeSp = 30f, align = InstructionTextAlign.START
                )
            )
        ),
        // Deck slide 2 (text was baked into the slide's picture in the source deck; reproduced
        // here as real text over a cropped, caption-free version of the same illustration)
        InstructionPage(
            title = "Coins in the Castle",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.06f, 0.05f, 0.88f, 0.16f, "There are many coins hiding behind the castle's many doors.", sizeSp = 26f),
                imageOverlay(0.30f, 0.24f, 0.40f, 0.46f, R.drawable.inst_room),
                textOverlay(0.06f, 0.76f, 0.88f, 0.16f, "Some rooms have few coins. Some have many.", sizeSp = 26f)
            )
        ),
        // Deck slide 3 — unchanged
        InstructionPage(
            title = "The Fairies",
            body = "There are kind fairies in the castle, hiding behind some of the doors. They like to give coins to visitors who open their doors.",
            titleFontSizeSp = 26f,
            bodyFontSizeSp = 24f,
            textAlign = InstructionTextAlign.CENTER,
            screenBackgroundColorHex = BG,
            titleColorHex = TITLE_COLOR,
            bodyColorHex = BODY_COLOR,
            foregroundImageRes = R.drawable.inst_en_fairy,
            foregroundImageAlignment = InstructionImageAlignment.CENTER,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN
        ),
        // Deck slide 4 — unchanged
        // Note: the deck bolds "some" and "take away"; InstructionPage.body is plain text, so
        // that emphasis is not reproduced here.
        InstructionPage(
            title = "The Monsters",
            body = "But, there are also grumpy monsters in the castle, hiding behind some of the doors. They like to steal coins from visitors who open their doors.",
            titleFontSizeSp = 26f,
            bodyFontSizeSp = 24f,
            textAlign = InstructionTextAlign.CENTER,
            screenBackgroundColorHex = BG,
            titleColorHex = TITLE_COLOR,
            bodyColorHex = BODY_COLOR,
            foregroundImageRes = R.drawable.inst_en_monster,
            foregroundImageAlignment = InstructionImageAlignment.CENTER,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN
        ),
        // Deck slide 5 — unchanged
        InstructionPage(
            title = "Your Goal",
            body = "Your goal is to collect as many coins as possible, by going through the different rooms in the castle. The coins you collect will be transformed into money you'll get at the end of the experiment.",
            titleFontSizeSp = 26f,
            bodyFontSizeSp = 21f,
            textAlign = InstructionTextAlign.CENTER,
            screenBackgroundColorHex = BG,
            titleColorHex = TITLE_COLOR,
            bodyColorHex = BODY_COLOR,
            foregroundImageRes = R.drawable.inst_en_doors,
            foregroundImageAlignment = InstructionImageAlignment.CENTER,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN
        ),
        // Deck slide 6
        InstructionPage(
            title = "Fairy or Monster",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.02f, 0.02f, 0.96f, 0.42f, "Behind each door, there is either a fairy, or a monster.\nHalf of the time, it will be a fairy.\nHalf of the time, it will be a monster.\nYou won't know which until you open the door.", sizeSp = 24f),
                imageOverlay(0.10f, 0.49f, 0.65f, 0.48f, R.drawable.inst_fairy_monster_scene),
                imageOverlay(0.76f, 0.49f, 0.22f, 0.33f, R.drawable.inst_en_fairy)
            )
        ),
        // Deck slide 7
        InstructionPage(
            title = "Bars: Overview",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.0f, 0.05f, 1f, 0.08f, "In each door, you could win or lose up to 7 coins.", sizeSp = 22f),
                textOverlay(0.02f, 0.16f, 0.94f, 0.09f, "The number of bars on the sides of the door will tell you:", sizeSp = 22f),
                textOverlay(0.01f, 0.35f, 0.38f, 0.18f, "If the door opens, and it hides a monster (50%): how many coins you'll lose.", sizeSp = 18f),
                textOverlay(0.61f, 0.35f, 0.38f, 0.18f, "If the door opens, and it hides a fairy (50%): how many coins you'll win.", sizeSp = 18f),
                imageOverlay(0.33f, 0.55f, 0.35f, 0.45f, R.drawable.inst_bars_generic),
                textOverlay(0.60f, 0.62f, 0.07f, 0.36f, "6\n5\n4\n3\n2\n1", sizeSp = 16f),
                textOverlay(0.355f, 0.85f, 0.07f, 0.15f, "2\n1", sizeSp = 16f)
            )
        ),
        // Deck slide 8
        InstructionPage(
            title = "Bars: Reward Side",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.0f, 0.05f, 1f, 0.08f, "In each door, you could win or lose up to 7 coins.", sizeSp = 22f),
                textOverlay(0.02f, 0.16f, 0.94f, 0.09f, "The number of bars on the sides of the door will tell you:", sizeSp = 22f),
                textOverlay(0.61f, 0.35f, 0.38f, 0.18f, "If the door opens, and it hides a fairy (50%): how many coins you'll win.", sizeSp = 18f),
                imageOverlay(0.33f, 0.55f, 0.35f, 0.45f, R.drawable.inst_bars_generic),
                textOverlay(0.60f, 0.62f, 0.07f, 0.36f, "6\n5\n4\n3\n2\n1", sizeSp = 16f),
                textOverlay(0.355f, 0.85f, 0.07f, 0.15f, "2\n1", sizeSp = 16f),
                textOverlay(0.75f, 0.65f, 0.22f, 0.09f, "+6 coins", sizeSp = 22f, bold = true, colorHex = "#1F7A3D"),
                imageOverlay(0.79f, 0.74f, 0.15f, 0.22f, R.drawable.inst_fairy_result)
            )
        ),
        // Deck slide 9
        InstructionPage(
            title = "Bars: Punishment Side",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.0f, 0.05f, 1f, 0.08f, "In each door, you could win or lose up to 7 coins.", sizeSp = 22f),
                textOverlay(0.02f, 0.16f, 0.94f, 0.09f, "The number of bars on the sides of the door will tell you:", sizeSp = 22f),
                textOverlay(0.01f, 0.35f, 0.38f, 0.18f, "If the door opens, and it hides a monster (50%): how many coins you'll lose.", sizeSp = 18f),
                imageOverlay(0.33f, 0.55f, 0.35f, 0.45f, R.drawable.inst_bars_generic),
                textOverlay(0.60f, 0.62f, 0.07f, 0.36f, "6\n5\n4\n3\n2\n1", sizeSp = 16f),
                textOverlay(0.355f, 0.85f, 0.07f, 0.15f, "2\n1", sizeSp = 16f),
                textOverlay(0.04f, 0.64f, 0.22f, 0.09f, "-2 coins", sizeSp = 22f, bold = true, colorHex = "#A73B3B"),
                imageOverlay(0.07f, 0.73f, 0.15f, 0.22f, R.drawable.inst_monster_result)
            )
        ),
        // Deck slide 10
        InstructionPage(
            title = "Bars: Example",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.05f, 0.13f, 0.90f, 0.20f, "If this door hides a fairy: you'll win 3 coins.\nIf this door hides a monster: you'll lose 6 coins.", sizeSp = 22f),
                imageOverlay(0.31f, 0.50f, 0.35f, 0.45f, R.drawable.inst_bars_example),
                textOverlay(0.05f, 0.56f, 0.22f, 0.09f, "-6 coins", sizeSp = 22f, bold = true, colorHex = "#A73B3B"),
                imageOverlay(0.06f, 0.66f, 0.20f, 0.27f, R.drawable.inst_monster_icon_small),
                textOverlay(0.70f, 0.56f, 0.24f, 0.09f, "+3 coins", sizeSp = 22f, bold = true, colorHex = "#1F7A3D"),
                imageOverlay(0.72f, 0.66f, 0.20f, 0.29f, R.drawable.inst_fairy_icon_small)
            )
        ),
        // Deck slide 16
        InstructionPage(
            title = "Remember: Door Opens",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.24f, 0.06f, 0.50f, 0.09f, "Remember, if the door opens:", sizeSp = 26f, bold = true),
                imageOverlay(0.09f, 0.18f, 0.29f, 0.37f, R.drawable.inst_bars_example),
                textOverlay(0.19f, 0.30f, 0.09f, 0.10f, "6-", sizeSp = 26f, bold = true, colorHex = "#A73B3B"),
                imageOverlay(0.16f, 0.42f, 0.14f, 0.20f, R.drawable.inst_monster_icon),
                imageOverlay(0.63f, 0.18f, 0.29f, 0.37f, R.drawable.inst_bars_example),
                textOverlay(0.71f, 0.30f, 0.09f, 0.10f, "3+", sizeSp = 26f, bold = true, colorHex = "#1F7A3D"),
                imageOverlay(0.70f, 0.42f, 0.13f, 0.19f, R.drawable.inst_fairy_icon),
                textOverlay(0.30f, 0.62f, 0.40f, 0.10f, "or", sizeSp = 26f)
            )
        ),
        // Deck slide 17
        InstructionPage(
            title = "Remember: Door Doesn't Open",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.24f, 0.10f, 0.50f, 0.09f, "If the door does not open:", sizeSp = 26f, bold = true),
                imageOverlay(0.34f, 0.24f, 0.30f, 0.38f, R.drawable.inst_bars_example),
                imageOverlay(0.41f, 0.38f, 0.16f, 0.20f, R.drawable.inst_lock_icon),
                textOverlay(0.20f, 0.68f, 0.60f, 0.10f, "You won't win or lose coins", sizeSp = 24f)
            )
        ),
        // Deck slide 19
        // "Let's review:" and "You see a door:" were baked into the source slide's picture with
        // no live-text equivalent; reproduced here as real text, styled to match the same heading
        // ("Let's review:") that slides 21-23 already carry as live text.
        InstructionPage(
            title = "Review: A Door",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.02f, 0.03f, 0.45f, 0.09f, "Let's review:", sizeSp = 28f, bold = true, align = InstructionTextAlign.START),
                textOverlay(0.30f, 0.14f, 0.40f, 0.08f, "You see a door:", sizeSp = 22f),
                imageOverlay(0.32f, 0.26f, 0.36f, 0.45f, R.drawable.inst_bars_review),
                textOverlay(0.03f, 0.72f, 0.30f, 0.16f, "How many coins you could lose", sizeSp = 22f, bold = true, align = InstructionTextAlign.START),
                textOverlay(0.67f, 0.62f, 0.30f, 0.16f, "How many coins you could win", sizeSp = 22f, bold = true, align = InstructionTextAlign.END)
            )
        ),
        // Deck slide 20 (mouse-drag illustration dropped as desktop-specific; the underlying
        // statement still applies with the touch slider, so it is kept as real text)
        InstructionPage(
            title = "Review: Getting Closer",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.02f, 0.06f, 0.45f, 0.09f, "Let's review:", sizeSp = 28f, bold = true, align = InstructionTextAlign.START),
                textOverlay(0.08f, 0.24f, 0.84f, 0.24f, "You decide how close you want to get to it.\nThe closer you get, the more likely that it will open.", sizeSp = 24f),
                imageOverlay(0.32f, 0.55f, 0.36f, 0.42f, R.drawable.inst_bars_review)
            )
        ),
        // Deck slide 21
        InstructionPage(
            title = "Review: Fairy Outcome",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.02f, 0.02f, 0.39f, 0.08f, "Let's review:", sizeSp = 28f, bold = true, align = InstructionTextAlign.START),
                imageOverlay(0.30f, 0.19f, 0.41f, 0.51f, R.drawable.inst_bars_review),
                imageOverlay(0.43f, 0.39f, 0.18f, 0.26f, R.drawable.inst_fairy_icon),
                textOverlay(0.44f, 0.27f, 0.12f, 0.08f, "5+", sizeSp = 26f, bold = true, colorHex = "#1F7A3D"),
                textOverlay(0.16f, 0.70f, 0.68f, 0.16f, "If the door opened and there's a fairy: You won – in this case, 5 coins", sizeSp = 22f, bold = true)
            )
        ),
        // Deck slide 22
        InstructionPage(
            title = "Review: Monster Outcome",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.02f, 0.02f, 0.39f, 0.08f, "Let's review:", sizeSp = 28f, bold = true, align = InstructionTextAlign.START),
                imageOverlay(0.30f, 0.19f, 0.41f, 0.51f, R.drawable.inst_bars_review),
                imageOverlay(0.42f, 0.40f, 0.18f, 0.25f, R.drawable.inst_monster_icon),
                textOverlay(0.47f, 0.27f, 0.08f, 0.08f, "2-", sizeSp = 26f, bold = true, colorHex = "#A73B3B"),
                textOverlay(0.14f, 0.70f, 0.72f, 0.16f, "If the door opened and there's a monster: You lost – in this case, 2 coins", sizeSp = 22f, bold = true)
            )
        ),
        // Deck slide 23
        InstructionPage(
            title = "Review: No Outcome",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.02f, 0.02f, 0.39f, 0.08f, "Let's review:", sizeSp = 28f, bold = true, align = InstructionTextAlign.START),
                imageOverlay(0.30f, 0.19f, 0.41f, 0.51f, R.drawable.inst_bars_review),
                imageOverlay(0.43f, 0.375f, 0.15f, 0.20f, R.drawable.inst_lock_icon),
                textOverlay(0.14f, 0.70f, 0.72f, 0.16f, "If the door didn't open: You didn't win or lose coins", sizeSp = 22f, bold = true)
            )
        ),
        // Deck slide 24
        InstructionPage(
            title = "Getting Paid",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.05f, 0.05f, 0.90f, 0.16f, "At the end of the game, you will receive REAL MONEY for your game winnings", sizeSp = 26f),
                imageOverlay(0.15f, 0.30f, 0.70f, 0.32f, R.drawable.inst_dollars),
                textOverlay(0.05f, 0.70f, 0.90f, 0.16f, "The more coins you get, the more money you will receive at the end of the game!", sizeSp = 24f)
            )
        ),
        // Deck slide 27
        // The source slide's own background picture carried a redundant, differently-worded
        // caption ("+6 dollars" / "-2 dollars") from an older draft; that picture was not used
        // here. The live "coins"-worded text below is what the deck actually displays on top of
        // it, and the coin-pile icon from that picture was replaced with the fairy/monster icons
        // used consistently everywhere else in the app, since no caption-free coin-pile asset
        // exists in the source deck's media.
        InstructionPage(
            title = "Bars Recap",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.04f, 0.04f, 0.92f, 0.30f, "A series of bars on the slides of the door will tell you:\nIf the door is hiding coins: how many coins you could win.\nIf the door is hiding a monster: how many coins you could lose.", sizeSp = 22f),
                imageOverlay(0.32f, 0.36f, 0.35f, 0.45f, R.drawable.inst_bars_generic),
                textOverlay(0.04f, 0.53f, 0.22f, 0.09f, "-2 coins", sizeSp = 22f, bold = true, colorHex = "#A73B3B"),
                imageOverlay(0.02f, 0.62f, 0.20f, 0.28f, R.drawable.inst_monster_icon),
                textOverlay(0.75f, 0.53f, 0.22f, 0.09f, "+6 coins", sizeSp = 22f, bold = true, colorHex = "#1F7A3D"),
                imageOverlay(0.78f, 0.62f, 0.20f, 0.28f, R.drawable.inst_fairy_icon)
            )
        ),
        // Deck slide 28 (same media caveat as slide 27 above)
        InstructionPage(
            title = "Bars Recap: Example",
            body = "",
            screenBackgroundColorHex = BG,
            backButtonColorHex = BACK_BTN,
            nextButtonColorHex = NEXT_BTN,
            overlays = listOf(
                textOverlay(0.05f, 0.05f, 0.90f, 0.18f, "If this door hides coins: you'll win 5 coins.\nIf this door hides a monster: you'll lose 2 coins.", sizeSp = 22f),
                imageOverlay(0.32f, 0.28f, 0.35f, 0.45f, R.drawable.inst_bars_review),
                textOverlay(0.05f, 0.76f, 0.22f, 0.09f, "-2 coins", sizeSp = 22f, bold = true, colorHex = "#A73B3B"),
                imageOverlay(0.03f, 0.60f, 0.20f, 0.16f, R.drawable.inst_monster_icon),
                textOverlay(0.74f, 0.76f, 0.22f, 0.09f, "+5 coins", sizeSp = 22f, bold = true, colorHex = "#1F7A3D"),
                imageOverlay(0.77f, 0.60f, 0.20f, 0.16f, R.drawable.inst_fairy_icon)
            )
        )
    )
}
