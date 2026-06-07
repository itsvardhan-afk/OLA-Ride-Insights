import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

sns.set_theme(style="whitegrid")

df = pd.read_excel('OLA_DataSet.xlsx')

print("Total Rows:", df.shape[0])
print("Total Columns:", df.shape[1])
print()
print("Column Names:")
print(df.columns.tolist())
print()
print("Data Types:")
print(df.dtypes)
print()
print("Missing Values:")
print(df.isnull().sum())
print()
print("Booking Status:")
print(df['Booking_Status'].value_counts())
print()
print("Vehicle Type:")
print(df['Vehicle_Type'].value_counts())
print()
print("Payment Method:")
print(df['Payment_Method'].value_counts())
print()

df['Booking_Status'].value_counts().plot(kind='bar', color=['green','red','orange','blue'])
plt.title('Booking Status')
plt.tight_layout()
plt.savefig('plot1_booking_status.png')
plt.show()

df['Vehicle_Type'].value_counts().plot(kind='barh', color='steelblue')
plt.title('Rides by Vehicle Type')
plt.tight_layout()
plt.savefig('plot2_vehicle_type.png')
plt.show()

df['Payment_Method'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Payment Methods')
plt.ylabel('')
plt.tight_layout()
plt.savefig('plot3_payment.png')
plt.show()

df['Canceled_Rides_by_Customer'].value_counts().plot(kind='barh', color='salmon')
plt.title('Customer Cancellation Reasons')
plt.tight_layout()
plt.savefig('plot4_cancellations.png')
plt.show()

sns.histplot(df[df['Ride_Distance']>0]['Ride_Distance'], bins=30, kde=True, color='teal')
plt.title('Ride Distance Distribution')
plt.tight_layout()
plt.savefig('plot5_distance.png')
plt.show()

print("DONE! Step 1 complete. Check your folder for 5 chart images.")