
# Sequence Diagram: eCommerce System

```mermaid
sequenceDiagram
    actor Customer
    Customer ->> eCommerce System: Select Product
    eCommerce System ->> Product: Retrieve Product Details
    Product -->> eCommerce System: Product Information
    Customer ->> eCommerce System: Add to Cart & Checkout
    eCommerce System ->> Order: Create Order
    Customer ->> eCommerce System: Initiate Payment
    eCommerce System ->> Payment Gateway: Send Payment Details
    Payment Gateway -->> eCommerce System: Payment Status
    eCommerce System -->> Customer: Confirm Order (if Payment Successful)
    eCommerce System ->> Order: Update Order Status
```
```

# Legend:
- **Customer**: The user who is buying the product.
- **eCommerce System**: The platform where the transaction takes place.
- **Product**: Represents the details and information of a product.
- **Order**: A generated order upon checkout.
- **Payment Gateway**: Third-party service used to process payments.
```
