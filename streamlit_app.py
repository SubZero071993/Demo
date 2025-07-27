import pandas as pd
from datetime import datetime

# البيانات من الجدول
data = [
    ["Cios Select FD VA20", "22-07-25", 20087, "warehouse", "", ""],
    ["Cios Connect", "25-05-25", 21521, "Al-Rawdhah Hospital (until we submit Cios Select)", "Ayman Tamimi", ""],
    ["Cios Fusion", "27-07-25", 31181, "warehouse", "", ""],
    ["Cios Alpha VA20", "29-05-25", 13020, "Al-Hayyat Hospital (until they receive their C-arm)", "Ammar", ""],
    ["Cios Alpha VA30", "03-07-25", 43815, "Aster Sanad Hospital", "Ammar", ""],
    ["Cios Spin VA30", "10-07-25", 50097, "Johns Hopkins Aramco Hospital", "Ayman Tamimi", "Ali"]
]

columns = [
    "Demo C-arm Model", 
    "Delivery Date", 
    "Serial #", 
    "Current Location", 
    "Account Manager", 
    "Application Specialist"
]

# إنشاء DataFrame
df = pd.DataFrame(data, columns=columns)

# تحويل عمود التاريخ إلى datetime
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"], format="%d-%m-%y")

# تحديد تاريخ اليوم (حسب طلبك = 27-07-2025)
today = datetime(2025, 7, 27)

# حساب عدد الأيام
df["Days in Site"] = (today - df["Delivery Date"]).dt.days

# إضافة عمود "هل الجهاز خربان؟"
df["Is Broken?"] = False  # افتراضيًا ما فيه جهاز خربان

# طباعة الجدول
print(df)
