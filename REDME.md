# 🧶 Crochet

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-success.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-informational.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-Open%20Source-green.svg)](#-license)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](#)
[![Deploy](https://img.shields.io/badge/Deploy-Railway-purple.svg)](https://railway.app)

---

<p align="center">
  <b>- MyCrochet -</b><br>
  A Django-based web application for custom and pesonalized clothing management.<br>
</p>

<p align="center">
  <a href="#-demo"> Demo</a> •
  <a href="#-setup"> Setup</a> •
  <a href="#-features"> Features</a> •
  <a href="#-code-highlights"> Code Highlights</a> •
  <a href="#-future-improvements"> To-Do</a> •
  <a href="#-license"> License</a>
</p>

---

## - Overview

**MyCrochet** is a full-featured **Django web application** designed for a **tailor-made clothing e-commerce**.  
It handles **user registration**, **client measurement tracking**, **shopping cart management**, and **sales analytics**.  
Focused on ORM optimization, class-based views, and advanced model relationships.

---

## - Features

-  **User Authentication** (Custom `UserCreationForm` + linked `Client` model)
-  **Client Profiles** with measurements and gender selection
-  **Cart and Orders** with dynamic quantity management
-  **Appointment Booking** (no overlapping logic)
-  **Analytics Dashboard** using `annotate`, `aggregate`, and `TruncDate`
-  **Role-based Access** via `AdminRequiredMixin` and decorators
-  **Invoice generation** with **WeasyPrint**
-  **PostgreSQL** as the main database for real production reliability

---

##  Setup

###  1. Clone the Repository

```bash
git clone https://github.com/your-username/crochet.git
cd crochet

2. Create and Activate a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the project root:

SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/crochet

5. Run Migrations and Start the Server

python manage.py migrate
python manage.py runserver

Then visit → http://127.0.0.1:8000/ 🎉

⸻

Code Highlights

AdminRequiredMixin

A mixin used to protect admin-only views (class-based):

from django.contrib.auth.mixins import UserPassesTestMixin

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.client_profile.role == "ADMIN"

For function-based views, a decorator version can be used:

from django.contrib.auth.decorators import user_passes_test

def admin_required(user):
    return user.is_authenticated and user.client_profile.role == "ADMIN"

@user_passes_test(admin_required)
def dashboard_view(request):
    ...


⸻

🧮 Aggregations & Analytics

Using annotate, Sum, and TruncDate to calculate daily sales totals:

from django.db.models import Sum
from django.db.models.functions import TruncDate
from .models import Order

daily_sales = (
    Order.objects.annotate(date=TruncDate("created_at"))
    .values("date")
    .annotate(total=Sum("total_amount"))
)


⸻

📆 No Overlapping Appointments

existing = Appointment.objects.filter(
    date=appointment_date,
    start_time__lt=end_time,
    end_time__gt=start_time
)
if existing.exists():
    raise ValidationError("This time slot is already booked.")


⸻

🧾 Invoice PDF with WeasyPrint

from weasyprint import HTML

html = render_to_string("invoice_template.html", {"order": order})
pdf = HTML(string=html).write_pdf()


⸻

📊 Admin Dashboard

A data-driven view showing summarized insights like:
	•	Total sales per day
	•	Top clients and top products
	•	Appointment frequency and user activity

All built with Django ORM and optimized query aggregation.

⸻

🌍 Demo (Coming Soon)

🚀 Hosted on Railway

🔗 Live Demo: ....

🧪 Demo Credentials:

Admin:
username: admin
password: Yoursecretpassword!

User:
username: user
password: Yoursecretpassword!



⸻

🖼️ Screenshots ------------------------

⸻

🧭 Future Improvements
	•	🛍️ Add product categories & image upload
	•	💳 Integrate Stripe for payments
	

⸻

🧑‍💻 Author

Salvatore Lombardo
- Guitarist • Software Developer • Music Teacher • Artistic Director 
- Based in Sicily, Italy
- salvolombardoj@gmail.com 
- Portfolio : https://github.com/SalvoLombardo

⸻

⚖️ License

This project is open source and intended for learning and portfolio purposes.
Feel free to fork, modify, or expand this repository.

⸻



```



⸻

