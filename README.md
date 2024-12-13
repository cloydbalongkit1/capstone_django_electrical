# Electrical Calculations

**Simplify the life of electrical practitioners with professional-grade calculations.**

---

## Purpose

Electrical Calculations is a web application designed to enhance the professional journey of electrical practitioners by providing a cost-effective alternative to expensive electrical software. The platform simplifies complex electrical calculations, making them accessible from any device—whether a desktop, mobile phone, or tablet. With no hardware requirements, the application leverages powerful servers to handle intensive tasks, allowing users to connect and operate seamlessly over the internet.

The platform also integrates access to extensive databases, including NEC standards and various industry-standard tables, further supporting precise and professional calculations.

Advanced features are available to subscribers, offering additional tools and functionalities to meet the needs of professionals.

---

## Distinctiveness and Complexity

#### Requirements

- Knowledge of Electrical Theories is required for implementing and solving complex functions.
- Familiarity with data manipulation libraries like NumPy and Matplotlib is essential for generating and plotting outputs.
- Matplotlib-generated outputs (via Tkinter) are converted into an in-memory bytes buffer using Buffered I/O. These outputs are saved to the database for future reference if the user decides to store their work.

#### Application Structure

- **Main Folder**: `electrical_calculations`
  - **`electrical_calculations`**: Manages the entire application.
  - **`circuits`**: Handles computations, home, about, and user profile.
  - **`payments`**: Manages Stripe payment integration.

---

## Technology Stack

- **Backend**: Python, Django
- **Libraries**: ElectricPy, NumPy, Matplotlib
- **Frontend**: JavaScript
- **Payment Integration**: Stripe

---

## Key Features

- Perform accurate and professional-grade electrical engineering calculations.
- User-friendly interface for ease of use.
- Contact Us support. Access for superuser only.
- Subscription-based access to advanced features (some features under development).
- Future plans include adding calculations for other engineering fields (currently in the planning stage).
---

## Usage

- Use the application as a web-based tool for electrical engineering calculations and theories.
- Ensure you have a subscription to unlock additional features.
- A solid understanding of Electrical Engineering theories is recommended to fully utilize the platform's capabilities.

---

## Installation

Currently, the application is not available online. To run the application locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/cloydbalongkit1/capstone_django_electrical.git
   cd electrical-calculations
   ```

2. Set up a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

5. Access the application in your browser at `http://127.0.0.1:8000`.

6. **Important**: Set up your own Stripe account and replace the placeholder keys in **`settings.py`** with your own Stripe API keys. Since the app is not yet online, this step is required for testing payment functionality.

   ```python
   STRIPE_PUBLIC_KEY = os.environ.get('stripe_api_public_key')
   STRIPE_SECRET_KEY = os.environ.get('stripe_api_secret_key')
   STRIPE_PRICE_ID = os.environ.get('stripe_price_id')
   STRIPE_WEBHOOK_SECRET = os.environ.get('stripe_webhook_secret_key')
   ```

   Refer to Stripe's documentation for instructions on obtaining these keys.



---

## Contribution

This application is a **capstone project for CS50W**, developed solely by me. Special thanks to the creators of libraries like ElectricPy, NumPy, Matplotlib, and others, which were instrumental in building this tool.

---

## Contact

For feedback or suggestions, feel free to reach out at: [cloydbalongkit1@gmail.com](mailto:cloydbalongkit1@gmail.com).

---

## Challenges

Development of this application involves significant effort, particularly in handling user-input data for plotting with Matplotlib. The plotted outputs are rendered using the Tkinter library, then converted to PNG format and served to browsers. To ensure efficient storage and retrieval, these outputs are saved in memory as byte streams and stored in the database if the user decides to save them. Input values are also saved alongside the plots, providing a comprehensive reference for future use. This approach ensures data integrity and usability over time.

