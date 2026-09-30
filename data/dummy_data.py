"""Dummy ServiceNow ticket and Splunk log data used to simulate real integrations."""

DUMMY_TICKETS = {
    "INC0012345": {
        "ticket_id": "INC0012345",
        "short_description": "Payment API returning intermittent 500 errors",
        "priority": "P1 - Critical",
        "category": "Payments",
        "affected_service": "payment-service",
        "sla_status": "Breached (opened 6h ago, SLA target 4h)",
        "opened_at": "2026-09-25T02:15:00Z",
        "description": (
            "Multiple customers reported failed checkouts. Payment API intermittently "
            "returns HTTP 500 during peak traffic. Started after the 02:00 UTC deploy."
        ),
    },
    "INC0012678": {
        "ticket_id": "INC0012678",
        "short_description": "Users unable to log in via SSO",
        "priority": "P2 - High",
        "category": "Authentication",
        "affected_service": "auth-service",
        "sla_status": "At risk (opened 2h ago, SLA target 4h)",
        "opened_at": "2026-09-25T06:30:00Z",
        "description": (
            "Several users report SSO login failures with a generic 'authentication "
            "failed' message. Appears isolated to the auth-service token validation path."
        ),
    },
    "INC0013002": {
        "ticket_id": "INC0013002",
        "short_description": "Order history page loading slowly",
        "priority": "P3 - Medium",
        "category": "Performance",
        "affected_service": "order-service",
        "sla_status": "Within SLA (opened 1h ago, SLA target 8h)",
        "opened_at": "2026-09-25T08:00:00Z",
        "description": (
            "Customers report the order history page taking 10-15 seconds to load, "
            "compared to a usual ~1 second."
        ),
    },
    "INC0013450": {
        "ticket_id": "INC0013450",
        "short_description": "Push notifications delayed by 20+ minutes",
        "priority": "P2 - High",
        "category": "Messaging",
        "affected_service": "notification-service",
        "sla_status": "At risk (opened 3h ago, SLA target 4h)",
        "opened_at": "2026-09-25T09:10:00Z",
        "description": (
            "Customers report order-confirmation and delivery push notifications "
            "arriving 20-30 minutes late. Started shortly after the v2.1.0 deploy."
        ),
    },
    "INC0013789": {
        "ticket_id": "INC0013789",
        "short_description": "Stock counts not syncing between warehouse and storefront",
        "priority": "P3 - Medium",
        "category": "Inventory",
        "affected_service": "inventory-service",
        "sla_status": "Within SLA (opened 5h ago, SLA target 24h)",
        "opened_at": "2026-09-24T22:00:00Z",
        "description": (
            "Storefront is showing items as in-stock that are actually sold out at "
            "the warehouse. The nightly reconciliation sync appears to be failing."
        ),
    },
    "INC0014021": {
        "ticket_id": "INC0014021",
        "short_description": "Product search returning zero results for common queries",
        "priority": "P2 - High",
        "category": "Search",
        "affected_service": "search-service",
        "sla_status": "Breached (opened 5h ago, SLA target 4h)",
        "opened_at": "2026-09-25T04:45:00Z",
        "description": (
            "Multiple customers report that searching for common product names returns "
            "no results. Suspected Elasticsearch cluster issue."
        ),
    },
    "INC0014205": {
        "ticket_id": "INC0014205",
        "short_description": "Shipping label generation failing for international orders",
        "priority": "P1 - Critical",
        "category": "Shipping",
        "affected_service": "shipping-service",
        "sla_status": "Breached (opened 7h ago, SLA target 4h)",
        "opened_at": "2026-09-25T01:30:00Z",
        "description": (
            "All international orders are failing to generate a shipping label. "
            "Domestic orders are unaffected. Began after the carrier API v3 rollout."
        ),
    },
    "INC0014502": {
        "ticket_id": "INC0014502",
        "short_description": "Cart items disappearing after applying a promo code",
        "priority": "P3 - Medium",
        "category": "Checkout",
        "affected_service": "checkout-service",
        "sla_status": "Within SLA (opened 2h ago, SLA target 8h)",
        "opened_at": "2026-09-25T07:20:00Z",
        "description": (
            "Some customers report their cart emptying immediately after applying a "
            "promo code, forcing them to re-add items before checkout."
        ),
    },
}

DEFAULT_TICKET = {
    "ticket_id": "UNKNOWN",
    "short_description": "No matching ticket found in ServiceNow",
    "priority": "Unknown",
    "category": "Unknown",
    "affected_service": "unknown-service",
    "sla_status": "Unknown",
    "opened_at": "Unknown",
    "description": "No ticket record exists for the given ticket ID in the dummy ServiceNow dataset.",
}

DUMMY_LOGS = {
    "payment-service": [
        {"timestamp": "2026-09-25T02:01:12Z", "level": "INFO", "message": "Deployed payment-service v4.2.0"},
        {"timestamp": "2026-09-25T02:04:47Z", "level": "ERROR", "message": "TimeoutException: downstream call to fraud-check-service timed out after 3000ms"},
        {"timestamp": "2026-09-25T02:05:03Z", "level": "ERROR", "message": "HTTP 500: /api/v1/payments/charge failed - connection pool exhausted"},
        {"timestamp": "2026-09-25T02:05:10Z", "level": "ERROR", "message": "TimeoutException: downstream call to fraud-check-service timed out after 3000ms"},
        {"timestamp": "2026-09-25T02:07:22Z", "level": "WARN", "message": "Connection pool utilization at 98%"},
        {"timestamp": "2026-09-25T02:10:55Z", "level": "ERROR", "message": "HTTP 500: /api/v1/payments/charge failed - connection pool exhausted"},
        {"timestamp": "2026-09-25T02:15:31Z", "level": "ERROR", "message": "TimeoutException: downstream call to fraud-check-service timed out after 3000ms"},
    ],
    "auth-service": [
        {"timestamp": "2026-09-25T06:10:02Z", "level": "INFO", "message": "Certificate rotation completed for auth-service"},
        {"timestamp": "2026-09-25T06:15:44Z", "level": "ERROR", "message": "JWT validation failed: signature verification error (unknown key id)"},
        {"timestamp": "2026-09-25T06:16:01Z", "level": "ERROR", "message": "JWT validation failed: signature verification error (unknown key id)"},
        {"timestamp": "2026-09-25T06:20:19Z", "level": "WARN", "message": "Falling back to cached JWKS, refresh from identity provider failed"},
        {"timestamp": "2026-09-25T06:25:47Z", "level": "ERROR", "message": "JWT validation failed: signature verification error (unknown key id)"},
    ],
    "order-service": [
        {"timestamp": "2026-09-25T07:50:10Z", "level": "INFO", "message": "order-service handling increased read traffic"},
        {"timestamp": "2026-09-25T07:55:33Z", "level": "WARN", "message": "Slow query detected: SELECT * FROM order_history took 8200ms"},
        {"timestamp": "2026-09-25T08:01:02Z", "level": "WARN", "message": "Slow query detected: SELECT * FROM order_history took 9100ms"},
        {"timestamp": "2026-09-25T08:05:18Z", "level": "INFO", "message": "Database CPU utilization at 87%"},
    ],
    "notification-service": [
        {"timestamp": "2026-09-25T09:00:05Z", "level": "INFO", "message": "Deployed notification-service v2.1.0"},
        {"timestamp": "2026-09-25T09:05:41Z", "level": "WARN", "message": "Queue depth increasing: push_notifications queue at 15,200 messages"},
        {"timestamp": "2026-09-25T09:08:12Z", "level": "ERROR", "message": "SQS consumer lag: 22 minutes behind, consumer count insufficient for current load"},
        {"timestamp": "2026-09-25T09:12:37Z", "level": "ERROR", "message": "Failed to publish to APNs: connection pool exhausted"},
        {"timestamp": "2026-09-25T09:15:03Z", "level": "WARN", "message": "Retrying failed push batch (attempt 3/5)"},
        {"timestamp": "2026-09-25T09:20:44Z", "level": "ERROR", "message": "SQS consumer lag: 27 minutes behind, consumer count insufficient for current load"},
    ],
    "inventory-service": [
        {"timestamp": "2026-09-24T22:00:00Z", "level": "INFO", "message": "Nightly warehouse reconciliation sync started"},
        {"timestamp": "2026-09-24T22:03:18Z", "level": "ERROR", "message": "Sync job failed: warehouse-feed API returned 429 Too Many Requests"},
        {"timestamp": "2026-09-24T22:03:20Z", "level": "WARN", "message": "Stock delta reconciliation skipped for 3,412 SKUs"},
        {"timestamp": "2026-09-24T22:10:05Z", "level": "ERROR", "message": "Sync job failed: warehouse-feed API returned 429 Too Many Requests"},
        {"timestamp": "2026-09-24T22:10:07Z", "level": "INFO", "message": "Retry scheduled for next sync window (02:00 UTC)"},
    ],
    "search-service": [
        {"timestamp": "2026-09-25T04:30:00Z", "level": "INFO", "message": "Elasticsearch cluster status: yellow"},
        {"timestamp": "2026-09-25T04:35:22Z", "level": "ERROR", "message": "Shard allocation failed: unassigned_shards=4"},
        {"timestamp": "2026-09-25T04:40:09Z", "level": "ERROR", "message": "Query timeout: search request exceeded 5000ms"},
        {"timestamp": "2026-09-25T04:41:53Z", "level": "WARN", "message": "Index refresh interval increased to 30s to reduce cluster load"},
        {"timestamp": "2026-09-25T04:44:17Z", "level": "ERROR", "message": "Query timeout: search request exceeded 5000ms"},
    ],
    "shipping-service": [
        {"timestamp": "2026-09-25T01:00:00Z", "level": "INFO", "message": "Carrier API integration v3 deployed"},
        {"timestamp": "2026-09-25T01:05:14Z", "level": "ERROR", "message": "Label generation failed: carrier API returned 500 for international routes"},
        {"timestamp": "2026-09-25T01:06:02Z", "level": "ERROR", "message": "Label generation failed: invalid customs form schema (carrier API v3 change)"},
        {"timestamp": "2026-09-25T01:10:45Z", "level": "WARN", "message": "Fallback carrier not configured for international routes"},
        {"timestamp": "2026-09-25T01:15:31Z", "level": "ERROR", "message": "Label generation failed: carrier API returned 500 for international routes"},
    ],
    "checkout-service": [
        {"timestamp": "2026-09-25T07:00:00Z", "level": "INFO", "message": "Promo code engine v1.4 deployed"},
        {"timestamp": "2026-09-25T07:08:23Z", "level": "ERROR", "message": "Cart state corrupted after applying promo code PROMO20: race condition in cart-cache update"},
        {"timestamp": "2026-09-25T07:09:01Z", "level": "WARN", "message": "Cart cache invalidation lag detected: 800ms"},
        {"timestamp": "2026-09-25T07:14:52Z", "level": "ERROR", "message": "Cart state corrupted after applying promo code PROMO20: race condition in cart-cache update"},
        {"timestamp": "2026-09-25T07:20:10Z", "level": "ERROR", "message": "Cart state corrupted after applying promo code PROMO20: race condition in cart-cache update"},
    ],
}

DEFAULT_LOGS = [
    {"timestamp": "Unknown", "level": "INFO", "message": "No log records found in the dummy Splunk dataset for this service."},
]


def get_ticket(ticket_id: str) -> dict:
    if not ticket_id:
        return DEFAULT_TICKET
    return DUMMY_TICKETS.get(ticket_id.strip().upper(), DEFAULT_TICKET)


def get_logs(service: str) -> list:
    if not service:
        return DEFAULT_LOGS
    return DUMMY_LOGS.get(service.strip().lower(), DEFAULT_LOGS)
