# Doors Task Android App

This document provides a comprehensive overview of the Doors Task Android application, its architecture, and a guide for making future modifications.

## 1. Application Overview

This application is a mobile-friendly Android version of the "Doors Task" psychological experiment. The task is designed to assess approach-avoidance behavior in response to potential rewards and punishments. The app presents users with a series of doors, each with a different combination of potential gains and losses. The user decides their level of engagement (represented as distance/zoom), which determines the probability of the door opening.

The app is built using modern Android development practices with Kotlin and Jetpack Compose.

## 2. Getting Started

### Prerequisites
- Android Studio (latest stable version recommended)
- An Android Emulator or a physical Android device

### Build and Run Instructions
1.  **Open the Project**: In Android Studio, select **File > Open** and navigate to the `app` directory within this project.
2.  **Sync Gradle**: Android Studio will automatically detect the Gradle build files and sync the project dependencies.
3.  **Select a Device**: Choose an emulator or a connected physical device from the device dropdown menu in the toolbar.
4.  **Run**: Click the green 'Run' button to build, install, and launch the application on your selected device.

## 3. Project Structure

The project is organized into a standard Android app structure, with key components separated into logical packages.

```
app
└── src
    └── main
        ├── java/com/neuroscienceanxietylab/doorstask/
        │   ├── data/             # Data layer (database, models)
        │   │   ├── local/        # Room database and DAO
        │   │   └── model/        # @Entity data classes
        │   ├── navigation/       # Navigation logic and routes
        │   ├── ui/               # UI components
        │   │   ├── screens/      # Composable screens
        │   │   └── theme/        # App theme and styles
        │   ├── util/             # Utility classes (e.g., SoundPlayer)
        │   ├── viewmodel/        # ViewModel for state management
        │   └── MainActivity.kt   # The single entry point for the app
        │
        └── res/                  # Application resources
            ├── drawable/         # Image assets
            ├── raw/              # Sound and video assets
            └── values/           # Strings, colors, themes
```

## 4. Core Components Explained

The app follows a modern, state-driven architecture using a central ViewModel.

-   **`DoorTaskViewModel.kt`**: This is the brain of the application. It holds the entire state of the task in `TaskUiState`, manages the flow of the experiment through `TaskPhase`, and contains all the core logic (e.g., generating trials, calculating outcomes, handling timers). The UI screens observe the state from this ViewModel and react accordingly.

-   **`AppNavigator.kt`**: This is the app's "traffic cop." Instead of traditional navigation where screens push each other, this component observes the `TaskPhase` from the `DoorTaskViewModel` and displays the appropriate screen (`InstructionScreen`, `DoorTrialScreen`, etc.). This creates a robust, single source of truth for what the user should be seeing.

-   **UI Screens (`/ui/screens`)**: These are simple, stateless composable functions that receive data from the ViewModel and display it. They capture user input (like button clicks or slider changes) and forward these events to the ViewModel for processing.

-   **Data Layer (`/data`)**: This package contains the Room database implementation for local data persistence. The `model` package defines the tables (`SessionLog`, `EventLog`, `VASResponse`), and the `local` package contains the DAO (Data Access Object) and the database class itself.

## 5. How to Make Modifications

This section details how to customize various aspects of the application.

### Changing the Number of Trials/Blocks

To change how many trials are in a block, you only need to edit one constant.

-   **File**: `app/src/main/java/com/neuroscienceanxietylab/doorstask/viewmodel/DoorTaskViewModel.kt`
-   **Constant**: `NUM_TRIALS_PER_BLOCK`

```kotlin
private const val NUM_TRIALS_PER_BLOCK = 25 // For demo; original is 49. Let's do 2 blocks.
```

Change the value `25` to your desired number of trials per block. The total number of trials in the experiment will be twice this value.

### Changing Timings

All timing-related logic is centralized in the `DoorTaskViewModel` and `DoorTrialScreen`.

1.  **Auto-Lock Timer**: To change the 10-second timer for each trial:
    -   **File**: `DoorTaskViewModel.kt`
    -   **Constant**: `TRIAL_TIMEOUT_MS` (value is in milliseconds)

2.  **Anticipation Delay** (time between lock-in and outcome):
    -   **File**: `DoorTaskViewModel.kt`
    -   **Method**: `onLockInPressed()`
    -   **Code**: `delay(3000)`

3.  **Outcome Display Duration**: To change how long the win/loss outcome is shown:
    -   **File**: `app/src/main/java/com/neuroscienceanxietylab/doorstask/ui/screens/DoorTrialScreen.kt`
    -   **Composable**: `OutcomeOverlay`
    -   **Code**: `delay(2000)`

### Changing Graphics and Zoom

1.  **Replacing Existing Graphics**: To change an image or sound, simply replace the corresponding file in the resource directories. The file name must be identical.
    -   **Images**: `app/src/main/res/drawable/`
    -   **Sounds/Videos**: `app/src/main/res/raw/`

2.  **Changing Door Image Zoom/Ratio**: The zoom effect is controlled in the trial screen.
    -   **File**: `DoorTrialScreen.kt`
    -   **Code**: The `Image` composable uses two key properties:
        ```kotlin
        Image(
            // ...
            modifier = Modifier
                .size(300.dp) // This is the base size at 0% zoom
                .graphicsLayer( // This handles the scaling
                    scaleX = animatedScale,
                    scaleY = animatedScale
                ),
            // ...
        )
        ```
        -   To change the initial size of the door, modify `.size(300.dp)`.
        -   The zoom level is calculated by `animatedScale`, which ranges from `1.0f` (no zoom) to `2.0f` (max zoom). You can adjust the formula `1.0f + (uiState.currentDistance / 100f)` in the `DoorTrialScreen` if you need a different zoom behavior.

### Adding/Changing Instruction Slides

1.  **Add the Image**: Place your new instruction image file (e.g., `my_new_instruction.png`) into the `app/src/main/res/drawable/` directory.
2.  **Update the List**: Open `app/src/main/java/com/neuroscienceanxietylab/doorstask/ui/screens/InstructionScreen.kt` and add your new resource to the `instructionImages` list in the desired order.

    ```kotlin
    val instructionImages = remember {
        listOf(
            R.drawable.inst_en_1e,
            R.drawable.inst_en_2e,
            // ... add your new image here
            R.drawable.my_new_instruction,
            // ... other images
        )
    }
    ```

### Adding/Changing VAS Questions

Currently, there is one hardcoded VAS question. To add more and cycle through them, you should modify the `DoorTaskViewModel`.

1.  **Add State to ViewModel**: In `DoorTaskViewModel.kt`, add a list of questions and an index to track the current one.
    ```kotlin
    // In DoorTaskViewModel.kt
    private val vasQuestions = listOf("Question 1?", "Question 2?", "Question 3?")
    // In TaskUiState data class
    val vasQuestionIndex: Int = 0
    ```
2.  **Update ViewModel Logic**: Modify `onNextTrial` to increment the `vasQuestionIndex` when it navigates to the `VAS` phase. Modify `onVasResponse` to navigate back to the `TRIAL` phase.
3.  **Update the UI**: In `VASScreen.kt`, read the question from the ViewModel state instead of using a hardcoded string.
    ```kotlin
    // In VASScreen.kt
    val uiState by viewModel.uiState.collectAsState()
    val vasQuestions = // ... get from viewmodel
    val currentQuestion = vasQuestions[uiState.vasQuestionIndex]
    ```

This provides a robust way to handle multiple VAS questions throughout the experiment.

## 6. Firebase Backend and Data Management

This section details the integration with Google Firebase for user management, remote configuration, and data collection.

### 6.1. Backend Infrastructure (Firebase)

The app is powered by Google Firebase, which handles all server-side needs.

-   **Firebase Authentication**: Manages user sign-up and login via email and password.
-   **Firestore Database**: A NoSQL database that stores all application data in collections of documents.

#### Firestore Data Structure:

1.  `users` **Collection**
    -   **Purpose**: Stores the remote configuration for each user.
    -   **Document ID**: The user's unique Firebase Auth UID.
    -   **Fields**: `subjectId`, `trialsPerBlock`, `totalBlocks`, `trialTimeoutMs`.

2.  `completed_sessions` **Collection**
    -   **Purpose**: Stores the aggregated data from a user's entire session.
    -   **Document ID**: Auto-generated by Firestore.
    -   **Fields**: Contains top-level info (`userId`, `sessionTimestamp`) and two main arrays:
        -   `behavioral_data`: An array where each object is a complete trial log.
        -   `vas_responses`: An array where each object is a single VAS answer.

### 6.2. User & Task Configuration

**How it Works**
1.  A new user registers in the app.
2.  The `AuthViewModel` automatically creates a new document for them in the `users` collection in Firestore with default settings.
3.  When that user logs in, the `DoorTaskViewModel` fetches this document.
4.  The fetched values for `trialsPerBlock`, `totalBlocks`, etc., are used to set up the experiment for that session.

**How to Modify a User's Configuration**
1.  Log in to the **Firebase Console** and navigate to your **Firestore Database**.
2.  In the `users` collection, find the document corresponding to the user you wish to modify (the document ID is their Firebase UID).
3.  Click to edit the fields directly in the console. For example, you can change `trialsPerBlock` from `25` to `10`.
4.  The next time that user logs into the app, the new configuration will be applied automatically.

### 6.3. Data Collection & Export

**Data Model: Hybrid Approach**
-   **Local Backup**: Every trial and VAS answer is immediately saved to the on-device Room database. This is a robust backup against crashes.
-   **Remote Aggregation**: At the end of the final trial, the `DoorTaskViewModel` aggregates all the data collected in memory and uploads it as a single document to the `completed_sessions` collection in Firestore.

**How to Access and Export Data**
1.  Log in to the **Firebase Console** and navigate to your **Firestore Database**.
2.  Select the `completed_sessions` collection.
3.  Here you will find a list of documents, each representing a full session from a user.
4.  You can view the data directly in the console or use Firebase's export features to download the entire collection as JSON, which can then be easily converted to CSV or other formats for analysis.

### 6.4. Securing Your Database

The database currently uses test rules that allow open access. Before deploying your app for real data collection, you **must** secure it.

1.  Go to the **Rules** tab in your Firestore console.
2.  Replace the existing rules with the following:

    ```
    rules_version = '2';
    service cloud.firestore {
      match /databases/{database}/documents {
        // Users can only read their own config and cannot see other users' docs.
        match /users/{userId} {
          allow read: if request.auth.uid == userId;
          allow write: if false; // Disallow clients from changing their own config
        }
        // Users can only create new session documents for themselves.
        match /completed_sessions/{docId} {
          allow create: if request.auth.uid == request.resource.data.userId;
          allow read, update, delete: if false;
        }
      }
    }
    ```

This ensures that users can only read their own configuration and can only write their own session data. They cannot read, update, or delete anyone else's data, nor can they see other users' configurations.

## 7. Advanced Modifications

This section covers more complex customization scenarios.

### Switching Door Image Sets

The original project contained two sets of door images (`doors1` and `doors2`). The app currently uses the first set. To switch to the second set:

-   **File**: `app/src/main/java/com/neuroscienceanxietylab/doorstask/ui/screens/DoorTrialScreen.kt`
-   **Function**: `getDoorImageResource()`
-   **Logic**: Change the prefix used to find the resource name.

    ```kotlin
    // Helper to get the correct door image resource
    @Composable
    private fun getDoorImageResource(reward: Int, punishment: Int): Int {
        val context = LocalContext.current
        // CHANGE THE PREFIX HERE from "d1_" to "d2_"
        val resourceName = "d1_p${punishment}r${reward}"
        val resourceId = context.resources.getIdentifier(resourceName, "drawable", context.packageName)
        return if (resourceId != 0) resourceId else R.drawable.d1_p0r0 // Fallback image
    }
    ```

### Customizing Trial Logic

All core trial logic is located in the `DoorTaskViewModel`.

-   **File**: `app/src/main/java/com/neuroscienceanxietylab/doorstask/viewmodel/DoorTaskViewModel.kt`
-   **Method**: `onLockInPressed()`

1.  **Door Opening Probability**: The chance of a door opening is currently linear based on the user's distance. To change this, modify the following line:
    ```kotlin
    val doorOpens = Random.nextFloat() * 100 <= distance
    ```
    You can replace this with any custom function, for example, a non-linear curve.

2.  **Reward/Punishment Probability**: The outcome of an opened door is currently a 50/50 chance. To change this, modify the following line:
    ```kotlin
    val didWin = Random.nextBoolean() // This is 50/50
    ```
    For example, to set a 70% chance of winning, you could change it to:
    ```kotlin
    val didWin = Random.nextFloat() <= 0.7f // 70% chance to win
    ```

### Adding Multiple Languages (Localization)

To add support for other languages (e.g., Hebrew), you should use Android's built-in localization system.

1.  **Create New String Files**: In Android Studio, right-click the `app/src/main/res/values` directory, select **New > Values Resource File**, and create a new `strings.xml` file for your target language (e.g., select the "Locale" qualifier and choose "Hebrew"). This will create a file at `app/src/main/res/values-iw/strings.xml`.

2.  **Externalize Strings**: Move all hardcoded text from your composable files into `app/src/main/res/values/strings.xml`. For example:
    ```xml
    <!-- in values/strings.xml -->
    <string name="submit_button">Submit</string>
    ```

3.  **Translate Strings**: Add the translated versions to the new language file.
    ```xml
    <!-- in values-iw/strings.xml -->
    <string name="submit_button">שלח</string>
    ```

4.  **Use String Resources**: In your code, reference the strings using `stringResource()`. 
    ```kotlin
    Text(text = stringResource(R.string.submit_button))
    ```

5.  **Localizing Images**: For instruction slides, you would need to add logic to `InstructionScreen.kt` to check the device's current language and select the appropriate list of drawable resources (e.g., `inst_en_...` vs. `inst_he_...`).

### Exporting Collected Data

This feature is not yet implemented but can be added by following these general steps:

1.  **Add a UI Trigger**: Add an "Export Data" button, perhaps on the `SummaryScreen`.
2.  **Query the Database**: In the `DoorTaskViewModel`, create a function that uses the `TaskDao` to fetch all saved `SessionLog`, `EventLog`, and `VASResponse` data.
3.  **Format to CSV**: Convert the lists of data into a single, well-formatted CSV string.
4.  **Save the File**: Use Android's Storage Access Framework (`ACTION_CREATE_DOCUMENT`) to launch a system file picker, allowing the user to choose a location and name for the CSV file. This is the modern, secure way to save files on Android.

### Resetting the App for a New Subject

For experimental purposes, you often need to clear all data between subjects.

-   **The Easy Way (During Development)**: The simplest method is to uninstall and reinstall the app on the device. Alternatively, go to the device's **Settings > Apps > DoorsTask > Storage & cache** and tap **Clear storage**.

-   **In-App Feature (Advanced)**: To build this into the app, you could add a hidden "Reset" button. This button would trigger a function in the `DoorTaskViewModel` that calls a new method in your `TaskDao`, such as `clearAllTables()`, which you would implement with `@Query` annotations to delete all data from each table.