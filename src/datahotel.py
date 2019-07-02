class DataHotel(object):
    """Данные об отеле"""

    def __init__(self, name, star, rating, count_of_review, thumb_up, distance_from_center, link_on_hotel, price=None,
                 amenities=None, image=None):
        self._name = name
        self._star = star
        self._rating = rating
        self._count_of_review = count_of_review
        self._thumb_up = thumb_up
        self._distance = distance_from_center
        self._amenities = amenities
        self._image = image
        self._link_on_hotel = link_on_hotel
        self._price = price

    @property
    def get_name(self):
        return self._name

    @property
    def get_price(self):
        return self._price

    @property
    def get_star(self):
        return self._star

    @property
    def get_rating(self):
        return self._rating

    @property
    def get_amenities(self):
        return self._amenities

    @property
    def get_count_of_review(self):
        return self._count_of_review

    @property
    def get_thumb_up(self):
        return self._thumb_up

    @property
    def get_distance_from_center(self):
        return self._distance

    @property
    def get_image(self):
        return self._image

    @property
    def get_link_on_hotel(self):
        return self._link_on_hotel
