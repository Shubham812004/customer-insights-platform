DROP TABLE IF EXISTS clean_bank_churn;

CREATE TABLE clean_bank_churn AS
SELECT
    "CustomerId" AS customer_id,
    "CreditScore" AS credit_score,
    "Geography" AS geography,
    "Gender" AS gender,
    "Age" AS age,
    "Tenure" AS tenure,
    "Balance" AS balance,
    "NumOfProducts" AS num_of_products,
    "HasCrCard" AS has_cr_card, 
    "IsActiveMember" AS is_active_member, 
    "EstimatedSalary" AS estimated_salary,
    "Exited" AS churn 
FROM
    raw_bank_churn;

DROP TABLE IF EXISTS clean_olist_transactions;


CREATE TABLE clean_olist_transactions AS
SELECT
    o."order_id",
    c."customer_unique_id",
    o."order_purchase_timestamp",
    p."payment_value"
FROM
    raw_olist_orders o
JOIN
    raw_olist_customers c ON o."customer_id" = c."customer_id"
JOIN
    raw_olist_order_payments p ON o."order_id" = p."order_id"
WHERE
    o."order_status" = 'delivered' 
    AND p."payment_value" > 0; 

CREATE INDEX idx_customer_unique_id ON clean_olist_transactions (customer_unique_id);
CREATE INDEX idx_order_purchase_timestamp ON clean_olist_transactions (order_purchase_timestamp);

