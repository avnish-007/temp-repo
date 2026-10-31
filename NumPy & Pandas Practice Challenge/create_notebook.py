import json

notebook = {
    'cells': [
        {
            'cell_type': 'markdown',
            'id': 'c0986aa3',
            'metadata': {},
            'source': [
                '# Dataset 2: Netflix Movies and TV Shows - Data Cleaning & Visualization\n',
                '\n',
                '* **Kaggle Link:** [Netflix Movies and TV Shows on Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)\n',
                '* **Core Competencies:** Datetime parsing, string cleaning, array flattening/exploding, frequency distributions, and data visualization.\n',
                '\n',
                'This notebook performs basic data cleaning and exploratory data analysis on the Netflix dataset, covering missing value handling, datetime parsing, duration extraction, genre analysis, and various visualizations.'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'c9d1ce14',
            'metadata': {},
            'outputs': [],
            'source': [
                'import numpy as np\n',
                'import pandas as pd\n',
                'import matplotlib.pyplot as plt\n',
                'import seaborn as sns\n',
                '\n',
                '%matplotlib inline\n',
                "plt.style.use('fivethirtyeight')\n",
                "sns.set_style('whitegrid')\n",
                '\n',
                "netflix_path = 'netflix_titles.csv'\n",
                'df = pd.read_csv(netflix_path)\n',
                '\n',
                "print('Shape of the dataset:', df.shape)\n",
                "print('Column names:', list(df.columns))\n",
                "print('\\nFirst 5 rows:')\n",
                'display(df.head())\n',
                "print('\\nData types:')\n",
                'display(df.dtypes)'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'da1e2c77',
            'metadata': {},
            'source': [
                '## 1. Data Exploration & Basic Cleaning\n',
                '\n',
                '### 1.1 Check for missing values\n',
                '\n',
                "Let's examine which columns have missing values and how many."
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '61618688',
            'metadata': {},
            'outputs': [],
            'source': [
                '# Check for missing values in each column\n',
                "missing_values = df.isnull().sum()\n",
                "missing_percent = (df.isnull().sum() / len(df)) * 100\n",
                "missing_df = pd.DataFrame({\n",
                "    'Total Missing': missing_values,\n",
                "    'Percentage': missing_percent.round(2)\n",
                "})\n",
                '\n',
                "missing_df = missing_df[missing_df['Total Missing'] > 0].sort_values('Total Missing', ascending=False)\n",
                "print('Columns with missing values:')\n",
                'display(missing_df)\n',
                '\n',
                "plt.figure(figsize=(10, 6))\n",
                "sns.heatmap(df.isnull(), cbar=False, cmap='viridis')\n",
                "plt.title('Missing Values Heatmap')\n",
                'plt.show()'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': '658d363e',
            'metadata': {},
            'source': [
                '### 1.2 Impute missing values\n',
                '\n',
                "We'll impute missing `director` and `cast` values with 'Unknown', and drop rows where `date_added` or `rating` is missing."
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '4291ceed',
            'metadata': {},
            'outputs': [],
            'source': [
                "# Impute missing director and cast with 'Unknown'\n",
                "df['director'] = df['director'].fillna('Unknown')\n",
                "df['cast'] = df['cast'].fillna('Unknown')\n",
                '\n',
                "# Drop rows where date_added or rating is missing\n",
                "df = df.dropna(subset=['date_added', 'rating'])\n",
                '\n',
                '# Verify missing values after cleaning\n',
                "missing_after = df.isnull().sum()\n",
                "missing_after_df = pd.DataFrame({\n",
                "    'Total Missing': missing_after,\n",
                "    'Percentage': (missing_after / len(df)) * 100\n",
                "})\n",
                "missing_after_df = missing_after_df[missing_after_df['Total Missing'] > 0]\n",
                "print('Remaining missing values after cleaning:')\n",
                'display(missing_after_df)\n',
                '\n',
                "print(f'\\nDataset shape after cleaning: {df.shape}')"
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'faefad09',
            'metadata': {},
            'source': [
                '## 2. Datetime Parsing & Temporal Analysis\n',
                '\n',
                '### 2.1 Parse `date_added` and extract temporal features\n',
                '\n',
                "We need to strip whitespace and convert `date_added` to pandas datetime, then extract `added_year`, `added_month_name`, and `added_day_name`."
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'faefad09',
            'metadata': {},
            'outputs': [],
            'source': [
                '# 1. Strip whitespace and convert to datetime\n',
                "df['date_added'] = pd.to_datetime(df['date_added'].str.strip())\n",
                '\n',
                '# 2. Extract temporal features\n',
                "df['added_year'] = df['date_added'].dt.year\n",
                "df['added_month'] = df['date_added'].dt.month\n",
                "df['added_month_name'] = df['date_added'].dt.month_name()\n",
                "df['added_day_name'] = df['date_added'].dt.day_name()\n",
                '\n',
                '# Display the new columns\n',
                "print('Sample of new temporal columns:')\n",
                "display(df[['title', 'date_added', 'added_year', 'added_month_name', 'added_day_name']].head(10))"
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '658d363e',
            'metadata': {},
            'outputs': [],
            'source': [
                '# 3. Identify top 3 months with most titles added\n',
                "top_months = df['added_month_name'].value_counts().head(10)\n",
                "print('Top 10 months with most titles added:')\n",
                'display(top_months)\n',
                '\n',
                "plt.figure(figsize=(10, 6))\n",
                "top_months.plot(kind='barh', color='steelblue')\n",
                "plt.title('Top 10 Months with Most Titles Added to Netflix')\n",
                "plt.xlabel('Number of Titles')\n",
                'plt.gca().invert_yaxis()\n',
                'plt.show()'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': '41a752c8',
            'metadata': {},
            'source': [
                '## 3. Numeric Duration Extraction\n',
                '\n',
                '### 3.1 Parse duration for movies and TV shows\n',
                '\n',
                "For movies, extract the minute count from the `duration` column (e.g., '90 min' -> 90). For TV shows, extract the season count into a new `seasons` column."
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '41a752c8',
            'metadata': {},
            'outputs': [],
            'source': [
                "df['duration_clean'] = df['duration'].astype(str)\n",
                '\n',
                "movie_mask = df['type'] == 'Movie'\n",
                "df.loc[movie_mask, 'duration_minutes'] = df.loc[movie_mask, 'duration_clean'].str.extract('(\\d+)').astype(float)\n",
                '\n',
                "df.loc[~movie_mask, 'seasons'] = df.loc[~movie_mask, 'duration_clean'].str.extract('(\\d+)').astype(float)\n",
                '\n',
                "movie_durations = df[movie_mask]['duration_minutes'].dropna()\n",
                "print('Movie durations summary statistics:')\n",
                'display(movie_durations.describe())\n',
                '\n',
                "plt.figure(figsize=(10, 6))\n",
                "plt.hist(movie_durations, bins=30, color='darkorange', edgecolor='black')\n",
                "plt.title('Distribution of Movie Durations')\n",
                "plt.xlabel('Duration (minutes)')\n",
                "plt.ylabel('Number of Movies')\n",
                'plt.xlim(0, 300)\n',
                'plt.show()'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'a55de303',
            'metadata': {},
            'source': [
                '## 4. Duration Bins with `np.select`\n',
                '\n',
                '### 4.1 Categorize movie durations using `np.select`\n',
                '\n',
                "Categorize movie durations into 'Short' (< 60 min), 'Feature' (60-120 min), and 'Long' (> 120 min). Calculate the percentage share of each category."
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'a55de303',
            'metadata': {},
            'outputs': [],
            'source': [
                'conditions = [\n',
                "    df.loc[movie_mask, 'duration_minutes'] < 60,\n",
                "    (df.loc[movie_mask, 'duration_minutes'] >= 60) & (df.loc[movie_mask, 'duration_minutes'] <= 120),\n",
                "    df.loc[movie_mask, 'duration_minutes'] > 120\n",
                ']\n',
                '\n',
                "choices = ['Short', 'Feature', 'Long']\n",
                '\n',
                "movie_df = df[movie_mask].copy()\n",
                "movie_df['duration_category'] = np.select(conditions, choices, default='Unknown')\n",
                '\n',
                "duration_counts = movie_df['duration_category'].value_counts()\n",
                "duration_percent = (duration_counts / len(movie_df) * 100).round(1)\n",
                '\n',
                "print('Movie Duration Categories:')\n",
                'display(duration_counts)\n',
                "print('\\nPercentage share:')\n",
                'display(duration_percent)\n',
                '\n',
                "plt.figure(figsize=(8, 8))\n",
                "labels = [f'{cat}\\n({pct}%)' for cat, pct in zip(duration_counts.index, duration_percent)]\n",
                "plt.pie(duration_counts, labels=labels, autopct='', colors=['#4c72b0', '#55a868', '#c44e52'])\n",
                "plt.title('Movie Duration Categories')\n",
                "plt.axis('equal')\n",
                'plt.show()'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'df5ea453',
            'metadata': {},
            'source': [
                '## 5. Exploding Delimited Strings (Countries)\n',
                '\n',
                '### 5.1 Split comma-separated strings in `country` and find top 10 contributing countries\n',
                '\n',
                "Use `.explode()` to create a flat series where each row has a single country, strip whitespace, and determine the top 10 countries."
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'df5ea453',
            'metadata': {},
            'outputs': [],
            'source': [
                "df['country_list'] = df['country'].astype(str).str.split(',')\n",
                '\n',
                "country_exploded = df['country_list'].explode()\n",
                '\n',
                "country_counts = country_exploded.str.strip().value_counts().head(10)\n",
                '\n',
                "print('Top 10 Countries:')\n",
                'display(country_counts)\n',
                '\n',
                "plt.figure(figsize=(10, 6))\n",
                "country_counts.plot(kind='barh', color='teal')\n",
                "plt.title('Top 10 Countries on Netflix')\n",
                "plt.xlabel('Number of Titles')\n",
                'plt.gca().invert_yaxis()\n',
                'plt.show()'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'c6d621cf',
            'metadata': {},
            'source': [
                '## 6. Genre Intersection Filtering\n',
                '\n',
                '### 6.1 Filter titles under both \'Documentaries\' AND \'International Movies\' released between 2018-2022\n',
                '\n',
                "Find titles that fall simultaneously under both genres and were released 2018-2022 (inclusive). Return title, director, and release year."
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'c6d621cf',
            'metadata': {},
            'outputs': [],
            'source': [
                "df['listed_in_list'] = df['listed_in'].astype(str).str.split(',')\n",
                "df_exploded = df.explode('listed_in_list')\n",
                '\n',
                "doc_intl_mask = df_exploded['listed_in_list'].str.strip().isin(['Documentaries', 'International Movies'])\n",
                "doc_intl_titles = df_exploded[doc_intl_mask]\n",
                '\n',
                "doc_intl_filtered = doc_intl_titles[doc_intl_titles['release_year'].between(2018, 2022)]\n",
                '\n',
                "result = doc_intl_filtered[['title', 'director', 'release_year']].drop_duplicates()\n",
                '\n',
                "print(f'Found {len(result)} titles matching the criteria:')\n",
                'display(result.head(20))'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'a2910ce6',
            'metadata': {},
            'source': [
                '## 7. Cast Frequency Ranking\n',
                '\n',
                '### 7.1 Split and explode the `cast` column, filter out \'Unknown\', and find top 10 most frequently credited actors\n',
                '\n',
                "Explode the cast column to get individual actors, then count their frequencies."
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'a2910ce6',
            'metadata': {},
            'outputs': [],
            'source': [
                "df['cast_list'] = df['cast'].astype(str).str.split(',')\n",
                "cast_exploded = df['cast_list'].explode()\n",
                '\n',
                "cast_clean = cast_exploded.str.strip()\n",
                "cast_clean = cast_clean[cast_clean != 'Unknown']\n",
                '\n',
                "top_actors = cast_clean.value_counts().head(10)\n",
                '\n',
                "print('Top 10 Most Frequently Credited Actors:')\n",
                'display(top_actors)\n',
                '\n',
                "plt.figure(figsize=(10, 6))\n",
                "top_actors.plot(kind='barh', color='purple')\n",
                "plt.title('Top 10 Most Frequently Credited Actors on Netflix')\n",
                "plt.xlabel('Number of Appearances')\n",
                'plt.gca().invert_yaxis()\n',
                'plt.show()'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'f5c88457',
            'metadata': {},
            'source': [
                '## 8. Decade Aggregation with NumPy Floor Division\n',
                '\n',
                '### 8.1 Create a `decade` column using integer floor division: `(release_year // 10) * 10`\n',
                '\n',
                "Compute the count and ratio of TV Shows to Movies produced in each decade."
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'f5c88457',
            'metadata': {},
            'outputs': [],
            'source': [
                "df['decade'] = (df['release_year'] // 10) * 10\n",
                '\n',
                "decade_type_counts = df.groupby(['decade', 'type']).size().unstack(fill_value=0)\n",
                '\n',
                "decade_type_counts['ratio'] = decade_type_counts['Movie'] / decade_type_counts['TV Show']\n",
                '\n',
                "print('Movies vs TV Shows per decade:')\n",
                'display(decade_type_counts)\n',
                '\n',
                "decade_type_counts['Movie'].plot(kind='area', figsize=(12, 6), color='steelblue', label='Movies')\n",
                "decade_type_counts['TV Show'].plot(kind='area', figsize=(12, 6), color='orange', label='TV Shows')\n",
                "plt.title('Movies and TV Shows Produced Per Decade')\n",
                "plt.xlabel('Decade')\n",
                "plt.ylabel('Count')\n",
                'plt.legend()\n',
                'plt.show()'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': '70170fb0',
            'metadata': {},
            'source': [
                '## 9. Contingency Matrix (`pd.crosstab`) to NumPy Array\n',
                '\n',
                '### 9.1 Generate a cross-tabulation table between `rating` (rows) and `type` (columns)\n',
                '\n',
                "Convert this contingency table into a pure 2D NumPy array matrix for downstream numerical or Chi-squared testing."
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '70170fb0',
            'metadata': {},
            'outputs': [],
            'source': [
                "ct = pd.crosstab(df['rating'], df['type'])\n",
                '\n',
                "print('Contingency Table (Rating vs Type):')\n",
                'display(ct)\n',
                '\n',
                "ct_array = ct.to_numpy()\n",
                "print('\\nAs NumPy array:')\n",
                'print(ct_array)\n',
                "print(f'\\nShape: {ct_array.shape}')"
            ]
        },
        {
            'cell_type': 'markdown',
            'id': '65a325f3',
            'metadata': {},
            'source': [
                '## 10. Text Length Quantiles with NumPy\n',
                '\n',
                '### 10.1 Compute the word count of each title\'s `description`\n',
                '\n',
                "Using `np.quantile()`, calculate the 25th, 50th (median), 75th, 90th, and 99th percentiles of description lengths."
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '65a325f3',
            'metadata': {},
            'outputs': [],
            'source': [
                "df['description_word_count'] = df['description'].astype(str).str.split().apply(len)\n",
                '\n',
                'quantiles = [0.25, 0.50, 0.75, 0.90, 0.99]\n',
                'quantile_values = np.quantile(df["description_word_count"], quantiles)\n',
                '\n',
                "print('Description Length Quantiles:')\n",
                "for q, v in zip(quantiles, quantile_values):\n",
                "    print(f'  {q*100}th percentile: {v:.1f} words')\n",
                '\n',
                "plt.figure(figsize=(10, 6))\n",
                "plt.hist(df['description_word_count'], bins=50, color='brown', edgecolor='black')\n",
                "plt.title('Distribution of Description Word Counts')\n",
                "plt.xlabel('Number of Words in Description')\n",
                "plt.ylabel('Number of Titles')\n",
                "plt.xlim(0, df['description_word_count'].quantile(0.99))\n",
                'plt.show()'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': '1a46d054',
            'metadata': {},
            'source': [
                '## Summary & Best Practices\n',
                '\n',
                '- **NumPy** excels at fast, low-level array transformations, mathematical vectorization (`np.where`, `np.select`, `np.log1p`), and percentile calculations.\n',
                '- **Pandas** excels at labeled data wrangling, grouping (`groupby`, `pivot_table`), datetime manipulation, and string processing.\n',
                '- Keep data types clean and always handle edge cases (like division by zero, skewness, and group-level missingness) before feeding data into downstream machine learning pipelines.\n',
                '- Visualizations should be clear, labeled, and use consistent styling for readability.'
            ]
        }
    ],
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python',
            'version': '3.x'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 5
}

with open('Dataset 2 Netflix Movies and TV Shows - Data Cleaning and Visualization.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)
print('Notebook written successfully!')