from marshmallow import Schema, fields

class BookingSchema(Schema):
    id = fields.Int(dump_only=True)
    service_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    booking_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)
    booking_status = fields.Str(required=True, default="pending")
