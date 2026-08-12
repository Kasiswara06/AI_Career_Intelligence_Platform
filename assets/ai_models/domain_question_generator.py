import random
from ai_models.answer_generator import generate_model_answer_package

DOMAIN_QUESTION_BANK = {
    "Python Development": [
        {
            "question": "What is the difference between a list and a tuple in Python?",
            "category": "Technical",
            "question_type": "Technical",
            "difficulty": "Easy",
            "model_answer": "A list is a mutable collection, meaning its elements can be changed after creation. A tuple is immutable, meaning its elements cannot be changed after creation.",
            "explanation": "Lists allow element modification, addition, and removal. Tuples cannot be modified after creation. Because tuples are immutable, Python allocates a fixed memory block for them, making them slightly faster and memory-efficient.",
            "example": "```python\nnumbers = [1, 2, 3]\nnumbers[0] = 10\n\nvalues = (1, 2, 3)\n```\nThe list can be modified, while the tuple cannot be modified.",
            "key_points": [
                "List → Mutable",
                "Tuple → Immutable",
                "List uses []",
                "Tuple uses ()"
            ],
            "interview_tip": "Mention mutability and give a simple example."
        },
        {
            "question": "What are Python's built-in data types and how does dynamic typing work?",
            "category": "Technical",
            "question_type": "Technical",
            "difficulty": "Easy",
            "model_answer": "Python features built-in types: int, float, str, list, tuple, dict, set, bool. In Python, variables are dynamically typed, meaning variable types are checked at runtime and variables bind to objects rather than declared types.",
            "explanation": "You don't need to declare variable types explicitly in Python. The interpreter determines the type based on the value assigned.",
            "example": "```python\nx = 10      # int\nx = 'Hello' # str (dynamically rebound)\n```",
            "key_points": [
                "Dynamic typing evaluates types at runtime",
                "Variables are references to objects",
                "Supports type hinting (`def add(a: int) -> int`)"
            ],
            "interview_tip": "Highlight that type hints in modern Python improve IDE autocompletion and static analysis without breaking dynamic typing."
        },
        {
            "question": "Explain decorators in Python and how `@classmethod` differs from `@staticmethod`.",
            "category": "Technical",
            "question_type": "Technical",
            "difficulty": "Medium",
            "model_answer": "Decorators wrap functions to alter behavior without modifying code. `@classmethod` receives `cls` as its first parameter to access class state, whereas `@staticmethod` receives no implicit first parameter and acts as a plain function bound to the class namespace.",
            "explanation": "Decorators utilize Python's first-class function capabilities. `@classmethod` is typically used for factory methods, while `@staticmethod` is used for utility functions related to the class.",
            "example": "```python\nclass Student:\n    school = 'Tech Academy'\n    \n    @classmethod\n    def get_school(cls):\n        return cls.school\n        \n    @staticmethod\n    def add(a, b):\n        return a + b\n```",
            "key_points": [
                "Decorators extend function behavior dynamically",
                "@classmethod receives `cls` argument",
                "@staticmethod receives no implicit first argument",
                "Preserve metadata using `functools.wraps`"
            ],
            "interview_tip": "Always mention `functools.wraps` when discussing custom decorators to preserve docstrings and signatures."
        },
        {
            "question": "How does Python memory management work under the hood (Reference Counting & GIL)?",
            "category": "Technical",
            "question_type": "Technical",
            "difficulty": "Hard",
            "model_answer": "CPython manages memory via PyMalloc, heap allocation, reference counting, and cyclic garbage collection. When an object's reference count drops to zero, its memory is freed immediately. Cyclic GC detects and breaks circular references.",
            "explanation": "The Global Interpreter Lock (GIL) ensures single-threaded execution of Python bytecode per process to maintain reference counting safety across C-extensions.",
            "example": "```python\nimport sys\na = []\nb = a\nprint(sys.getrefcount(a)) # 3 (a, b, and temporary arg in getrefcount)\n```",
            "key_points": [
                "Reference counting frees memory immediately when count hits 0",
                "Cyclic GC handles circular references",
                "GIL prevents parallel bytecode execution across native threads in CPython"
            ],
            "interview_tip": "Differentiate CPU-bound tasks (use Multiprocessing) from I/O-bound tasks (use Multithreading or AsyncIO)."
        }
    ],

    "Data Science": [
        {
            "question": "What is Exploratory Data Analysis (EDA)?",
            "category": "Technical",
            "question_type": "Technical",
            "difficulty": "Easy",
            "model_answer": "Exploratory Data Analysis, or EDA, is the process of examining and understanding a dataset using statistics and visualizations before building a machine learning model.",
            "explanation": "EDA allows data scientists to discover patterns, detect anomalies, check assumptions, test hypotheses, and verify feature relationships before committing to predictive modeling.",
            "example": "```python\nimport pandas as pd\nimport seaborn as sns\n\ndf = pd.read_csv('data.csv')\nprint(df.describe())\nsns.heatmap(df.corr(), annot=True)\n```",
            "key_points": [
                "Understand data distribution & skewness",
                "Detect missing values and outliers",
                "Identify relationships between features",
                "Select key predictive features for modeling"
            ],
            "interview_tip": "Mention the tools you use, such as Pandas, NumPy, Matplotlib, Seaborn, or Plotly."
        },
        {
            "question": "What is feature engineering and what are key techniques?",
            "category": "Technical",
            "question_type": "Technical",
            "difficulty": "Medium",
            "model_answer": "Feature engineering transforms raw dataset variables into meaningful representations that boost machine learning model accuracy and convergence speed.",
            "explanation": "Techniques include One-Hot Encoding, Ordinal Encoding for categorical variables, MinMax/Standard Scaling for numerical variables, Log transformations, and Polynomial features.",
            "example": "```python\nfrom sklearn.preprocessing import StandardScaler\nscaler = StandardScaler()\nX_scaled = scaler.fit_transform(X)\n```",
            "key_points": [
                "Categorical: One-Hot, Ordinal, Target Encoding",
                "Numerical: Standard Scaling, MinMax, Log Transform",
                "Prevents data leakage by scaling after train/test split"
            ],
            "interview_tip": "Emphasize fitting scalers only on training data to avoid data leakage."
        }
    ],

    "Machine Learning": [
        {
            "question": "What is overfitting in Machine Learning and how do you reduce it?",
            "category": "Technical",
            "question_type": "Technical",
            "difficulty": "Medium",
            "model_answer": "Overfitting occurs when a machine learning model learns the training data too closely, including its noise and unnecessary patterns. As a result, it performs very well on training data but poorly on unseen test data.",
            "explanation": "High model variance leads to memorization rather than learning general patterns. The model fits training samples too tightly.",
            "example": "```python\n# Detecting Overfitting\ntrain_acc = 0.99\ntest_acc = 0.62 # Large performance gap indicates overfitting\n```",
            "key_points": [
                "Use cross-validation (K-Fold)",
                "Apply L1/L2 Regularization",
                "Gather more training data",
                "Perform feature selection",
                "Apply Dropout for neural networks",
                "Reduce model complexity or prune decision trees"
            ],
            "interview_tip": "Always explain overfitting using the performance difference between training data and test data."
        },
        {
            "question": "What is the core difference between Supervised and Unsupervised Machine Learning?",
            "category": "Technical",
            "question_type": "Technical",
            "difficulty": "Easy",
            "model_answer": "Supervised learning trains models on labeled datasets (inputs X with ground truth target Y) for classification or regression. Unsupervised learning trains on unlabeled data (inputs X only) to discover inherent clusters, patterns, or lower-dimensional representations.",
            "explanation": "Supervised learning has direct error metrics against true labels. Unsupervised learning evaluates cluster cohesion or reconstruction loss.",
            "example": "Supervised: Spam Classification, House Price Prediction.\nUnsupervised: Customer Segmentation (K-Means), Dimensionality Reduction (PCA).",
            "key_points": [
                "Supervised → Labeled data (Input X + Target Y)",
                "Unsupervised → Unlabeled data (Input X only)",
                "Supervised tasks: Regression & Classification",
                "Unsupervised tasks: Clustering & Dimensionality Reduction"
            ],
            "interview_tip": "Give quick real-world examples for both (e.g. Fraud detection vs Customer segmentation)."
        }
    ],

    "SQL & Database": [
        {
            "question": "What is the difference between INNER JOIN and LEFT JOIN?",
            "category": "Technical",
            "question_type": "Technical",
            "difficulty": "Medium",
            "model_answer": "An INNER JOIN returns only rows that have matching values in both tables. A LEFT JOIN returns all rows from the left table and matching rows from the right table. If no match exists, the right-side columns contain NULL.",
            "explanation": "INNER JOIN filters out unmatched records from both sides. LEFT JOIN preserves all rows from the primary left table regardless of matches in the right table.",
            "example": "```sql\nSELECT e.name, d.department_name\nFROM employees e\nINNER JOIN departments d\nON e.department_id = d.department_id;\n```",
            "key_points": [
                "INNER JOIN → only matching records in both tables",
                "LEFT JOIN → all left records + matching right records",
                "Unmatched rows in LEFT JOIN yield NULL for right table columns"
            ],
            "interview_tip": "Mention that filtering right table columns in the WHERE clause can accidentally convert a LEFT JOIN into an INNER JOIN."
        },
        {
            "question": "What is the logical execution order of a SQL SELECT query?",
            "category": "Technical",
            "question_type": "Technical",
            "difficulty": "Easy",
            "model_answer": "The logical execution order of SQL statements is: 1) FROM, 2) ON, 3) JOIN, 4) WHERE, 5) GROUP BY, 6) HAVING, 7) SELECT, 8) DISTINCT, 9) ORDER BY, and 10) LIMIT / OFFSET.",
            "explanation": "Understanding this execution order explains why column aliases defined in the SELECT clause cannot be used inside WHERE or GROUP BY clauses, and why HAVING filters aggregated groups after GROUP BY.",
            "example": "```sql\nSELECT department_id, COUNT(*) AS emp_count\nFROM employees\nWHERE salary > 50000\nGROUP BY department_id\nHAVING COUNT(*) > 5\nORDER BY emp_count DESC;\n```",
            "key_points": [
                "FROM & JOIN run first to gather source data",
                "WHERE filters raw rows before aggregation",
                "GROUP BY & HAVING aggregate and filter groups",
                "SELECT & DISTINCT evaluate column expressions",
                "ORDER BY & LIMIT sort and slice final output"
            ],
            "interview_tip": "Explain why HAVING is needed alongside WHERE (WHERE filters individual rows before grouping, HAVING filters groups after aggregation)."
        }
    ]
}

def get_domain_questions(domain: str, target_role: str, difficulty: str = "Mixed", count: int = 10) -> list:
    """
    Retrieves or generates domain-tailored interview questions with COMPLETE MODEL ANSWERS.
    """
    diff_clean = difficulty.replace("🟢", "").replace("🟡", "").replace("🔴", "").replace("🔥", "").strip()

    domain_key = domain
    if domain not in DOMAIN_QUESTION_BANK:
        for k in DOMAIN_QUESTION_BANK.keys():
            if k.lower() in domain.lower() or domain.lower() in k.lower():
                domain_key = k
                break

    pool = DOMAIN_QUESTION_BANK.get(domain_key, DOMAIN_QUESTION_BANK["Python Development"])
    
    if diff_clean in ["Easy", "Medium", "Hard"]:
        filtered = [q for q in pool if q.get("difficulty") == diff_clean]
        if not filtered:
            filtered = pool
    else:
        filtered = pool

    questions = []
    for idx, q in enumerate(filtered):
        q_copy = dict(q)
        q_copy["domain"] = domain
        q_copy["role"] = target_role
        q_copy["question_id"] = idx + 1

        if not q_copy.get("explanation") or not q_copy.get("key_points"):
            pkg = generate_model_answer_package(q_copy["question"], domain=domain, target_role=target_role, difficulty=q_copy.get("difficulty", "Medium"))
            q_copy["model_answer"] = q_copy.get("model_answer") or pkg["model_answer"]
            q_copy["explanation"] = pkg["explanation"]
            q_copy["example"] = q_copy.get("example") or pkg["example"]
            q_copy["key_points"] = pkg["key_points"]
            q_copy["interview_tip"] = pkg["interview_tip"]

        questions.append(q_copy)

    result = []
    while len(result) < count:
        for q in questions:
            if len(result) >= count:
                break
            result.append(dict(q))

    return result[:count]
