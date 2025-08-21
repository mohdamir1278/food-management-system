Food Distribution Management Project — EDA Explanation
Exploratory Data Analysis (EDA) is the crucial first step to understanding the data collected in the food distribution system. It helps uncover patterns, trends, and anomalies, allowing us to make informed decisions to reduce food wastage and improve distribution efficiency.

Key Data Sources:

Providers: Who donates food and their details.

Receivers: Who receives food and their details.

Food Inventory: Details about food items including type, quantity, expiry dates, and locations.

Claims: Records of food claims by receivers with status like completed or wasted.

Main EDA Focus Areas

Distribution of Providers and Receivers:

Analyze counts and locations of providers and receivers.


this is SQL query:
(select city, 'providers' as entity_type, count(*) as total
from providers
group by city
union all 
select city, 'receivers' as entity_type, count(*) as total
from receivers
group by city
order by city, entity_type)



Understand geographic coverage and concentration.



Food Inventory Exploration:

Break down food by categories (types) to see what is most donated.

SQL query:(select name,address,city,contact from providers
where city='city'

select r.name as receive_name, count(c.claim_id) as total_claim
from claims c
inner join receivers r
on r.receiver_id=c.receiver_id
group by r.name
order by total_claim desc)

output image of the query:<img width="436" height="699" alt="Screenshot 2025-08-21 172633" src="https://github.com/user-attachments/assets/95f427bf-8ed3-463b-984e-d6ad8f55e8a8" />

Check quantity distributions and highlight inventory close to expiry.

Analyze food availability across locations.

Claims and Wastage Analysis:

Study claim statuses to identify how much food is successfully distributed versus wasted.

Track wastage by food categories and locations.

Calculate average quantities claimed by receivers to understand demand.

Expiry and Risk Assessment:

Identify items with approaching or past expiry dates to prioritize distribution.

Link expiry data with wastage claims to find key problem areas.

Visualization & Insights
Use bar charts to show provider counts by city or donation quantities by type.
<img width="880" height="437" alt="download" src="https://github.com/user-attachments/assets/6aeaa50b-7a24-4cad-8dec-ecc258285239" />

Heatmaps or charts that correlate food categories with wastage and expiry.

Timelines or line graphs to observe trends over time (if date info is available).

Not give/providing any because there no food wastage in this datasets.
