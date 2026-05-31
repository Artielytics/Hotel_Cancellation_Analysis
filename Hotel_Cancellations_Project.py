# ==================================================
# Hotel Booking Cancellation Prediction
# Author: Artie Zarskus
# Date: June 2026
#
# Portfolio Project:
# SQL, EDA, Logistic Regression and Industry Insight
# ==================================================

# ==================================================
# IMPORTS
# ==================================================
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# ==================================================
# DATA LOADING
# ==================================================

import os


df = pd.read_csv('data/Hotel_Reservations.csv')


conn = sqlite3.connect('data/Hotel_Reservations.db')


df.to_sql('Hotel_Reservations', conn, if_exists='replace' , index=False)

# ==================================================
# EXPLORATORY DATA ANALYSIS
# ==================================================

# query = """
# # SELECT booking_status, COUNT(*) as total
# # FROM Hotel_Reservations
# # GROUP BY booking_status
# # """
# # result = pd.read_sql(query, conn)
# # print(result,"\n")
# #
# # #lead time vs cancellation query
# # query = """
# # SELECT
# #     CASE
# #          WHEN lead_time < 7 THEN '0-7 days'
# #             WHEN lead_time < 30 THEN '7-30 days'
# #             WHEN lead_time < 90 THEN '30-90 days'
# #             ELSE '90+ days'
# #         END as lead_time_group,
# #         booking_status,
# #         COUNT(*) AS total
# #         FROM Hotel_Reservations
# #     GROUP BY lead_time_group, booking_status
# #     ORDER BY
# #     CASE
# #     WHEN lead_time_group = '0-7 days' THEN 1
# #     WHEN lead_time_group = '7-30 days' THEN 2
# #     WHEN lead_time_group = '30-90 days' THEN 3
# #     WHEN lead_time_group = '90+ days' THEN 4
# #     END;
# #     """
# result = pd.read_sql(query, conn)
# print(result,"\n")
#
# #pivot data for plotting
# pivot_df = result.pivot(index='booking_status', columns='lead_time_group', values='total')
# #create bar chart/grouped
# pivot_df = pivot_df[
#     ['0-7 days',
#      '7-30 days',
#      '30-90 days',
#      '90+ days']
# ]
# ax = pivot_df.plot(
#     kind='bar',
#     figsize=(9,5),
#     color=[
#         '#d0e1f9',  # light blue
#         '#74a9cf',  # medium blue
#         '#2b8cbe',  # darker blue
#         '#045a8d'   # dark blue
#     ]
#
# )
# #label/title
# plt.title('Lead Time and Booking Cancellation Patterns')
# plt.xlabel('Booking Status')
# plt.ylabel('Number of Bookings')
#
# plt.xticks(rotation=0) # rotate labels
# plt.show()
#
# #Price vs cancellation
# query = """
# SELECT
#     booking_status,
#     ROUND(AVG(avg_price_per_room), 2) AS avg_price
#     FROM Hotel_Reservations
#     GROUP BY booking_status;
# """
# result = pd.read_sql(query, conn)
# print(result,"\n")
#
# #Data separated into groups
# cancelled = df[df['booking_status'] == 'Canceled']['avg_price_per_room']
# not_cancelled = df[df['booking_status'] == 'Not_Canceled']['avg_price_per_room']
# plt.boxplot([cancelled, not_cancelled],
#             tick_labels=['Canceled','Not_Canceled'])
# #titles/labels
# plt.title('Room price By Booking Status')
# plt.ylabel('Average Price Per Room')
# plt.show()
#
#
# #Previous cancellations impact
# query = """
# SELECT
#
#     CASE
#         WHEN no_of_previous_cancellations = 0 THEN 'None'
#         WHEN no_of_previous_cancellations <= 2 THEN 'Low (1-2)'
#         ELSE 'High (3+)'
#     END AS cancellation_history,
#
#     SUM(CASE
#         WHEN booking_status = 'Canceled' THEN 1
#         ELSE 0
#     END) AS cancelled_bookings,
#
#     COUNT(*) AS total_bookings,
#
#     ROUND(
#         100.0 * SUM(CASE
#             WHEN booking_status = 'Canceled' THEN 1
#             ELSE 0
#         END) / COUNT(*),
#         2
#     ) AS cancellation_rate
#
# FROM Hotel_Reservations
#
# GROUP BY cancellation_history
#
# ORDER BY
#     CASE
#         WHEN cancellation_history = 'None' THEN 1
#         WHEN cancellation_history = 'Low (1-2)' THEN 2
#         ELSE 3
#     END;
# """
# result = pd.read_sql(query, conn)
# print(result.to_string(),"\n")
#
# #Rpeated Guests
# query = """
# SELECT repeated_guest,
#     booking_status,
#     COUNT(*) AS total
#     FROM Hotel_Reservations
#     GROUP BY repeated_guest, booking_status;
#     """
# result = pd.read_sql(query, conn)
# print(result,"\n")
#
#
# rate_df = pd.DataFrame({
#     'Guest Type': ['Non-Repeat', 'Repeat'],
#     'Cancellation Rate': [33.6, 1.7]
# })
#
# rate_df.plot(
#     x='Guest Type',
#     y='Cancellation Rate',
#     kind='bar',
#     legend=False,
# color=['teal']
# )
#
# plt.title('Cancellation Rate by Guest Type')
# plt.ylabel('Cancellation Rate (%)')
# plt.xticks(rotation=0)
#
# plt.show()
#
# #Special Requests
# query = """
# SELECT
#     no_of_special_requests,
#
#     SUM(
#         CASE
#             WHEN booking_status = 'Canceled' THEN 1
#             ELSE 0
#         END
#     ) AS cancelled_bookings,
#
#     COUNT(*) AS total_bookings,
#
#     ROUND(
#         100.0 *
#         SUM(
#             CASE
#                 WHEN booking_status='Canceled' THEN 1
#                 ELSE 0
#             END
#         )
#         / COUNT(*),
#         2
#     ) AS cancellation_rate
#
# FROM Hotel_Reservations
#
# GROUP BY no_of_special_requests
#
# ORDER BY no_of_special_requests;
# """
# result = pd.read_sql(query, conn)
# print(result,"\n")
#
# result.plot(
#     x='no_of_special_requests',
#     y='cancellation_rate',
#     kind='bar',
#     legend=False,
# color=['red','orange','gold','green','blue','purple']
# )
#
# plt.title('Cancellation Rate by Number of Special Requests')
# plt.xlabel('Number of Special Requests')
# plt.ylabel('Cancellation Rate (%)')
#
# plt.xticks(rotation=0)
#
# plt.show()
#
#
# #Group size vs cancellations
# query = """
# SELECT
#     (no_of_adults + no_of_children) AS total_guests,
#
#     SUM(
#         CASE
#             WHEN booking_status='Canceled' THEN 1
#             ELSE 0
#         END
#     ) AS cancelled_bookings,
#
#     COUNT(*) AS total_bookings,
#
#     ROUND(
#         100.0 *
#         SUM(
#             CASE
#                 WHEN booking_status='Canceled' THEN 1
#                 ELSE 0
#             END
#         )
#         / COUNT(*),
#         2
#     ) AS cancellation_rate
#
# FROM Hotel_Reservations
#
# GROUP BY total_guests
#
# ORDER BY total_guests;
# """
# result = pd.read_sql(query, conn)
#
# filtered_result = result[
#     result['total_bookings'] >= 10
# ].copy() # creates new dataframe
# print(filtered_result)
#
# # Clean formatting
# filtered_result['total_guests'] = (
#     filtered_result['total_guests']
#     .astype(int)
# )
#
# filtered_result['cancellation_rate'] = (
#     filtered_result['cancellation_rate']
#     .map(lambda x: f'{x:.2f}%')
# )
#
# # Create figure
# fig, ax = plt.subplots(figsize=(8,4))
#
# # Remove axes
# ax.axis('off')
#
# # Create table
# table = ax.table(
#     cellText=filtered_result.values,
#     colLabels=filtered_result.columns,
#     loc='center'
# )
#
# # Adjust appearance
# table.auto_set_font_size(False)
# table.set_fontsize(10)
# table.scale(1.2, 1.5)
#
# for (row, col), cell in table.get_celld().items():
#     if row == 0:
#         cell.set_text_props(weight='bold')
#         cell.set_facecolor('#d9eaf7')
#
# plt.title(
#     'Cancellation Rates by Group Size',
#     pad=20
# )

#plt.show()
# ==================================================
# FEATURE ENGINEERING
# ==================================================
df['total_guests'] = (
    df['no_of_adults']
    + df['no_of_children']
)
features = [

'lead_time',
'repeated_guest',
'no_of_special_requests',
'total_guests',
'avg_price_per_room',
'no_of_previous_cancellations'

]

df['booking_status'] = (
    df['booking_status']
    .map({
        'Canceled':1,
        'Not_Canceled':0
    })
)
X = df[features]

y = df['booking_status']

# ==================================================
# MODEL BUILDING
# ==================================================

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42

)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

#train model
from sklearn.linear_model import LogisticRegression


model = LogisticRegression(
    class_weight='balanced'
)

model.fit(
    X_train,
    y_train
)

predictions = model.predict(X_test)

#evaluation
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

print(
accuracy_score(
y_test,
predictions
)
)

print(
classification_report(
y_test,
predictions
)
)

print(
confusion_matrix(
y_test,
predictions
)
)

coef_df = pd.DataFrame({
    'Feature': features,
    'Coefficient': model.coef_[0]
})

print(
coef_df.sort_values(
    by='Coefficient',
    ascending=False
))

# ==================================================
# MODEL EVALUATION
# ==================================================

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

cm = confusion_matrix(
    y_test,
    predictions
)

fig, ax = plt.subplots(figsize=(6,5))

im = ax.imshow(cm)

# Labels
ax.set_xticks([0,1])
ax.set_yticks([0,1])

ax.set_xticklabels([
    'Not Cancelled',
    'Cancelled'
])

ax.set_yticklabels([
    'Not Cancelled',
    'Cancelled'
])

ax.set_xlabel('Predicted')
ax.set_ylabel('Actual')

plt.title('Confusion Matrix')

labels = [
    [f'True Negative\n{cm[0, 0]}',
     f'False Positive\n{cm[0, 1]}'],

    [f'False Negative\n{cm[1, 0]}',
     f'True Positive\n{cm[1, 1]}']
]

for i in range(2):
    for j in range(2):
        ax.text(
            j,
            i,
            labels[i][j],
            ha='center',
            va='center'
        )

plt.colorbar(im)

plt.tight_layout()

plt.show()