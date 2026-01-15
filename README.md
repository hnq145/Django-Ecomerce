# Django E-commerce Platform

A comprehensive e-commerce solution built with Django, featuring a responsive design, product filtering, shopping cart, and order management.

## 🚀 Features

- **Product Catalog**: Browse products with advanced filtering (Price, Category) and sorting capabilities.
- **Product Details**: comprehensive product pages with:
  - Customer Reviews and breakdown.
  - Related Products suggestions.
  - "Recently Viewed" products tracking.
- **Shopping Cart**: Fully functional cart system with coupon code support.
- **Order Management**: content-rich checkout process and order tracking.
- **User Interface**:
  - Responsive design using Bootstrap.
  - Dark Mode support.
  - Interactive elements (Quick View, customized alerts).

## 🛠 Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 4
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **Utilities**:
  - `django-crispy-forms` for form rendering.
  - `Pillow` for image processing.

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (optional but recommended)

### Steps

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/Django-Ecomerce.git
    cd Django-Ecomerce
    ```

2.  **Create and Activate Virtual Environment**

    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Migration**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create Superuser (Admin)**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Development Server**

    ```bash
    python manage.py runserver
    ```

    Access the application at `http://127.0.0.1:8000/`

## 🛒 Usage

1.  **Admin Panel**: Log in to `http://127.0.0.1:8000/admin/` to manage products, categories, coupons, and orders.
2.  **Storefront**: Browse products, add items to cart, apply coupons, and proceed to checkout.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the project.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
