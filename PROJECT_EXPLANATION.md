# Music Recommendation System - Complete Project Explanation

## Project Overview
This is a music recommendation system that analyzes song features from a CSV dataset and calculates similarity between tracks and artists using various mathematical algorithms. The system provides a graphical user interface (GUI) for easy interaction.

---

## Module 1: load_dataset.py (Data Loading Module)

### Purpose
Loads music data from a CSV file and organizes it into a dictionary structure for efficient access.

### Key Components

#### Class: `DatasetLoader`

**Constructor (`__init__`)**
```python
def __init__(self, filepath):
    self.filepath = filepath
    self.artist_music = {}
```
- Takes the CSV file path as input
- Initializes an empty dictionary `artist_music` to store all data

**Method: `load_data()`**

**What it does:**
1. Opens the CSV file and reads it row by row using `csv.DictReader`
2. For each song/track, it extracts:
   - **Artists**: Can be multiple artists per track (handles comma-separated values)
   - **Track ID**: Unique identifier for each song
   - **Track name**: Title of the song
   - **Audio features**: 9 musical characteristics (acousticness, danceability, energy, liveness, loudness, speechiness, tempo, valence, popularity)

**Data Structure Created:**
```python
{
    "Artist Name": {
        "track_id_1": {
            "name": "Song Title",
            "features": {
                "acousticness": 0.5,
                "danceability": 0.7,
                "energy": 0.8,
                # ... more features
            }
        },
        "track_id_2": { ... }
    },
    "Another Artist": { ... }
}
```

**Key Features:**
- Handles multiple artists per track (splits by comma)
- Converts all feature values to appropriate data types (float for audio features, int for popularity)
- Uses `strip()` to remove extra whitespace from artist names
- Groups all tracks by their artists for easy lookup

**Return Value:** Returns the complete `artist_music` dictionary

---

## Module 2: similarity_module.py (Similarity Calculation Module)

### Purpose
Calculates similarity between tracks or artists using three different mathematical methods.

### Key Components

#### Class: `BaseSimilarity`
**Method: `features_to_list()`**
- Converts a feature dictionary into a simple list of values
- This is needed for mathematical calculations (you can't do math operations on dictionaries)
- Example: `{"acousticness": 0.5, "danceability": 0.7}` → `[0.5, 0.7]`

#### Class: `SimilarityEngine` (inherits from `BaseSimilarity`)

**Constructor:**
```python
def __init__(self, artist_music):
    self.artist_music = artist_music
```
- Stores the entire dataset for quick access

**Method: `get_track_features(track_id)`**
- Searches through all artists to find a specific track by its ID
- Returns the feature dictionary for that track
- Returns `None` if track is not found

### Three Similarity Calculation Methods:

#### 1. Euclidean Similarity
```python
def euclidean_similarity(self, list1, list2):
    total = 0
    for i in range(len(list1)):
        total += (list1[i] - list2[i]) ** 2
    return math.sqrt(total)
```

**What it does:**
- Calculates the straight-line distance between two points in multi-dimensional space
- Formula: √((x₁-y₁)² + (x₂-y₂)² + ... + (xₙ-yₙ)²)
- **Lower values = More similar** (0 means identical)
- Like measuring the physical distance between two locations

**Example:**
- Track A: [0.5, 0.7, 0.6]
- Track B: [0.6, 0.8, 0.5]
- Distance: √((0.5-0.6)² + (0.7-0.8)² + (0.6-0.5)²) = √(0.01 + 0.01 + 0.01) = 0.173

#### 2. Cosine Similarity
```python
def cosine_similarity(self, list1, list2):
    dot_product = 0
    mag1 = 0
    mag2 = 0
    
    for i in range(len(list1)):
        dot_product += list1[i] * list2[i]
        mag1 += list1[i] ** 2
        mag2 += list2[i] ** 2
    
    if mag1 == 0 or mag2 == 0:
        return 0
    
    return dot_product / (math.sqrt(mag1) * math.sqrt(mag2))
```

**What it does:**
- Measures the angle between two vectors (feature lists)
- Formula: (A·B) / (|A| × |B|)
- Range: -1 to 1 (1 = identical, 0 = unrelated, -1 = opposite)
- **Higher values = More similar**
- Good for comparing patterns regardless of magnitude

**Steps:**
1. Calculate dot product: sum of (list1[i] × list2[i])
2. Calculate magnitudes: √(sum of squares)
3. Divide dot product by product of magnitudes

#### 3. Pearson Similarity (Correlation Coefficient)
```python
def pearson_similarity(self, list1, list2):
    mean1 = sum(list1) / len(list1)
    mean2 = sum(list2) / len(list2)
    
    top = 0
    bottom1 = 0
    bottom2 = 0
    
    for i in range(len(list1)):
        top += (list1[i] - mean1) * (list2[i] - mean2)
        bottom1 += (list1[i] - mean1) ** 2
        bottom2 += (list2[i] - mean2) ** 2
    
    if bottom1 == 0 or bottom2 == 0:
        return 0
    
    return top / (math.sqrt(bottom1) * math.sqrt(bottom2))
```

**What it does:**
- Measures linear correlation between two variables
- Range: -1 to 1 (1 = perfect positive correlation)
- **Higher values = More similar**
- Similar to cosine but subtracts the mean first (centers the data)
- Good for finding tracks that vary together

**Steps:**
1. Calculate mean of each list
2. For each feature, calculate deviation from mean
3. Multiply deviations and sum (numerator)
4. Calculate standard deviations (denominator)
5. Divide numerator by denominator

### Comparison Methods:

**`track_similarity(track1_id, track2_id, method)`**
- Compares two individual tracks
- Gets features for both tracks
- Converts to lists
- Applies the chosen similarity method
- Returns similarity score

**`artist_similarity(artist1, artist2, method)`**
- Compares two artists based on their average track features
- Uses a nested function `average_features()` that:
  - Collects all tracks from an artist
  - Averages each feature across all tracks
  - Returns average feature vector
- Then compares the two average vectors using chosen method

**`top_5_similar_artists(artist, method)`**
- Finds the 5 most similar artists to a given artist
- Steps:
  1. Loop through all other artists
  2. Calculate similarity score for each
  3. Store (artist_name, score) pairs
  4. Sort by score (highest first for cosine/pearson, lowest for euclidean)
  5. Return top 5

---

## Module 3: statistics_module.py (Statistical Analysis Module)

### Purpose
Provides statistical analysis of audio features across the entire dataset.

### Key Components

#### Class: `StatsAnalyzer`

**Constructor:**
```python
def __init__(self, artist_music: dict):
    self.artist_music = artist_music
```
- Stores the dataset for analysis

### Helper Methods (Private - start with `_`):

**`_all_feature_values(feature_name)`**
- Collects all values for a specific feature across entire dataset
- Example: All "danceability" values from all tracks
- Returns a list of numbers

**`_mean(values)`**
- Calculates average: sum / count
- Formula: (x₁ + x₂ + ... + xₙ) / n

**`_min(values)` and `_max(values)`**
- Find minimum and maximum values in the list

**`_variance(values, sample=False)`**
- Measures how spread out the data is
- Formula: Σ(x - mean)² / n
- If `sample=True`, divides by (n-1) instead of n (sample variance)
- Higher variance = more spread out data

**`_std_dev(values, sample=False)`**
- Standard deviation: square root of variance
- More interpretable than variance (same units as original data)
- Formula: √variance

**`_mode(values)`**
- Most frequently occurring value
- Returns:
  - Single value if one clear mode
  - List if multiple modes (tie)
  - None if no mode (all equally common)
- Uses `Counter` from collections module to count occurrences

### Public Method:

**`feature_summary(feature_name, sample_std=False)`**

Returns a comprehensive dictionary with all statistics:
```python
{
    "count": 1000,           # Number of values
    "mean": 0.65,           # Average
    "mode": 0.7,            # Most common value
    "min": 0.0,             # Minimum
    "max": 1.0,             # Maximum
    "variance": 0.05,       # Spread measure
    "std_dev": 0.22        # Standard deviation
}
```

**Use Case:**
- Analyze feature distributions
- Understand data ranges
- Identify typical values
- Detect outliers

---

## Module 4: user_interface_module.py (GUI Module)

### Purpose
Creates a graphical user interface for easy interaction with the recommendation system.

### Key Components

#### Design Theme: Material Design 3 Dark Theme
- Professional, modern appearance
- Custom color scheme with purple accents
- Colors defined as constants at top of file

#### Class: `MusicApp`

**Constructor (`__init__`)**

Creates the entire GUI with these sections:

**1. Window Setup**
```python
self.window = tk.Tk()
self.window.title("Music Recommendation System")
self.window.geometry("700x750")
self.window.configure(bg=BG_COLOR)
```
- Creates main window
- Sets size to 700×750 pixels
- Applies dark background color

**2. Similarity Method Selection Card**
- Text entry field for choosing algorithm
- Default: "euclidean"
- Options: euclidean, cosine, pearson
- Helper text shows available options

**3. Comparison Mode Selection**
- Radio buttons for three modes:
  - **Track IDs**: Compare using Spotify track IDs
  - **Artists**: Compare two artists
  - **Track Names**: Compare using song titles
- Uses `tk.StringVar()` to track selection

**4. Input Fields Card**
- Two text entry fields:
  - "First Input": First track/artist to compare
  - "Second Input": Second track/artist to compare
- Styled with Material Design colors
- Custom border highlighting on focus

**5. Button Frame**
- **Compare Button**: Triggers the comparison
- **Quit Button**: Closes the application
- Custom styling with hover effects

**6. Output Text Area**
- Large text box to display results
- Read-only for user (but editable programmatically)
- Monospace font (Consolas) for aligned output
- Dark themed with syntax highlighting

**7. Progress Bar**
- Shows progress when calculating similarities for many tracks
- Material Design styled
- Horizontal orientation

### Core Methods:

**`find_track_id_by_name(name)`**
- Searches entire dataset for a track by its name
- Case-insensitive search (converts to lowercase)
- Returns track ID if found, None otherwise

**`get_all_track_ids()`**
- Collects all track IDs from the dataset
- Returns complete list for batch comparisons

**`compare()`** - The Main Logic Method

**What it does:**

1. **Get User Inputs**
   - Reads similarity method from entry field
   - Reads two inputs (track IDs, artist names, or track names)
   - Clears previous output
   - Resets progress bar

2. **Three Different Comparison Modes:**

   **Mode A: Track Comparison**
   ```python
   if self.mode.get() == "track":
   ```
   - Calculates similarity between two tracks
   - Then finds top 5 similar tracks to the first track
   - Updates progress bar for each comparison
   - Displays results in output area

   **Mode B: Artist Comparison**
   ```python
   elif self.mode.get() == "artist":
   ```
   - Calculates similarity between two artists
   - Uses `top_5_similar_artists()` to find similar artists
   - Displays artist names with similarity scores

   **Mode C: Track Name Comparison**
   ```python
   else:  # name mode
   ```
   - Converts track names to track IDs
   - Then performs track similarity comparison
   - Handles case where track names not found

3. **Error Handling**
   - Wraps all logic in try-except block
   - Shows error message box if something goes wrong
   - Displays helpful error messages

4. **Progress Bar Updates**
   ```python
   self.progress["value"] = i + 1
   self.window.update_idletasks()
   ```
   - Updates progress bar after each comparison
   - Forces GUI to redraw (update_idletasks)
   - Gives user visual feedback for long operations

**`run()`**
- Starts the GUI main loop
- Keeps window open and responsive
- Waits for user interactions

---

## Module 5: main.py (Entry Point)

### Purpose
The starting point of the application - ties everything together.

### Code Structure:

```python
def main():
    try:
        # 1. Create data loader
        loader = DatasetLoader("data.csv")
        
        # 2. Load the dataset
        artist_music = loader.load_data()
        
        # 3. Create GUI app with loaded data
        app = MusicApp(artist_music)
        
        # 4. Start the application
        app.run()
        
    except Exception as e:
        # Handle any startup errors
        print("Error starting application:", e)
```

**Flow:**
1. Creates a `DatasetLoader` instance with CSV file
2. Loads all data into memory
3. Passes data to `MusicApp` GUI
4. Starts the GUI event loop

**Error Handling:**
- Catches any errors during startup
- Prints error message if file not found or data corrupted

**Entry Point Check:**
```python
if __name__ == "__main__":
    main()
```
- Only runs `main()` if script is executed directly
- Allows importing without auto-running

---

## Data Flow Through the System

```
1. main.py
   ↓
2. DatasetLoader loads data.csv
   ↓
3. Creates artist_music dictionary
   ↓
4. Passes to MusicApp GUI
   ↓
5. User interacts with GUI
   ↓
6. MusicApp calls SimilarityEngine
   ↓
7. SimilarityEngine calculates similarities
   ↓
8. Results displayed in GUI
```

---

## Mathematical Concepts Explained

### 1. Euclidean Distance
- **Intuition**: Like measuring with a ruler in multi-dimensional space
- **Best for**: When absolute differences matter
- **Interpretation**: Lower = more similar

### 2. Cosine Similarity
- **Intuition**: Measures direction, not magnitude
- **Best for**: When relative patterns matter more than absolute values
- **Interpretation**: Higher = more similar (range: -1 to 1)

### 3. Pearson Correlation
- **Intuition**: Measures how features vary together
- **Best for**: Finding linear relationships
- **Interpretation**: Higher = more similar (range: -1 to 1)
- **Difference from Cosine**: Centers data around mean first

---

## Key Programming Concepts Used

### 1. Object-Oriented Programming (OOP)
- **Classes**: DatasetLoader, SimilarityEngine, StatsAnalyzer, MusicApp
- **Inheritance**: SimilarityEngine inherits from BaseSimilarity
- **Encapsulation**: Private methods (starting with `_`)

### 2. Data Structures
- **Dictionaries**: Nested dictionaries for artist → track → features
- **Lists**: For feature vectors and search results
- **Tuples**: For (artist, score) pairs

### 3. File I/O
- **CSV Reading**: Using `csv.DictReader`
- **Error Handling**: try-except blocks

### 4. GUI Programming
- **Tkinter**: Python's standard GUI library
- **Event-Driven**: Responds to button clicks
- **Progressive Updates**: Progress bar during calculations

### 5. Algorithms
- **Sorting**: `results.sort(key=lambda x: x[1])`
- **Searching**: Linear search through dictionaries
- **Statistical Calculations**: Mean, variance, standard deviation

---

## How to Use the System

1. **Run the program**: Execute `main.py`
2. **Choose similarity method**: Type "euclidean", "cosine", or "pearson"
3. **Select mode**: Track IDs, Artists, or Track Names
4. **Enter inputs**: Type two values to compare
5. **Click Compare**: See similarity score and top 5 recommendations
6. **View results**: Scroll through output area

---

## Potential Improvements

1. **Database Integration**: Use SQLite instead of CSV for larger datasets
2. **More Algorithms**: Add Manhattan distance, Jaccard similarity
3. **User Ratings**: Incorporate user preferences
4. **Visualization**: Add charts and graphs
5. **Search Functionality**: Auto-complete for artist/track names
6. **Export Results**: Save recommendations to file
7. **Playlist Generation**: Create Spotify playlists automatically

---

## Conclusion

This music recommendation system demonstrates:
- **Data processing**: Loading and organizing CSV data
- **Mathematical algorithms**: Three different similarity measures
- **Statistical analysis**: Comprehensive feature statistics
- **User interface design**: Professional Material Design GUI
- **Modular programming**: Separate modules for different functions

The system can help users discover new music by finding songs or artists similar to their favorites, using scientifically-sound similarity algorithms.
