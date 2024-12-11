# Electrical Calculations

**Simplify the life of electrical practitioners with professional-grade calculations.**

---

## Purpose

Electrical Calculations is a web application designed to enhance the professional journey of electrical practitioners by providing a cost-effective alternative to expensive electrical software. The platform simplifies complex electrical calculations, making them accessible from any device—whether a desktop, mobile phone, or tablet. With no hardware requirements, the application leverages powerful servers to handle intensive tasks, allowing users to connect and operate seamlessly over the internet.

The platform also integrates access to extensive databases, including NEC standards and various industry-standard tables, further supporting precise and professional calculations.

Advanced features are available to subscribers, offering additional tools and functionalities to meet the needs of professionals.

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
- Subscription-based access to some advanced features (some features are in development).
- Future adds other engineering field calculations. (planning stage for development)

---

## Installation

- As for now, the application is not available online. 
- To run the application locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone <https://github.com/cloydbalongkit1/capstone_django_electrical.git>
   cd electrical-calculations
   ```

2. Set up a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
   ```bash
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


6. Important: Setup you own Stripe account and replace it with your own stripe keys in the **settings.py**. This is because the app is not yet in online. 

```bash
STRIPE_PUBLIC_KEY = os.environ.get('stripe_api_public_key')
STRIPE_SECRET_KEY = os.environ.get('stripe_api_secret_key')
STRIPE_PRICE_ID = os.environ.get('stripe_price_id')
STRIPE_WEBHOOK_SECRET = os.environ.get('stripe_webhook_secret_key')
```
- Stripe documentation will tell you how to get this keys.

---

## Usage

- Use the application as a web-based tool for electrical engineering calculations and theories.
- Ensure you have a subscription to unlock more features and also knowledgeable in Electrical Engineering theories to utilize them effectively.

---

## Contribution

This application is a **capstone project for CS50W**, developed solely by me. Special thanks to the creators of libraries like ElectricPy, NumPy, Matplotlib, and others, which were instrumental in building this tool.

---

## Contact

If you have any feedback or suggestions, please reach out at: [[cloydbalongkit1@gmail.com](mailto\:your-email@example.com)].

---

## Challeges

Development of this application involves significant effort, particularly in handling user-input data for plotting with Matplotlib. The plotted outputs are managed using the Tkinter library. To ensure efficient storage and retrieval, the plots are converted to byte format and saved in memory. This will be an PNG based rendered to browsers. If the user decides to save their work, both the byte-formatted solution and the corresponding input values are stored in the database, serving as a reference for future use. This approach ensures data integrity and usability over time.

