config = {
    "ALLOWED_ACCOUNT_TYPES": {
        "VenueAPI": ('promoter',),
        "DraftOrderAPI": ('consumer', 'admin'),
        "ConcertAPI": ('promoter', 'admin'),
        "ConcertManagerAPI": ('promoter', 'admin')
    },
    "REQUIRED_PARAMS": {
      "ConcertManagerAPI": ('concert_number',),
    },
    "UPDATE_BODY_FIELDS": {
        "ConcertManagerAPI": ('name', 'venue', 'date', 'seat_offering', 'pricing')
    }
}
