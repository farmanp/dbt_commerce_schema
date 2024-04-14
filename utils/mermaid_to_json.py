import re
import json

# Sample input as a string (ideally, this would be read from a file)
mermaid_data = """
```mermaid
    orders {
        varchar order_id
        varchar customer_id
        varchar market_id
        varchar store_id
        varchar payment_id
        datetime order_created_datetime
        datetime order_last_modified_datetime
        decimal order_total
        varchar currency_name
        varchar order_status
        decimal order_tax
        decimal order_shipping
        decimal order_discount
        decimal order_subtotal
        decimal platform_commission_fees
        decimal tax_rate
        decimal refund_amount
        decimal total_weight
        varchar order_source
        varchar sales_channel
        varchar cart_token
        varchar email
        varchar store_employee_id
        datetime order_cancel_datetime
        varchar financial_status
        varchar fulfillment_status
        varchar cancel_reason
        varchar shipping_address_id
        varchar billing_address_id
        varchar customer_language
        varchar browser_ip
        varchar referring_site
        varchar order_tags
        varchar order_notes
        boolean business_order_flag
        boolean expedited_shipping_order_flag
        boolean prime_order_flag
        boolean replacement_order_flag
        boolean refund_flag
        boolean taxes_included_flag
        varchar notes
    }
    order_line_items {
        varchar order_item_id
        varchar order_id
        varchar currency_name
        varchar product_variant_store_id
        datetime order_item_created_datetime
        datetime order_item_last_modified_datetime
        decimal order_item_price
        decimal order_item_tax
        decimal order_item_shipping
        decimal order_item_discount
        decimal order_item_subtotal
        decimal order_item_quantity
        decimal order_quantity_fulfilled
        decimal product_cost
        varchar order_item_status
        decimal platform_commission_fees
        boolean gift_card_flag
        boolean shipped_item_flag
        boolean refund_flag
    }
    order_payments {
        varchar payment_id 
        varchar order_id
        varchar payment_gateway_name   
    }    
    transactions {
        varchar transaction_id
        varchar order_id 
        datetime transaction_datetime
        varchar transaction_gateway
        varchar transaction_source
        varchar transaction_type
        varchar transaction_status
        varchar transaction_authorization
        varchar currency_name
        decimal transaction_amount
        varchar avs_result_code
        varchar credit_card_bin
        varchar credit_card_company
        varchar cvv_result_code
        datetime transaction_created_datetime  
    }
    fulfillments{
        varchar fulfillment_id
        varchar order_id
        varchar fulfillment_status
        varchar fulfillment_location_id
        varchar fulfillment_location
        varchar customer_address_id
        varchar shipment_status
        varchar tracking_company
        varchar tracking_number
        varchar currency_name
        decimal fulfillment_cost
        decimal shipping_cost
        datetime fulfillment_datetime
        date estimated_arrival_date
        datetime delivery_datetime
        datetime fulfillment_created_datetime
        datetime fulfullment_updated_datetime
    }
    order_item_fulfillments{
        varchar order_item_fulfillment_id
        varchar order_item_id
        varchar fulfillment_id
        varchar product_variant_id
        varchar product_variant_sku
        decimal order_item_quantity
        decimal order_item_quantity_to_fulfill
        varchar item_fulfillment_status 
    }
    refunds {
        varchar refund_id
        varchar order_id
        varchar employee_id
        datetime refund_datetime
        varchar currency_name
        decimal refund_amount
    }
    refund_line_items{
        varchar refund_line_item_id
        varchar refund_id
        varchar order_id
        varchar order_item_id
        decimal refund_item_quantity
        decimal refund_amount
        decimal refund_tax_amount   
    }
    product_listings {
        varchar product_list_id
        varchar product_variant_store_id
        varchar market_id
        varchar store_id
        decimal product_price
        varchar currency_name   
        datetime product_listing_created_datetime
        datetime product_listing_last_modified_datetime
        varchar product_listing_status
        varchar product_listing_description
    }
    products {
        varchar product_id
        varchar product_name
        varchar product_type
        varchar product_tags
        varchar supplier_id
        datetime product_created_datetime
        datetime product_modified_datetime
        varchar product_status
        varchar product_description
        varchar product_category
        varchar product_subcategory
        varchar product_brand
        varchar product_department
    }
    product_variants {
        varchar product_variant_id
        varchar product_id
        varchar supplier_id
        varchar product_variant_name
        varchar product_variant_sku
        datetime product_variant_created_datetime
        datetime product_variant_last_modified_datetime
        varchar product_variant_color
        varchar product_variant_size
        varchar product_variant_weight
        varchar product_variant_weight_unit
        varchar product_variant_status
        varchar barcode
        boolean inventory_tracked_flag
        boolean requires_shipping_flag 
        varchar country_of_origin
        varchar image_url
        int image_position
    }
    inventory_history {
        varchar product_variant_store_id
        datetime inventory_datetime
        varchar store_id
        decimal inventory_quantity
    }
    price_history {
        varchar product_variant_store_id
        datetime price_datetime
        decimal price 
        varchar currency
        varchar store_id
        varchar market_id
        datetime price_start_datetime
        datetime price_end_datetime
    }
    stores {
        varchar store_id
        varchar market_id
        varchar location_name
        varchar address1
        varchar address2
        varchar city
        varchar state
        varchar country
        varchar zip
        varchar phone_number  
        date store_open_date
        date store_close_date
    }
    inventory_cost_history {
        varchar product_variant_store_id
        datetime cost_datetime
        varchar store_id
        decimal cost
        varchar currency
        datetime received_datetime
        decimal quantity_received
        varchar supplier_id
    }
    collections {
        varchar collection_id
        varchar product_variant_store_id
        varchar store_id
        datetime collection_created_datetime
        datetime collection_last_modified_datetime
    }
    product_variant_stores {
        varchar product_variant_store_id
        varchar product_variant_id
        varchar store_id
        datetime product_variant_store_created_datetime
        datetime product_variant_store_last_modified_datetime
    }
    product_reviews {
        varchar review_id
        varchar product_id
        varchar customer_id
        varchar review
        decimal rating
        datetime product_review_created_datetime
        datetime product_review_last_modified_datetime
        varchar review_status
        varchar review_language
        varchar review_market
    }
    customers {
        varchar customer_id
        varchar first_name
        varchar last_name
        varchar email
        varchar address_id
        varchar customer_status
        varchar phone_number
        datetime customer_created_datetime
        datetime customer_last_modified_datetime
    }
    customer_addresses {
        varchar customer_address_id
        varchar customer_id
        varchar address1
        varchar address2
        varchar city
        varchar state
        varchar zip
        varchar country
        varchar address_type
        datetime address_created_datetime
        datetime address_last_modified_datetime
    }
    suppliers {
        varchar supplier_id
        varchar supplier_name
        varchar supplier_address
        varchar supplier_city
        varchar supplier_state
        varchar supplier_zip
        varchar supplier_country
        varchar supplier_phone
        varchar supplier_email
        varchar supplier_status
        datetime supplier_created_datetime
        datetime supplier_last_modified_datetime
    }
    audiences {
        varchar audience_id
        varchar customer_id
        datetime audience_created_datetime
        datetime audience_last_modified_datetime
    }
    ad_campaigns {
        varchar ad_campaign_id
        varchar audience_id
        varchar ad_platform_id
        datetime ad_campaign_created_datetime
        datetime ad_campaign_last_modified_datetime
    }
    ads {
        varchar ad_id
        varchar ad_campaign_id
        datetime ad_created_datetime
        datetime ad_last_modified_datetime
    }
    ad_impressions {
        varchar ad_impression_id
        varchar ad_id
        datetime ad_impression_datetime
    }
    email_campaigns {
        varchar email_campaign_id
        varchar audience_id
        datetime email_campaign_created_datetime
    }
    emails {
        varchar email_id
        varchar email_campaign_id
        datetime email_created_datetime
    }
    emails_sent {
        varchar email_sent_id
        varchar email_id
        datetime email_sent_datetime
    }
    customer_email_addresses {
        varchar customer_email_address_id
        varchar customer_id
        varchar email_address
        datetime email_address_created_datetime
        datetime email_address_last_modified_datetime
    }
    calendar{
        date date
        varchar day_of_week
        varchar month
        varchar year
        varchar fiscal_week
        varchar fiscal_month
        varchar fiscal_quarter
        varchar fiscal_year
    }
    currency{
        varchar currency_name
        date currency_date
        decimal currency_exchange_rate
    }
    markets {
        varchar market_id
        varchar market_name
    }
    store_markets {
        varchar store_market_id
        varchar store_id
        varchar market_id
    }
    product_suppliers { 
        varchar product_supplier_id
        varchar product_id
        varchar supplier_id
        datetime product_supplier_created_datetime
        datetime product_supplier_last_modified_datetime
    }
    households {
        varchar household_id
        varchar customer_id
    }
    employees {
        varchar employee_id
        varchar store_employee_id
        varchar first_name
        varchar last_name  
        date employee_start_date
        date employee_end_date
    }
    order_discounts{
        varchar order_discount_id
        varchar order_id
        varchar discount_code
        varchar discount_type
        varchar currency_name
        decimal discount_amount  
    }
    order_shipping_services{
        varchar order_shipping_line_id
        varchar order_id
        varchar order_item_id
        varchar shipping_code
        varchar shipping_title 
        varchar carrier_identifier     
    }
       events_base_cart_viewed {
        varchar products
        varchar total
        varchar anonymous_id
        varchar user_id
        varchar original_timestamp
        varchar context_ip
        varchar context_source
        varchar context_library_version
        varchar context_library_name
        varchar context_referrer
        varchar context_page_title
        varchar context_user_agent
        varchar context_page_height
        varchar context_debug
        varchar context_page_referrer
        varchar context_page_path
        varchar context_os_name
        varchar context_page_url
        varchar context_locale
        varchar context_timezone
        varchar context_page_width
        varchar context_campaign_name
        varchar context_campaign_medium
        varchar context_campaign_source
        varchar context_page_search
        varchar context_page_hash
        varchar event_id
    }
    events_base_checkout_created {
        varchar affiliation
        varchar coupon
        varchar currency
        decimal discount
        varchar products
        decimal tax
        decimal value
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_library_name
        varchar context_locale
        varchar context_user_agent
        varchar context_source
        varchar context_library_version
        varchar context_ip
        varchar context_passed_ip
        varchar event_id
    }
    events_base_checkout_updated {
        varchar affiliation
        varchar coupon
        varchar currency
        decimal discount
        varchar products
        decimal tax
        decimal value
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_source
        varchar context_locale
        varchar context_user_agent
        varchar context_library_name
        varchar context_ip
        varchar context_library_version
        varchar context_passed_ip
        varchar event_id
    }
    events_base_identifies {
        varchar address_city
        varchar address_street
        varchar email
        varchar first_name
        varchar last_name
        varchar name
        varchar phone
        varchar anonymous_id
        varchar user_id
        varchar external_customer_id
        varchar created_at
        datetime original_timestamp
        varchar context_traits_first_name
        varchar context_traits_phone
        varchar context_locale
        varchar context_library_name
        varchar context_passed_ip
        varchar context_user_agent
        varchar context_ip
        varchar context_source
        varchar context_traits_email
        varchar context_traits_last_name
        varchar context_traits_created_at
        varchar context_traits_external_customer_id
        varchar context_library_version
        varchar context_traits_name
        varchar context_traits_context_session_id
        varchar context_traits_address_street
        varchar context_traits_context_ip
        varchar context_traits_address_country_code
        varchar context_traits_address_state
        varchar context_traits_context_client_id
        varchar context_traits_context_anonymous_id
        varchar context_traits_address_postal_code
        varchar context_traits_address_city
        varchar context_traits_addresses
        varchar context_traits_context_page_url
        varchar context_page_path
        varchar context_traits_context_page_search
        varchar context_traits_context_debug
        varchar context_traits_context_os_name
        varchar context_traits_context_page_width
        varchar context_page_width
        varchar context_traits_context_page_title
        varchar context_traits_context_page_referrer
        varchar context_os_name
        varchar context_referrer
        varchar context_page_height
        varchar context_traits_context_library_version
        varchar context_page_search
        varchar context_traits_context_locale
        varchar context_traits_context_page_height
        varchar context_traits_context_user_agent
        varchar context_page_url
        varchar context_timezone
        varchar context_page_referrer
        varchar context_traits_context_app
        varchar context_traits_context_library_name
        varchar context_page_title
        varchar context_traits_context_referrer
        varchar context_traits_context_initialized
        varchar context_debug
        varchar context_traits_context_timezone
        varchar context_traits_context_page_path
        varchar context_traits_context_offline
        varchar context_campaign_gclid
        varchar context_traits_context_campaign_gclid
        varchar context_traits_context_page_hash
        varchar context_page_hash
        varchar context_campaign_term
        varchar context_traits_context_campaign_source
        varchar context_traits_context_campaign_term
        varchar context_traits_context_campaign_medium
        varchar context_campaign_name
        varchar context_campaign_source
        varchar context_traits_context_campaign_name
        varchar context_campaign_medium
        varchar context_campaign_profile
        varchar context_campaign_id
        varchar context_traits_context_campaign_id
        varchar context_traits_context_campaign_profile
        varchar context_campaign_content
        varchar context_traits_context_campaign_content
        varchar event_id
    }
    events_base_logged_in {
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_ip
        varchar context_library_name
        varchar context_source
        varchar context_library_version
        varchar context_page_width
        varchar context_timezone
        varchar context_user_agent
        varchar context_page_url
        varchar context_page_referrer
        varchar context_os_name
        varchar context_debug
        varchar context_page_title
        varchar context_page_height
        varchar context_locale
        varchar context_referrer
        varchar context_page_path
        varchar context_page_search
        varchar event_id
    }
    events_base_order_cancelled {
        varchar billing_address_address
        varchar billing_address_city
        varchar billing_address_country
        varchar billing_address_first_name
        varchar billing_address_last_name
        varchar billing_address_postal_code
        varchar billing_address_state
        varchar currency
        varchar order_id
        decimal revenue
        decimal shipping
        varchar status
        decimal subtotal
        decimal total
        varchar type
        varchar value
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_library_name
        varchar context_source
        varchar context_library_version
        varchar context_ip
        varchar context_passed_ip
        varchar context_locale
        varchar context_user_agent
        varchar event_id
    }
    events_base_order_completed {
        varchar affiliation
        varchar billing_address_address
        varchar billing_address_city
        varchar billing_address_country
        varchar billing_address_first_name
        varchar billing_address_last_name
        varchar billing_address_phone
        varchar billing_address_postal_code
        varchar billing_address_state
        varchar cart_id
        varchar coupon
        varchar currency
        decimal discount
        varchar event_text
        varchar order_id
        varchar payment_type
        varchar products
        decimal revenue
        decimal shipping
        varchar status
        decimal subtotal
        decimal tax
        decimal total
        varchar type
        decimal value
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_passed_ip
        varchar context_user_agent
        varchar context_source
        varchar context_library_name
        varchar context_library_version
        varchar context_locale
        varchar context_ip
        varchar event_id
    }
    events_base_order_updated {
        varchar affiliation
        varchar billing_address_address
        varchar billing_address_city
        varchar billing_address_country
        varchar billing_address_first_name
        varchar billing_address_last_name
        varchar billing_address_phone
        varchar billing_address_postal_code
        varchar billing_address_state
        varchar cart_id
        varchar coupon
        varchar currency
        decimal discount
        varchar event_text
        varchar order_id
        varchar payment_type
        varchar products
        decimal revenue
        varchar shipping
        varchar status
        decimal subtotal
        decimal tax
        decimal total
        varchar type
        decimal value
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_user_agent
        varchar context_ip
        varchar context_locale
        varchar context_library_name
        varchar context_passed_ip
        varchar context_source
        varchar context_library_version
        varchar event_id
    }
    events_base_pages {
        varchar _hash
        varchar height
        varchar name
        varchar path
        varchar referrer
        varchar search
        varchar title
        varchar url
        varchar width
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_ip
        varchar context_library_version
        varchar context_library_name
        varchar context_timezone
        varchar context_page_hash
        varchar context_page_search
        varchar context_page_height
        varchar context_locale
        varchar context_page_url
        varchar context_page_referrer
        varchar context_campaign_medium
        varchar context_campaign_name
        varchar context_debug
        varchar context_os_name
        varchar context_referrer
        varchar context_campaign_gclid
        varchar context_page_title
        varchar context_page_path
        varchar context_user_agent
        varchar context_campaign_term
        varchar context_campaign_source
        varchar context_page_width
        varchar context_campaign_content
        varchar context_campaign_profile
        varchar context_campaign_id
        varchar event_id
    }
    events_base_product_added {
        varchar brand
        varchar category
        varchar image_url
        varchar name
        varchar position
        decimal price
        varchar product_id
        decimal quantity
        varchar sku
        varchar url
        varchar variant
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_library_name
        varchar context_ip
        varchar context_library_version
        varchar context_source
        varchar context_page_height
        varchar context_page_path
        varchar context_os_name
        varchar context_debug
        varchar context_locale
        varchar context_page_url
        varchar context_referrer
        varchar context_page_search
        varchar context_timezone
        varchar context_user_agent
        varchar context_page_referrer
        varchar context_page_width
        varchar context_page_title
        varchar context_campaign_gclid
        varchar context_campaign_content
        varchar context_campaign_medium
        varchar context_campaign_name
        varchar context_campaign_source
        varchar context_campaign_term
        varchar context_page_hash
        varchar context_campaign_profile
        varchar context_campaign_id
        varchar event_id
    }
    events_base_product_list_viewed {
        varchar category
        varchar list_id
        varchar products
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_source
        varchar context_library_name
        varchar context_ip
        varchar context_library_version
        varchar context_campaign_name
        varchar context_page_title
        varchar context_page_width
        varchar context_campaign_medium
        varchar context_timezone
        varchar context_locale
        varchar context_os_name
        varchar context_page_referrer
        varchar context_page_height
        varchar context_page_search
        varchar context_debug
        varchar context_user_agent
        varchar context_referrer
        varchar context_page_url
        varchar context_campaign_source
        varchar context_page_path
        varchar context_campaign_term
        varchar context_campaign_gclid
        varchar context_campaign_content
        varchar context_page_hash
        varchar context_campaign_profile
        varchar context_campaign_id
        varchar event_id
    }
    events_base_product_removed {
        varchar position
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_ip
        varchar context_library_name
        varchar context_library_version
        varchar context_source
        varchar context_user_agent
        varchar context_locale
        varchar context_page_url
        varchar context_page_path
        varchar context_page_referrer
        varchar context_page_title
        varchar context_os_name
        varchar context_debug
        varchar context_referrer
        varchar context_page_height
        varchar context_timezone
        varchar context_page_width
        varchar event_id
    }
    events_base_products_searched {
        varchar query
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_source
        varchar context_ip
        varchar context_library_version
        varchar context_library_name
        varchar context_page_search
        varchar context_os_name
        varchar context_locale
        varchar context_referrer
        varchar context_page_referrer
        varchar context_page_height
        varchar context_timezone
        varchar context_page_title
        varchar context_page_path
        varchar context_page_url
        varchar context_user_agent
        varchar context_debug
        varchar context_page_width
        varchar event_id
    }
    events_base_signed_up {
        varchar email
        varchar first_name
        varchar last_name
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_library_name
        varchar context_library_version
        varchar context_ip
        varchar context_source
        varchar context_timezone
        varchar context_referrer
        varchar context_os_name
        varchar context_page_height
        varchar context_user_agent
        varchar context_locale
        varchar context_debug
        varchar context_page_referrer
        varchar context_page_url
        varchar context_page_width
        varchar context_page_title
        varchar context_page_path
        varchar event_id
    }
    events_base_subscription_activated {
        varchar charge_interval_frequency
        datetime created_at
        varchar has_queued_charges
        varchar is_skippable
        varchar is_swappable
        varchar max_retries_reached
        varchar next_charge_scheduled_at
        varchar order_billing_address_address
        varchar order_billing_address_city
        varchar order_billing_address_country
        varchar order_billing_address_email
        varchar order_billing_address_first_name
        varchar order_billing_address_last_name
        varchar order_billing_address_phone
        varchar order_billing_address_postal_code
        varchar order_billing_address_state
        varchar order_coupon
        varchar order_currency
        decimal order_discount
        varchar order_id
        varchar order_interval_frequency
        varchar order_interval_unit
        varchar order_order_id
        varchar order_products
        decimal order_revenue
        varchar order_status
        decimal order_subtotal
        decimal order_tax
        decimal order_total
        varchar order_type
        decimal order_value
        varchar products
        varchar sku_override
        datetime started_at
        varchar status
        datetime updated_at
        varchar user_id
        datetime original_timestamp
        varchar context_source
        varchar context_library_version
        varchar context_ip
        varchar context_library_name
        varchar event_id
    }
    events_base_subscription_cancelled {
        varchar charge_interval_frequency
        datetime created_at
        varchar end_reason
        datetime ended_at
        varchar has_queued_charges
        varchar is_skippable
        varchar is_swappable
        varchar max_retries_reached
        varchar order_billing_address_address
        varchar order_billing_address_city
        varchar order_billing_address_country
        varchar order_billing_address_email
        varchar order_billing_address_first_name
        varchar order_billing_address_last_name
        varchar order_billing_address_phone
        varchar order_billing_address_postal_code
        varchar order_billing_address_state
        varchar order_cart_id
        varchar order_coupon
        varchar order_currency
        decimal order_discount
        varchar order_id
        varchar order_interval_frequency
        varchar order_interval_unit
        varchar order_order_id
        varchar order_products
        decimal order_revenue
        varchar order_status
        decimal order_subtotal
        decimal order_tax
        decimal order_total
        varchar order_type
        decimal order_value
        varchar products
        varchar sku_override
        datetime started_at
        varchar status
        datetime updated_at
        varchar user_id
        datetime original_timestamp
        varchar context_source
        varchar context_library_name
        varchar context_library_version
        varchar context_ip
        varchar event_id
    }
    events_base_subscription_created {
        varchar charge_interval_frequency
        datetime created_at
        varchar has_queued_charges
        varchar is_skippable
        varchar is_swappable
        varchar max_retries_reached
        datetime next_charge_scheduled_at
        varchar order_billing_address_address
        varchar order_billing_address_city
        varchar order_billing_address_country
        varchar order_billing_address_email
        varchar order_billing_address_first_name
        varchar order_billing_address_last_name
        varchar order_billing_address_phone
        varchar order_billing_address_postal_code
        varchar order_billing_address_state
        varchar order_coupon
        varchar order_currency
        decimal order_discount
        varchar order_id
        varchar order_interval_frequency
        varchar order_interval_unit
        varchar order_order_id
        varchar order_products
        decimal order_revenue
        varchar order_status
        decimal order_subtotal
        decimal order_tax
        decimal order_total
        varchar order_type
        varchar order_value
        varchar products
        varchar sku_override
        datetime started_at
        varchar status
        datetime updated_at
        varchar user_id
        datetime original_timestamp
        varchar context_library_name
        varchar context_ip
        varchar context_source
        varchar context_library_version
        varchar event_id
    }
    events_base_tracks {
        varchar event
        varchar event_text
        varchar anonymous_id
        varchar user_id
        datetime original_timestamp
        varchar context_source
        varchar context_ip
        varchar context_library_version
        varchar context_library_name
        varchar context_user_agent
        varchar context_passed_ip
        varchar context_locale
        varchar event_id
    }
    events_base_users {
        varchar address_city
        varchar address_country_code
        varchar address_postal_code
        varchar address_state
        varchar address_street
        varchar addresses
        datetime created_at
        varchar email
        varchar external_customer_id
        varchar first_name
        varchar last_name
        varchar name
        varchar phone
        varchar anonymous_id
        varchar user_id
        varchar context_passed_ip
        varchar context_traits_email
        varchar context_traits_first_name
        varchar context_library_name
        varchar context_traits_phone
        varchar context_user_agent
        varchar context_source
        varchar context_traits_external_customer_id
        varchar context_traits_created_at
        varchar context_traits_last_name
        varchar context_locale
        varchar context_library_version
        varchar context_ip
        varchar context_traits_address_country_code
        varchar context_traits_name
        varchar context_traits_address_city
        varchar context_traits_context_anonymous_id
        varchar context_traits_address_street
        varchar context_traits_address_state
        varchar context_traits_context_client_id
        varchar context_traits_address_postal_code
        varchar context_traits_context_ip
        varchar context_traits_context_session_id
        varchar context_traits_addresses
        varchar context_traits_context_page_title
        varchar context_page_width
        varchar context_traits_context_page_url
        varchar context_traits_context_referrer
        varchar context_traits_context_os_name
        varchar context_traits_context_locale
        varchar context_page_referrer
        varchar context_traits_context_library_name
        varchar context_os_name
        varchar context_page_path
        varchar context_page_height
        varchar context_traits_context_initialized
        varchar context_page_search
        varchar context_debug
        varchar context_traits_context_app
        varchar context_traits_context_page_referrer
        varchar context_traits_context_page_search
        varchar context_traits_context_library_version
        varchar context_traits_context_debug
        varchar context_traits_context_user_agent
        varchar context_traits_context_timezone
        varchar context_traits_context_offline
        varchar context_traits_context_page_height
        varchar context_timezone
        varchar context_referrer
        varchar context_traits_context_page_path
        varchar context_page_title
        varchar context_traits_context_page_width
        varchar context_page_url
        varchar context_campaign_gclid
        varchar context_traits_context_campaign_gclid
        varchar context_traits_context_page_hash
        varchar context_page_hash
        varchar context_traits_context_campaign_source
        varchar context_campaign_term
        varchar context_traits_context_campaign_name
        varchar context_campaign_source
        varchar context_traits_context_campaign_medium
        varchar context_traits_context_campaign_term
        varchar context_campaign_medium
        varchar context_campaign_name
        varchar context_campaign_profile
        varchar context_traits_context_campaign_profile
        varchar context_traits_context_campaign_id
        varchar context_campaign_id
        varchar context_traits_context_campaign_content
        varchar context_campaign_content
    }
    events_base_cart_line_items {
        varchar event_type
        varchar event_id
        varchar cart_id
        datetime original_timestamp
        varchar brand
        varchar category
        varchar imageurl
        varchar name
        varchar position
        decimal price
        varchar product_id
        decimal quantity
        varchar sku
        varchar url
        varchar variant
        varchar unnested_product_column
    }
    events_base_checkout_line_items {
        varchar event_type
        varchar event_id
        varchar cart_id
        datetime original_timestamp
        varchar is_refunded
        varchar line_item_id
        varchar name
        varchar position
        decimal price
        varchar product_id
        decimal quantity
        varchar sku
        varchar variant
        varchar unnested_product_column
    }
    events_base_order_line_items {
        varchar event_type
        varchar order_id
        datetime original_timestamp
        varchar is_refunded
        varchar line_item_id
        varchar name
        varchar position
        decimal price
        varchar product_id
        decimal quantity
        varchar sku
        varchar variant
        varchar unnested_product_column
    }
    events_base_product_list_viewed_products {
        varchar event_type
        varchar event_id
        datetime original_timestamp
        varchar list_id
        varchar brand
        varchar category
        varchar imageurl
        varchar name
        varchar position
        decimal price
        varchar product_id
        decimal quantity
        varchar sku
        varchar url
        varchar variant
        varchar unnested_product_column
    }
```
"""

def parse_mermaid(mermaid_str):
    # Finding all entity blocks
    entities_raw = re.findall(r'(\w+)\s*\{([\s\S]*?)\}', mermaid_str)

    entities = {}
    relationships = []
    entity_started = False  # Flag to track if entity parsing has started

    # Parsing entities
    for entity, fields_str in entities_raw:
        fields = []
        for line in fields_str.strip().split('\n'):
            parts = line.strip().split()
            if len(parts) >= 2:
                field_type, field_name = parts[:2]
                description = ' '.join(parts[2:])
                fields.append({'field_name': field_name, 'type': field_type, 'description': description})
        entities[entity] = fields
        entity_started = True  # Set flag to True when first entity is encountered

    # Parsing relationships
    if entity_started:  # Only parse relationships if entity_started is True
        relationship_lines = re.findall(r'(\w+)\s+([\|\}\{]+)--([\|o\{\}]+)\s*(\w+)\s*:\s*"(\d+\.\.\d+|\d+)"', mermaid_str)
        for from_entity, from_card, to_card, to_entity, cardinality in relationship_lines:
            relationships.append({
                'from': from_entity,
                'from_card': from_card,
                'to_card': to_card,
                'to': to_entity,
                'cardinality': cardinality
            })

    return entities, relationships

def convert_to_json(entities, relationships):
  """
  Converts the given entities and relationships into a JSON schema.

  Args:
    entities (list): A list of entities.
    relationships (list): A list of relationships.

  Returns:
    str: A JSON string representing the schema.

  """
  schema = {'entities': entities, 'relationships': relationships}
  return json.dumps(schema, indent=4)


# entities, relationships = parse_mermaid(mermaid_data)
# json_output = convert_to_json(entities, relationships)

# with open('models.json', 'w') as f:
#     f.write(json_output)

def execute(file_name):
    data = open(file_name, 'r').read()
    entities, relationships = parse_mermaid(data)
    json_output = convert_to_json(entities, relationships)    
    with open('dbt_def.json', 'w') as f:
        f.write(json_output)

execute('../erd.md')