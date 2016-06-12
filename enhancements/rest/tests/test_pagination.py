# from rest_framework.test import APITestCase

# from .models import Goods


# class PaginationTestCase(APITestCase):

#     def setUp(self):
#         Goods.objects.bulk_create([
#             Goods(id=i, name='goods', price=i)
#             for i in range(1, 101)
#         ])

#     def test_page(self):
#         response = self.client.get('/goods/?cursor=cD05MQ%3D%3D&ordering=-id')

#         print(response.data)
