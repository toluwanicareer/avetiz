TYPE_CHOICES =(
    ('land', "Land"),
	('house', "Houses"),
	('estate', "Estate"),
)

STATUS_CHOICES=(
	('rent', "For Rent"),
	('sale', "For Sale"),
	('lease',"For Lease"),
	)

COLUMN_CHOICES=(
		('value', 'Price DESC'),
		('-value', 'Price ASC'),
		)

LIMIT_CHOICES=(
		(6,'6'),
		(7,'7'),
		(8,'8'),
		(9,'9'),
		(10,'10'),
		)

PICTURE_TYPE_CHOICES=(
		('thumbnail','Thumbnail'),
		('real_size', 'Real Size'),
		)

FEATURE_CATEGORY_CHOICES=(
		('interior','Interior'),
		('exterior','Exterior'),
		('neighborhood','School And Neighborhood'),
		)

FEATURE_HEADER_CHOICES=(
	('kitchen', 'Kitchen'),
	('laundry', 'Laundry'),
	('garage','Garage'),
	('heating','Heating'),
	)

PAYMENT_STATE_CHOICES=(
	('still_payn','still paying'),
	('completed','completed'),
	)

True_OR_FALSE=(
	('Yes'),('yes'),
	('No'),('no'),
	)	

PRICE_CHOICES=(
	('0','ANY'),
	('1000000','N1M'),
	('5000000','N5M'),
	('10000000','N10M'),
	)
