## Context for the Doors Task Android App Project

This document provides the necessary context for understanding and modifying the Doors Task Android application.

### 1. Project Goal & Task Flow

The project is a native Android mobile application that implements the "Doors Task." 

#### Scientific Purpose
The task is a psychological experiment designed to assess **approach-avoidance behavior**, particularly in the context of anxiety disorders. It measures how a user's decisions are influenced by varying levels of potential reward and potential punishment. The primary data of interest is the "distance" a user chooses to keep from a door, which represents their level of engagement or avoidance of a given risk/reward scenario.

#### Task Flow
A complete session of the Doors Task follows this sequence:

1.  **Instructions**: The user is first presented with a series of instructional slides that explain the task.

2.  **Trial Block**: The user begins a block of trials. A single trial proceeds as follows:
    -   **Door Presentation**: A door is shown on screen. Each door is associated with a unique combination of a potential reward (e.g., +X coins) and a potential punishment (e.g., -Y coins).
    -   **Decision**: The user uses a slider to choose their "distance" from the door, which corresponds to a percentage (0-100%). This percentage directly sets the probability that the door will open. A higher percentage (closer distance) means a higher chance of the door opening. This decision must be made within a 10-second time limit.
    -   **Lock-In**: The user can press a "Lock In" button to confirm their choice. If no choice is made after 10 seconds, the current distance is locked in automatically.
    -   **Anticipation**: A brief delay occurs after the choice is locked in.
    -   **Outcome**: One of two things happens:
        -   **Door Stays Closed**: Based on the probability set by the user, the door may not open. The trial ends, and no coins are won or lost.
        -   **Door Opens**: If the door opens, a 50/50 chance determines the outcome. The user either wins the specified reward coins or loses the specified punishment coins.

3.  **VAS (Visual Analogue Scale)**: After a block of trials, the user is presented with one or more VAS questions to rate their current subjective state (e.g., "How anxious do you feel right now?").

4.  **Repeat**: The user may complete one or more blocks of trials, often separated by a VAS assessment.

5.  **Summary**: Once all trials are complete, the user is shown a final summary screen displaying their total coins earned.

### 2. Core Technologies & Architecture

-   **Language**: Kotlin
-   **UI**: Jetpack Compose
-   **Architecture**: A state-driven MVVM (Model-View-ViewModel) approach is used.
    -   A central `DoorTaskViewModel` holds the application's entire state.
    -   UI Composables are largely stateless and observe a `StateFlow` from the ViewModel.
-   **Navigation**: The app uses a custom state-driven navigation system. A central `AppNavigator` composable observes a `TaskPhase` enum from the ViewModel to decide which screen to display. This avoids complex navigation graphs and keeps the current screen as a function of the application's state.
-   **Data Persistence**: A local Room database is used for data storage.
-   **Build System**: Gradle, executed via the `./gradlew` wrapper in the `app/` directory.

### 3. Project Structure

```
app
└── src
    └── main
        ├── java/com/neuroscienceanxietylab/doorstask/
        │   ├── data/             # Data layer: Room database, DAO, and @Entity models.
        │   ├── navigation/       # Contains the state-driven AppNavigator.
        │   ├── ui/               # Composable UI components.
        │   │   ├── screens/      # The app's main screens.
        │   │   └── theme/        # App theme (colors, typography).
        │   ├── util/             # Utility classes (SoundPlayer).
        │   ├── viewmodel/        # The central DoorTaskViewModel.
        │   └── MainActivity.kt   # Single activity entry point.
        │
        └── res/                  # Resources
            ├── drawable/         # All image assets.
            ├── raw/              # All sound and video assets.
            └── values/           # strings.xml, colors.xml, etc.

copy_assets.sh          # A shell script used to copy and sanitize assets.
README.md               # Comprehensive project documentation.
prompt.md               # This file.
```

### 4. Key File Summaries

-   **`viewmodel/DoorTaskViewModel.kt`**: The **brain** of the app. It manages the current `TaskPhase` (which screen to show), the list of trials, the current trial index, coin totals, and all core logic for timing and outcomes. Constants like `NUM_TRIALS_PER_BLOCK` and `TRIAL_TIMEOUT_MS` are defined here.

-   **`navigation/AppNavigator.kt`**: The **navigator**. It contains a `when` statement that observes `uiState.phase` from the ViewModel and renders the correct screen. This is the single source of truth for navigation.

-   **`ui/screens/DoorTrialScreen.kt`**: The main experiment screen. It is mostly stateless. It displays door images, a slider for distance, and outcome animations based on the ViewModel's state. It uses `Modifier.graphicsLayer` to apply a true zoom effect to the door image.

-   **`ui/screens/InstructionScreen.kt`**: Displays a sequence of instruction images. The list of images is currently hardcoded here.

-   **`data/` package**: Defines the schema for the local Room database. It contains three `@Entity` classes: `SessionLog` (for trial summaries), `EventLog` (for fine-grained distance changes), and `VASResponse`.

-   **`README.md`**: A detailed documentation file with instructions for common and advanced modifications. **Always refer to this file first for modification instructions.**

### 5. How to Build & Verify

To compile the entire application and check for errors, run the following command from the `app/` directory:

```bash
./gradlew build
```

---

With this context, you are prepared to assist with modifications, bug fixes, and feature additions to this project.
